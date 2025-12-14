from __future__ import annotations

from dataclasses import dataclass
from typing import List

from debate_arena.llm import LLM, Message


@dataclass(frozen=True)
class Agent:
    name: str
    persona: str
    style: str

    def speak(self, *, llm: LLM, topic: str, context: str, task: str, seed: int) -> str:
        sys = (
            "You are an AI agent in a structured debate. "
            "Be intense and adversarial, but do not use slurs, hate, or threats. "
            "Be specific, cite assumptions, and propose concrete next steps."
        )
        persona = (
            f"Name: {self.name}\n"
            f"Persona: {self.persona}\n"
            f"Style: {self.style}\n"
        )
        user = (
            f"TOPIC/IDEA:\n{topic}\n\n"
            f"DEBATE CONTEXT SO FAR:\n{context}\n\n"
            f"YOUR TASK:\n{task}\n\n"
            "Output format:\n"
            "- Claim (1-2 sentences)\n"
            "- Evidence/Reasoning (3-6 bullets)\n"
            "- Attack (2-4 bullets on the weakest opposing assumptions)\n"
            "- Concessions (0-2 bullets)\n"
            "- Actionable next step (1 bullet)\n"
        )
        return llm.complete(
            messages=[
                Message(role="system", content=sys),
                Message(role="system", content=persona),
                Message(role="user", content=user),
            ],
            temperature=0.8,
            max_output_tokens=700,
            seed=seed,
        )


def default_agents() -> List[Agent]:
    return [
        Agent(
            name="Builder",
            persona="Product-minded engineer. Ships MVPs, keeps scope tight.",
            style="Concrete, stepwise, biased-to-action.",
        ),
        Agent(
            name="Skeptic",
            persona="Professional critic. Hunts hidden assumptions and failure modes.",
            style="Combative, precise, ruthless about evidence.",
        ),
        Agent(
            name="Strategist",
            persona="Thinks in systems, distribution, positioning, and moats.",
            style="High-level but grounded, frames tradeoffs.",
        ),
        Agent(
            name="Security",
            persona="Threat modeler. Focuses on abuse, privacy, data handling, prompt injection.",
            style="Forensic, risk-first, mitigation oriented.",
        ),
        Agent(
            name="Economist",
            persona="Cost/ROI analyst. Evaluates incentive alignment, unit economics, viability.",
            style="Numbers-first, skeptical of hand-wavy value.",
        ),
        Agent(
            name="UserAdvocate",
            persona="Represents real users. Cares about UX, trust, friction, and outcomes.",
            style="Blunt, empathy-driven, prioritizes clarity.",
        ),
    ]
