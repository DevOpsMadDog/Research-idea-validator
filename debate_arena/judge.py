from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Dict, List, Tuple

from debate_arena.llm import LLM, Message


@dataclass(frozen=True)
class JudgeRubric:
    weights: Dict[str, float]


DEFAULT_RUBRIC = JudgeRubric(
    weights={
        "user_value": 1.2,
        "feasibility": 1.2,
        "clarity": 1.0,
        "evidence": 1.0,
        "risk_handling": 1.1,
        "originality": 0.7,
        "operational_detail": 1.0,
    }
)


@dataclass(frozen=True)
class JudgeCandidate:
    name: str
    philosophy: str
    strictness: str

    def score_round(
        self,
        *,
        llm: LLM,
        topic: str,
        transcript: str,
        agent_names: List[str],
        seed: int,
    ) -> str:
        sys = (
            "You are the judge of a multi-agent debate. "
            "You must be fair, skeptical, and rubric-driven. "
            "No fluff: score and justify."
        )
        meta = (
            f"Judge name: {self.name}\n"
            f"Philosophy: {self.philosophy}\n"
            f"Strictness: {self.strictness}\n"
        )
        user = (
            f"TOPIC/IDEA:\n{topic}\n\n"
            f"TRANSCRIPT THIS ROUND:\n{transcript}\n\n"
            f"AGENTS: {', '.join(agent_names)}\n\n"
            "Output format (must follow):\n"
            "1) Winner: <agent name>\n"
            "2) Scores: one line per agent as '<agent>: <0-100>'\n"
            "3) Reasons: 3-8 bullets, cite concrete points from transcript\n"
            "4) Missing: 2-5 bullets for what's not addressed yet\n"
            "5) Directive: 1-3 bullets on what next round must answer\n"
        )
        return llm.complete(
            messages=[
                Message(role="system", content=sys),
                Message(role="system", content=meta),
                Message(role="user", content=user),
            ],
            temperature=0.4,
            max_output_tokens=650,
            seed=seed,
        )


def default_judges() -> List[JudgeCandidate]:
    return [
        JudgeCandidate(
            name="StrictRubric",
            philosophy="Prioritize feasibility + risk-handling; penalize vague claims.",
            strictness="High",
        ),
        JudgeCandidate(
            name="UserValue",
            philosophy="Optimize for user outcomes and trust; penalize complexity.",
            strictness="Medium",
        ),
        JudgeCandidate(
            name="OpsRealist",
            philosophy="Assume production constraints; reward instrumentation and guardrails.",
            strictness="High",
        ),
    ]


def pick_best_judge(
    *,
    judge_candidates: List[JudgeCandidate],
    llm: LLM,
    topic: str,
    early_transcript: str,
    agent_names: List[str],
    seed: int,
) -> Tuple[JudgeCandidate, Dict[str, float]]:
    """Heuristic selection without ground-truth labels.

    We choose the judge that is:
    - Discriminative (spreads scores meaningfully)
    - Consistent (structured output presence)

    Returns: (chosen_judge, diagnostics)
    """

    def parse_scores(text: str) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        for line in text.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            left, right = line.split(":", 1)
            name = left.strip()
            if name in agent_names:
                try:
                    scores[name] = float(right.strip().split()[0])
                except Exception:
                    pass
        return scores

    best = None
    best_metric = -1.0
    diagnostics: Dict[str, float] = {}

    for j in judge_candidates:
        txt = j.score_round(
            llm=llm,
            topic=topic,
            transcript=early_transcript,
            agent_names=agent_names,
            seed=seed ^ (hash(j.name) & 0xFFFF),
        )
        s = parse_scores(txt)
        # Coverage: did it score most agents?
        coverage = len(s) / max(1, len(agent_names))
        spread = 0.0
        if len(s) >= 3:
            spread = statistics.pstdev(list(s.values()))
        metric = coverage * 0.6 + spread * 0.4
        diagnostics[f"{j.name}.coverage"] = coverage
        diagnostics[f"{j.name}.spread"] = spread
        diagnostics[f"{j.name}.metric"] = metric
        if metric > best_metric:
            best_metric = metric
            best = j

    assert best is not None
    diagnostics["chosen.metric"] = best_metric
    return best, diagnostics
