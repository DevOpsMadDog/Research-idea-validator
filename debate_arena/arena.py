from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from debate_arena.agents import Agent
from debate_arena.judge import JudgeCandidate, default_judges, pick_best_judge
from debate_arena.llm import LLM


@dataclass(frozen=True)
class DebateConfig:
    rounds: int = 4
    seed: int = 1337


def _tighten_context(context: str, *, max_chars: int = 6000) -> str:
    if len(context) <= max_chars:
        return context
    # Keep the start + end (often contains latest directives).
    head = context[: max_chars // 2]
    tail = context[-max_chars // 2 :]
    return head + "\n\n...[snip]...\n\n" + tail


class DebateArena:
    def __init__(
        self,
        *,
        llm: LLM,
        agents: List[Agent],
        judges: Optional[List[JudgeCandidate]] = None,
        config: Optional[DebateConfig] = None,
    ) -> None:
        self.llm = llm
        self.agents = agents
        self.judges = judges or default_judges()
        self.config = config or DebateConfig()

    def run(self, *, topic: str) -> Dict[str, str]:
        context = ""
        agent_names = [a.name for a in self.agents]

        # Round 0: quick positions (used to pick best judge).
        early = []
        for i, a in enumerate(self.agents):
            msg = a.speak(
                llm=self.llm,
                topic=topic,
                context="(no prior context)",
                task=(
                    "State your position on the idea. Propose the best execution path. "
                    "Also name the single biggest risk or flaw."
                ),
                seed=self.config.seed ^ (i + 1),
            )
            early.append(f"### {a.name}\n{msg}\n")
        early_transcript = "\n".join(early)

        judge, judge_diag = pick_best_judge(
            judge_candidates=self.judges,
            llm=self.llm,
            topic=topic,
            early_transcript=early_transcript,
            agent_names=agent_names,
            seed=self.config.seed,
        )

        context = (
            "=== ROUND 0: OPENING POSITIONS ===\n"
            + early_transcript
            + "\n=== JUDGE SELECTION DIAGNOSTICS ===\n"
            + "\n".join([f"- {k}: {v:.3f}" for k, v in sorted(judge_diag.items())])
            + f"\nChosen judge: {judge.name}\n"
        )

        # Full rounds.
        for r in range(1, self.config.rounds + 1):
            round_msgs: List[str] = []
            directive = (
                "Push the debate forward. Attack weak assumptions. "
                "Quantify tradeoffs. Propose concrete MVP steps."
            )
            for i, a in enumerate(self.agents):
                msg = a.speak(
                    llm=self.llm,
                    topic=topic,
                    context=_tighten_context(context),
                    task=(
                        f"Round {r}: {directive}\n"
                        "Additionally: respond to the judge’s prior 'Missing' and 'Directive' items if present."
                    ),
                    seed=self.config.seed ^ (r * 100 + i + 7),
                )
                round_msgs.append(f"### {a.name}\n{msg}\n")

            round_transcript = "\n".join(round_msgs)
            judge_out = judge.score_round(
                llm=self.llm,
                topic=topic,
                transcript=round_transcript,
                agent_names=agent_names,
                seed=self.config.seed ^ (r * 1000 + 42),
            )

            context += (
                f"\n\n=== ROUND {r}: AGENT ARGUMENTS ===\n"
                + round_transcript
                + f"\n=== ROUND {r}: JUDGE VERDICT ({judge.name}) ===\n"
                + judge_out
                + "\n"
            )

        # Final synthesis: ask the chosen judge to output end-to-end plan + prototype steps.
        final_sys = (
            "You are the final judge and synthesizer. "
            "Produce a complete end-to-end plan and a concrete prototype spec. "
            "Be decisive: pick a direction and justify it."
        )
        final_user = (
            f"TOPIC/IDEA:\n{topic}\n\n"
            f"FULL DEBATE CONTEXT:\n{_tighten_context(context, max_chars=12000)}\n\n"
            "Output format (must follow):\n"
            "## Winner\n"
            "<agent name and 2-3 sentence rationale>\n\n"
            "## End-to-end plan\n"
            "- Goal\n"
            "- Target user\n"
            "- Key assumptions\n"
            "- Architecture (components + data flow)\n"
            "- Guardrails (safety/security/privacy)\n"
            "- MVP scope (1-2 weeks)\n"
            "- Metrics\n"
            "- Risks + mitigations\n\n"
            "## Prototype\n"
            "- Minimal CLI/flow\n"
            "- Data structures\n"
            "- Prompts/rubric\n"
            "- Test plan (manual)\n"
            "- Next iteration\n"
        )
        from debate_arena.llm import Message  # local import to avoid cycles

        final = self.llm.complete(
            messages=[Message(role="system", content=final_sys), Message(role="user", content=final_user)],
            temperature=0.3,
            max_output_tokens=900,
            seed=self.config.seed ^ 9999,
        )

        return {
            "judge": judge.name,
            "debate": context,
            "final": final,
        }
