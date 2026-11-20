"""`odczyt` command line: one entry point for the whole episode pipeline.

uv run odczyt new 74                 # episode folder from status.json / whitepapers/
uv run odczyt run 74                 # every stage up to the next gate
uv run odczyt approve 74 script      # after reading review.md
uv run odczyt run 74                 # TTS → scenes → stills review → render
uv run odczyt approve 74 video       # after watching build/{slug}.mp4
uv run odczyt run 74                 # copy to youtube/output, print upload command
uv run odczyt status 74

Episode arguments take ranges and lists: `64-116`, `64,65,70`. With more than one
episode, `run` starts one process per episode (`--jobs` at a time), logs to each
episode's build/run.log and prints a summary.
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from odczyt import llm, render, tts
from odczyt.episode import find_episode_dir, load_episode, new_episode
from odczyt.paths import EPISODES_DIR
from odczyt.pipeline import GATES, STAGE_NAMES, Options, Runner, Stop


def episode_numbers(spec: str) -> list[int]:
    """Parse `73`, `64-116` or `64,65,70-72` into episode numbers."""
    numbers: list[int] = []
    for part in spec.split(","):
        first, _, last = part.strip().partition("-")
        numbers.extend(range(int(first), int(last or first) + 1))
    return numbers


def existing(spec: str) -> list[int]:
    numbers = episode_numbers(spec)
    found = [n for n in numbers if find_episode_dir(n) is not None]
    missing = sorted(set(numbers) - set(found))
    if missing:
        print(f"⚠️  no episode folder (odczyt new): {', '.join(map(str, missing))}")
    return found


def cmd_new(args: argparse.Namespace) -> int:
    numbers = episode_numbers(args.episode)
    if args.paper and len(numbers) != 1:
        raise ValueError("--paper works with one episode")
    for n in numbers:
        if find_episode_dir(n) is not None:
            print(f"⏭️  {n} exists")
            continue
        print(f"✅ {new_episode(n, Path(args.paper) if args.paper else None)}")
    print(f"📋 next: uv run odczyt run {args.episode}")
    return 0


def last_line(log: Path, prefix: str) -> str:
    lines = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.startswith(prefix)]
    return lines[-1] if lines else ""


def run_one_logged(number: int, args: argparse.Namespace) -> tuple[int, int, str]:
    ep = load_episode(number)
    log = ep.build / "run.log"
    cmd = [sys.executable, "-m", "odczyt.cli", "run", str(number)]
    cmd += ["--parallel", str(args.parallel)]
    if args.until:
        cmd += ["--until", args.until]
    for stage in args.force:
        cmd += ["--force", stage]
    if args.api_key_file:
        cmd += ["--api-key-file", args.api_key_file]
    print(f"🔄 {ep.slug} → {ep.rel(log)}", flush=True)
    with log.open("w", encoding="utf-8") as out:
        code = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, check=False).returncode
    stop = last_line(log, "⏸️") or last_line(log, "🎉") or last_line(log, "❌") or "see log"
    print(f"{'✅' if code == 0 else '⏸️ ' if code == 2 else '❌'} {ep.slug}: {stop}", flush=True)
    return number, code, stop


def cmd_run(args: argparse.Namespace) -> int:
    numbers = existing(args.episode)
    if len(numbers) != 1:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(lambda n: run_one_logged(n, args), numbers))
        print("\n| Episode | Result |\n|---|---|")
        for n, _, stop in results:
            print(f"| {n} | {stop.strip()} |")
        return max((code for _, code, _ in results), default=0)
    ep = load_episode(numbers[0])
    runner = Runner(ep, Options(api_key_file=args.api_key_file, parallel=args.parallel))
    try:
        runner.run(until=args.until, force=set(args.force))
    except Stop as e:
        print(f"\n⏸️  {e}")
        print(f"💰 LLM so far: ${llm.total_cost(ep):.2f}")
        return 2
    print(f"\n🎉 {ep.slug} done · LLM ${llm.total_cost(ep):.2f}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    ep = load_episode(args.episode)
    runner = Runner(ep)
    for name, mark in runner.status():
        print(f"{mark} {name}")
    print(
        f"💰 LLM ${llm.total_cost(ep):.2f} · TTS still needed: {tts.missing_characters(ep)} chars"
    )
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    total = 0.0
    for path in sorted(
        EPISODES_DIR.glob("*/episode.yaml"), key=lambda p: int(p.parent.name.split("-")[0])
    ):
        ep = load_episode(path.parent.name.split("-")[0])
        pending = next((n for n, mark in Runner(ep).status() if mark != "✅"), "done")
        cost = llm.total_cost(ep)
        total += cost
        print(f"{ep.slug:40} next: {pending:16} ${cost:6.2f}")
    print(f"💰 LLM total ${total:.2f}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    for n in existing(args.episode):
        Runner(load_episode(n)).approve(args.gate)
        print(f"✅ {n}: approved {args.gate}")
    return 0


def cmd_stills(args: argparse.Namespace) -> int:
    scenes = set(args.scenes.split(",")) if args.scenes else None
    for path in render.render_stills(load_episode(args.episode), scenes):
        print(path)
    return 0


def cmd_step(args: argparse.Namespace) -> int:
    ep = load_episode(args.episode)
    extra = dict(v.split("=", 1) for v in args.var)
    result = llm.run_step(ep, args.step, extra, args.label, args.model)
    print(result.message[:3000])
    if result.ok and args.step == "review" and result.data:
        llm.save_review(ep, result.data)
    return 0 if result.ok else 1


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="odczyt", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(required=True)

    s = sub.add_parser("new", help="Create episode folders for papers")
    s.add_argument("episode", help="Number, range or list")
    s.add_argument("--paper", help="PDF path (default: from whitepapers/status.json)")
    s.set_defaults(func=cmd_new)

    s = sub.add_parser("run", help="Run stages up to the next gate")
    s.add_argument("episode")
    s.add_argument("--until", choices=STAGE_NAMES, help="Stop after this stage")
    s.add_argument("--force", action="append", default=[], choices=STAGE_NAMES)
    s.add_argument("--api-key-file", help="ElevenLabs key file")
    s.add_argument("--parallel", type=int, default=5, help="Parallel claude -p agents")
    s.add_argument("--jobs", type=int, default=2, help="Episodes at a time (batch runs)")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("status", help="Show which stages are fresh")
    s.add_argument("episode")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("list", help="All diagram-first episodes and their next stage")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("approve", help="Owner sign-off for a gate")
    s.add_argument("episode")
    s.add_argument("gate", choices=GATES)
    s.set_defaults(func=cmd_approve)

    s = sub.add_parser("stills", help="Render review stills")
    s.add_argument("episode")
    s.add_argument("--scenes", help="Comma-separated scene ids")
    s.set_defaults(func=cmd_stills)

    s = sub.add_parser("step", help="Run one LLM step by hand")
    s.add_argument("episode")
    s.add_argument("step", choices=sorted(llm.STEPS))
    s.add_argument("--var", action="append", default=[], help="Prompt placeholder KEY=VALUE")
    s.add_argument("--label", help="Log and cost label")
    s.add_argument("--model")
    s.set_defaults(func=cmd_step)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        print(f"❌ {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
