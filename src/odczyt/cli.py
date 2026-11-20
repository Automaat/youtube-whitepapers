"""`odczyt` command line: one entry point for the whole episode pipeline.

uv run odczyt new 74                 # episode folder from status.json / whitepapers/
uv run odczyt run 74                 # every stage up to the next gate
uv run odczyt approve 74 script      # after reading review.md
uv run odczyt run 74                 # TTS → scenes → stills review → render
uv run odczyt approve 74 video       # after watching build/{slug}.mp4
uv run odczyt run 74                 # copy to youtube/output, print upload command
uv run odczyt status 74
"""

import argparse
import sys
from pathlib import Path

from odczyt import llm, render, tts
from odczyt.episode import load_episode, new_episode
from odczyt.paths import EPISODES_DIR
from odczyt.pipeline import GATES, STAGE_NAMES, Options, Runner, Stop


def cmd_new(args: argparse.Namespace) -> int:
    path = new_episode(args.episode, Path(args.paper) if args.paper else None)
    print(f"✅ {path}")
    print(f"📋 next: uv run odczyt run {args.episode}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    ep = load_episode(args.episode)
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
    for path in sorted(EPISODES_DIR.glob("*/episode.yaml")):
        ep = load_episode(path.parent.name.split("-")[0])
        pending = next((n for n, mark in Runner(ep).status() if mark != "✅"), "done")
        print(f"{ep.slug:40} next: {pending}")
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    Runner(load_episode(args.episode)).approve(args.gate)
    print(f"✅ approved {args.gate}")
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

    s = sub.add_parser("new", help="Create an episode folder for a paper")
    s.add_argument("episode", type=int)
    s.add_argument("--paper", help="PDF path (default: from whitepapers/status.json)")
    s.set_defaults(func=cmd_new)

    s = sub.add_parser("run", help="Run stages up to the next gate")
    s.add_argument("episode")
    s.add_argument("--until", choices=STAGE_NAMES, help="Stop after this stage")
    s.add_argument("--force", action="append", default=[], choices=STAGE_NAMES)
    s.add_argument("--api-key-file", help="ElevenLabs key file")
    s.add_argument("--parallel", type=int, default=5, help="Parallel claude -p agents")
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
