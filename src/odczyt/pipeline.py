"""Episode orchestrator: runs every stage in order, skips fresh ones, stops at gates.

State lives in build/state.json. A stage with `inputs` reruns when the digest of
its inputs changes; a stage without `inputs` (LLM generation) runs only while its
output is missing, so hand edits are never overwritten. Outputs that already exist
when no state is recorded are adopted as fresh.
"""

import json
import math
import shutil
import subprocess
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from odczyt import llm, metadata, paper, render, scenes, thumbnails, timeline, tts
from odczyt.episode import Episode, digest
from odczyt.paths import OUTPUT_DIR, REMOTION_DIR, STATUS_FILE, THUMBNAILS_DIR

META_FIELDS = ("title", "subtitle", "authors", "paper_url")
GATES = ("script", "video")


class Stop(Exception):
    """The run cannot continue without the owner (gate, failed check, missing key)."""


@dataclass(frozen=True)
class Stage:
    name: str
    help: str
    done: Callable[["Runner"], bool]
    run: Callable[["Runner"], None]
    inputs: Callable[["Runner"], str] | None = None


@dataclass
class Options:
    api_key_file: str | None = None
    parallel: int = 5


class Runner:
    """Runs stages for one episode and keeps build/state.json."""

    def __init__(self, ep: Episode, options: Options | None = None) -> None:
        self.ep = ep
        self.options = options or Options()
        self.state_path = ep.build / "state.json"
        self.state = (
            json.loads(self.state_path.read_text(encoding="utf-8"))
            if self.state_path.exists()
            else {}
        )
        self.state.setdefault("stages", {})
        self.state.setdefault("approvals", {})

    def save(self) -> None:
        llm.write_json(self.state_path, self.state)

    def setting(self, key: str, default: object) -> object:
        return self.ep.config.get("pipeline", {}).get(key, default)

    def gates(self) -> set[str]:
        return set(self.setting("gates", list(GATES)))

    def fresh(self, stage: Stage, adopt: bool = True) -> bool:
        """Output exists and inputs are unchanged; unrecorded outputs count only if `adopt`."""
        if not stage.done(self):
            return False
        if stage.inputs is None:
            return True
        recorded = self.state["stages"].get(stage.name)
        if recorded is None:
            return adopt
        return recorded == stage.inputs(self)

    def status(self) -> list[tuple[str, str]]:
        rows = []
        upstream_fresh = True
        for stage in STAGES:
            ok = self.fresh(stage, adopt=upstream_fresh)
            upstream_fresh = upstream_fresh and ok
            rows.append((stage.name, "✅" if ok else "⏳"))
        return rows

    def run(self, until: str | None = None, force: set[str] | None = None) -> None:
        """Run stale stages in order. Outputs without a recorded digest are adopted only
        while nothing upstream has run, so they never mask changes made in this run."""
        force = force or set()
        ran = False
        for stage in STAGES:
            if stage.name not in force and self.fresh(stage, adopt=not ran):
                if stage.inputs is not None and stage.name not in self.state["stages"]:
                    self.state["stages"][stage.name] = stage.inputs(self)
                    self.save()
                print(f"✅ {stage.name}", flush=True)
            else:
                print(f"\n🔄 {stage.name}: {stage.help}", flush=True)
                stage.run(self)
                ran = True
                if stage.inputs is not None:
                    self.state["stages"][stage.name] = stage.inputs(self)
                self.save()
            if stage.name == until:
                return

    def approve(self, gate: str) -> None:
        self.state["approvals"][gate] = GATE_DIGEST[gate](self)
        self.save()

    def parallel(self, jobs: list[Callable[[], llm.LlmResult]]) -> list[llm.LlmResult]:
        with ThreadPoolExecutor(max_workers=self.options.parallel) as pool:
            return list(pool.map(lambda job: job(), jobs))

    def step(self, name: str, extra: dict[str, str] | None = None, label: str | None = None):
        result = llm.run_step(self.ep, name, extra, label)
        if not result.ok:
            raise Stop(result.message)
        return result


def storyboard_core(r: Runner) -> dict:
    sb = r.ep.storyboard()
    return {k: v for k, v in sb.items() if k != "thumbnail"}


def script_digest(r: Runner) -> str:
    return digest(r.ep.file("script.yaml"), storyboard_core(r))


def scene_code_files(r: Runner) -> list[Path]:
    return sorted(r.ep.scenes_dir.glob("*.ts*"))


def visuals_digest(r: Runner) -> str:
    design = sorted((REMOTION_DIR / "src" / "design").glob("*"))
    core = [REMOTION_DIR / "src" / name for name in ("Episode.tsx", "timeline.ts", "Root.tsx")]
    return digest(*scene_code_files(r), *design, *core, r.ep.public / "timeline.json")


def video_path(r: Runner) -> Path:
    return r.ep.build / f"{r.ep.slug}.mp4"


def published(r: Runner) -> list[tuple[Path, Path]]:
    ep = r.ep
    return [
        (video_path(r), OUTPUT_DIR / f"{ep.slug}.mp4"),
        (ep.build / "metadata.txt", OUTPUT_DIR / f"{ep.slug}-metadata.txt"),
        (ep.build / "captions.srt", OUTPUT_DIR / f"{ep.slug}.srt"),
        (ep.build / "thumbnail.png", THUMBNAILS_DIR / f"{ep.slug}.png"),
    ]


GATE_DIGEST: dict[str, Callable[[Runner], str]] = {
    "script": script_digest,
    "video": lambda r: digest(video_path(r)),
}


def ensure_node_modules() -> None:
    if not (REMOTION_DIR / "node_modules").exists():
        print("🔄 npm ci (Remotion dependencies)", flush=True)
        subprocess.run(["npm", "ci"], cwd=REMOTION_DIR, check=True)


def typecheck() -> None:
    proc = subprocess.run(
        ["npm", "run", "typecheck"], cwd=REMOTION_DIR, capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise Stop(f"Typecheck failed:\n{proc.stdout[-3000:]}")


def run_paper(r: Runner) -> None:
    print(f"✅ {paper.write_paper_text(r.ep)} pages")


def run_meta(r: Runner) -> None:
    data = r.step("meta").data or {}
    r.ep.update(**{k: data[k] for k in META_FIELDS if not r.ep.raw.get(k)})
    print(f"📋 {r.ep.config['title']}: {r.ep.config['subtitle']}")


def run_review(r: Runner) -> None:
    rounds = int(r.setting("review_rounds", 4))
    for n in range(1, rounds + 1):
        review = r.step("review", label=f"review-r{n}").data or {}
        llm.save_review(r.ep, review)
        print(f"📋 round {n}: {review['verdict']}, {len(review['must_fix'])} must-fix")
        if review["verdict"] == "pass":
            return
        if n < rounds:
            r.step("script-fix", label=f"script-fix-r{n}")
    raise Stop(
        f"Scenario review still fails after {rounds} rounds; see {r.ep.rel(r.ep.file('review.md'))}"
    )


def review_passed(r: Runner) -> bool:
    path = r.ep.file("review.json")
    return path.exists() and json.loads(path.read_text(encoding="utf-8"))["verdict"] == "pass"


def gate(name: str, what: str) -> Stage:
    def done(r: Runner) -> bool:
        if name not in r.gates():
            return True
        return r.state["approvals"].get(name) == GATE_DIGEST[name](r)

    def stop(r: Runner) -> None:
        raise Stop(f"Gate: {what}\n   then: uv run odczyt approve {r.ep.number} {name}")

    return Stage(f"approve-{name}", what, done, stop)


def run_tts(r: Runner) -> None:
    chars = tts.missing_characters(r.ep)
    print(f"📋 {chars} characters to synthesize (≈{chars // 2} credits)")
    key = None
    if chars:
        item = r.ep.config.get("elevenlabs", {}).get("bitwarden_item")
        key = tts.resolve_api_key(r.options.api_key_file, item)
        if not key:
            raise Stop(
                "No ElevenLabs key: pass --api-key-file, set ELEVENLABS_API_KEY, "
                "or export BW_SESSION=$(bw unlock --raw)"
            )
        needed = math.ceil(
            chars * float(r.ep.config.get("elevenlabs", {}).get("credits_per_char", 0.5))
        )
        left = tts.remaining_credits(key)
        if left is not None and left < needed:
            raise Stop(f"ElevenLabs: about {needed} credits needed, {left} left this period")
    try:
        tts.synthesize_episode(r.ep, key)
    except RuntimeError as e:
        raise Stop(str(e)) from e


def tts_digest(r: Runner) -> str:
    segs = [
        {k: s[k] for k in ("id", "speaker", "scene", "text")} for s in r.ep.script()["segments"]
    ]
    return digest(segs, r.ep.config["voices"], r.ep.config.get("tts_model"))


def run_timeline(r: Runner) -> None:
    try:
        timeline.build_timeline(r.ep)
    except ValueError as e:
        raise Stop(str(e)) from e


def run_layout(r: Runner) -> None:
    ensure_node_modules()
    scenes.scaffold(r.ep)
    r.step("layout")


def scene_parts(r: Runner) -> list[tuple[str, list[str]]]:
    return scenes.plan_parts(r.ep.storyboard())


def scenes_done(r: Runner) -> bool:
    return all(not scenes.is_placeholder(r.ep.scenes_dir / f"{p}.tsx") for p, _ in scene_parts(r))


def run_scenes(r: Runner) -> None:
    ensure_node_modules()
    parts = scenes.scaffold(r.ep)
    todo = [(p, ids) for p, ids in parts if scenes.is_placeholder(r.ep.scenes_dir / f"{p}.tsx")]
    results = r.parallel(
        [
            lambda p=p, ids=ids: llm.run_step(
                r.ep, "scenes", {"part": p, "scene_ids": ",".join(ids)}, f"scenes-{p}"
            )
            for p, ids in todo
        ]
    )
    failed = [res.message for res in results if not res.ok]
    if failed or not scenes_done(r):
        raise Stop("Scene generation incomplete:\n" + "\n".join(failed))
    typecheck()


def review_stills(r: Runner, names: list[str], label: str) -> list[dict]:
    """Review stills in parallel chunks; return all findings."""
    size = int(r.setting("stills_per_review", 14))
    chunks = scenes.chunk_stills(names, size)
    results = r.parallel(
        [
            lambda i=i, chunk=chunk: llm.run_step(
                r.ep,
                "stills-review",
                {"scope": ", ".join(f"{n}.png" for n in chunk)},
                f"{label}-c{i}",
            )
            for i, chunk in enumerate(chunks, 1)
        ]
    )
    failed = [res.message for res in results if not res.ok]
    if failed:
        raise Stop("Stills review failed:\n" + "\n".join(failed))
    return [f for res in results for f in (res.data or {})["findings"]]


def save_findings(r: Runner, findings: list[dict]) -> bool:
    blockers = [f for f in findings if f["severity"] == "blocker"]
    verdict = "fail" if blockers else "pass"
    llm.write_json(r.ep.build / "stills-review.json", {"verdict": verdict, "findings": findings})
    print(f"📋 stills: {len(blockers)} blockers, {len(findings) - len(blockers)} minor")
    return not blockers


def fix_job(r: Runner, part: str, scene_ids: list[str], label: str) -> Callable[[], llm.LlmResult]:
    extra = {"part": part, "scene_ids": ",".join(scene_ids)}
    return lambda: llm.run_step(r.ep, "scenes-fix", extra, label)


def run_stills_review(r: Runner) -> None:
    rounds = int(r.setting("stills_fix_rounds", 2))
    names = [p.stem for p in render.render_stills(r.ep)]
    findings = review_stills(r, names, "stills-review-r0")
    by_part = scenes.part_of_scene(scene_parts(r))
    for n in range(1, rounds + 1):
        if save_findings(r, findings):
            return
        blocked = {f["scene"] for f in findings if f["severity"] == "blocker"}
        affected = sorted(blocked & by_part.keys())
        if not affected:
            break
        jobs = [
            fix_job(r, part, [s for s in affected if by_part[s] == part], f"scenes-fix-r{n}-{part}")
            for part in sorted({by_part[s] for s in affected})
        ]
        results = r.parallel(jobs)
        failed = [res.message for res in results if not res.ok]
        if failed:
            raise Stop("Scene fix failed:\n" + "\n".join(failed))
        typecheck()
        rerendered = [p.stem for p in render.render_stills(r.ep, set(affected))]
        kept = [f for f in findings if f["scene"] not in affected]
        findings = kept + review_stills(r, rerendered, f"stills-review-r{n}")
    if not save_findings(r, findings):
        raise Stop(
            f"Stills still have blockers after {rounds} fix rounds; "
            f"see {r.ep.rel(r.ep.build / 'stills-review.json')}"
        )


def stills_passed(r: Runner) -> bool:
    path = r.ep.build / "stills-review.json"
    return path.exists() and json.loads(path.read_text(encoding="utf-8"))["verdict"] == "pass"


def thumbnail_image_ready(r: Runner) -> bool:
    image = r.ep.thumbnail_image()
    return image is None or image.exists()


def ask_thumbnail_image(r: Runner) -> None:
    """Recover an earlier dog thumbnail (git history, then YouTube) or ask for a new one."""
    image = r.ep.thumbnail_image()
    if thumbnails.from_git(r.ep.repo, image):
        print(f"✅ {r.ep.rel(image)} restored from git history")
        return
    url = thumbnails.youtube_url(STATUS_FILE, r.ep.number)
    if url and thumbnails.from_youtube(url, image):
        print(f"✅ {r.ep.rel(image)} downloaded from {url}")
        return
    prompt = r.ep.thumbnail_prompt()
    source = r.ep.rel(prompt) if prompt.exists() else "/generate-thumbnails"
    raise Stop(
        f"Thumbnail: generate the dog image from {source} and save it as {r.ep.rel(image)}\n"
        "   (or set `thumbnail: diagram` in episode.yaml), then rerun"
    )


def run_thumbnail(r: Runner) -> None:
    image = r.ep.thumbnail_image()
    if image is not None:
        shutil.copy2(image, r.ep.build / "thumbnail.png")
        print(f"✅ {r.ep.rel(image)} (hand-made)")
        return
    ensure_node_modules()
    print(f"✅ {r.ep.rel(render.render_thumbnail(r.ep))}")


def thumbnail_digest(r: Runner) -> str:
    image = r.ep.thumbnail_image()
    return digest(image) if image is not None else visuals_digest(r)


def run_metadata(r: Runner) -> None:
    data = r.step("metadata").data or {}
    tl = render.load_timeline(r.ep)
    text = metadata.format_metadata(r.ep, data, tl)
    (r.ep.build / "metadata.txt").write_text(text, encoding="utf-8")
    print(text.split("\n", 2)[1])


def run_render(r: Runner) -> None:
    ensure_node_modules()
    video = render.render_video(r.ep)
    problems = render.verify_video(
        video, r.ep.public / "narration.wav", float(render.load_timeline(r.ep)["outroSeconds"])
    )
    if problems:
        raise Stop("Video verification failed: " + "; ".join(problems))
    print(f"✅ {r.ep.rel(video)} verified")


def run_publish(r: Runner) -> None:
    for src, dst in published(r):
        if not src.exists():
            raise Stop(f"Missing {r.ep.rel(src)}")
        if dst.exists() and digest(dst) != digest(src) and not r.state["stages"].get("publish"):
            raise Stop(
                f"{r.ep.rel(dst)} already exists; move it away or rerun with --force publish"
            )
    for src, dst in published(r):
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"✅ {r.ep.rel(dst)}")
    print(f"📋 next: mise run upload -- {r.ep.number}   (private upload, then mise run publish)")


def generate(step: str) -> Callable[[Runner], None]:
    def run(r: Runner) -> None:
        r.step(step)

    return run


def publish_done(r: Runner) -> bool:
    return all(dst.exists() and digest(dst) == digest(src) for src, dst in published(r))


def file_exists(*names: str) -> Callable[[Runner], bool]:
    return lambda r: all(r.ep.file(n).exists() for n in names)


def build_exists(*names: str) -> Callable[[Runner], bool]:
    return lambda r: all((r.ep.build / n).exists() for n in names)


STAGES: list[Stage] = [
    Stage(
        "paper",
        "extract paper text",
        file_exists("paper.txt"),
        run_paper,
        lambda r: digest(r.ep.repo / r.ep.config["paper"]),
    ),
    Stage(
        "meta",
        "title, subtitle, authors, paper URL",
        lambda r: all(r.ep.raw.get(k) for k in META_FIELDS),
        run_meta,
    ),
    Stage(
        "storyboard",
        "plan chapters, scenes, cues",
        file_exists("storyboard.yaml"),
        generate("storyboard"),
    ),
    Stage("script", "write narration", file_exists("script.yaml"), generate("script")),
    Stage("review", "fact-check script, fix until pass", review_passed, run_review, script_digest),
    gate("script", "read review.md and script.yaml"),
    Stage(
        "thumbnail-image",
        "dog thumbnail: git history, YouTube, or by hand",
        thumbnail_image_ready,
        ask_thumbnail_image,
    ),
    Stage(
        "tts",
        "ElevenLabs narration (cached per segment)",
        build_exists("tts/manifest.json"),
        run_tts,
        tts_digest,
    ),
    Stage(
        "timeline",
        "narration.wav, timeline.json, captions",
        build_exists("public/timeline.json", "public/narration.wav"),
        run_timeline,
        lambda r: digest(
            r.ep.build / "tts" / "manifest.json",
            r.ep.storyboard(),
            {k: r.ep.config.get(k) for k in (*META_FIELDS, "theme")},
            r.ep.thumbnail_image() or "",
        ),
    ),
    Stage(
        "layout",
        "shared diagram geometry",
        lambda r: (r.ep.scenes_dir / "layout.ts").exists(),
        run_layout,
    ),
    Stage("scenes", "scene code, one agent per chapter", scenes_done, run_scenes),
    Stage(
        "stills-review",
        "review frames, fix scenes until no blockers",
        stills_passed,
        run_stills_review,
        visuals_digest,
    ),
    Stage(
        "thumbnail",
        "dog image or rendered 1280x720 card",
        build_exists("thumbnail.png"),
        run_thumbnail,
        thumbnail_digest,
    ),
    Stage(
        "metadata",
        "YouTube title, description, chapters, tags",
        build_exists("metadata.txt"),
        run_metadata,
        lambda r: digest(r.ep.file("script.yaml"), r.ep.public / "timeline.json", r.ep.raw),
    ),
    Stage(
        "render",
        "render and verify the video",
        lambda r: video_path(r).exists(),
        run_render,
        visuals_digest,
    ),
    gate("video", "watch the video, thumbnail and metadata"),
    Stage(
        "publish",
        "copy to youtube/output and youtube/thumbnails",
        publish_done,
        run_publish,
        lambda r: digest(*[src for src, _ in published(r)]),
    ),
]

STAGE_NAMES = [s.name for s in STAGES]
