from __future__ import annotations

import argparse
import os
from pathlib import Path

from debate_arena.agents import default_agents
from debate_arena.arena import DebateArena, DebateConfig
from debate_arena.llm import default_llm


def _read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return ""


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="debate_arena")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run multi-agent debate on an idea")
    run.add_argument("--idea", help="Idea text (overrides --idea-file)")
    run.add_argument(
        "--idea-file",
        default="/workspace/sample",
        help="Path to file containing the idea (default: /workspace/sample)",
    )
    run.add_argument("--rounds", type=int, default=4)
    run.add_argument("--seed", type=int, default=1337)
    run.add_argument(
        "--save",
        default="",
        help="Optional path to save the full debate transcript (text)",
    )

    demo = sub.add_parser("demo", help="Run with a built-in sample idea")

    args = p.parse_args(argv)

    llm = default_llm()
    agents = default_agents()

    if args.cmd == "demo":
        idea = (
            "Build a multi-agent debate system that stress-tests product ideas. "
            "Agents argue intensely under a strict rubric; a judge picks a winning plan and produces an MVP prototype spec."
        )
        cfg = DebateConfig(rounds=4, seed=1337)
    else:
        idea = (args.idea or "").strip()
        if not idea:
            idea = _read_text_file(Path(args.idea_file))
        if not idea:
            idea = "(No idea provided. Defaulting to: 'Research a product idea and propose an MVP.')"
        cfg = DebateConfig(rounds=args.rounds, seed=args.seed)

    arena = DebateArena(llm=llm, agents=agents, config=cfg)
    out = arena.run(topic=idea)

    print(f"Chosen judge: {out['judge']}")
    print("\n" + out["final"].strip() + "\n")

    if args.cmd == "run" and args.save:
        Path(args.save).write_text(out["debate"] + "\n\n" + out["final"], encoding="utf-8")
        print(f"Saved transcript to: {args.save}")

    # Helpful hint to use real model.
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "\n(Note: running in offline MockLLM mode. "
            "Set OPENAI_API_KEY to use a real model; optionally set DEBATE_ARENA_MODEL.)"
        )

    return 0
