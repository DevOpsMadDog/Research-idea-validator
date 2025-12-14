from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Message:
    role: str  # "system" | "user" | "assistant"
    content: str


class LLM:
    """Tiny abstraction over a text-generation backend.

    - If OPENAI_API_KEY is set, uses OpenAI Responses API via urllib (no extra deps).
    - Otherwise uses a deterministic "mock" generator for offline prototyping.
    """

    def complete(
        self,
        *,
        messages: List[Message],
        temperature: float = 0.7,
        max_output_tokens: int = 600,
        seed: Optional[int] = None,
    ) -> str:
        raise NotImplementedError


class MockLLM(LLM):
    def __init__(self, *, salt: str = "debate_arena") -> None:
        self._salt = salt

    def complete(
        self,
        *,
        messages: List[Message],
        temperature: float = 0.7,
        max_output_tokens: int = 600,
        seed: Optional[int] = None,
    ) -> str:
        # Deterministic-ish text: hash the prompt + salt, then sample from templates.
        prompt = "\n".join([f"{m.role.upper()}: {m.content}" for m in messages])
        h = hashlib.sha256((self._salt + "\n" + prompt).encode("utf-8")).hexdigest()
        base_seed = int(h[:8], 16)
        if seed is not None:
            base_seed ^= seed
        rng = random.Random(base_seed)

        # Heuristic: obey strict formats used by the arena so the prototype is runnable offline.
        user_text = ""
        for m in reversed(messages):
            if m.role == "user":
                user_text = m.content
                break
        format_tail = ""
        if "Output format (must follow):" in user_text:
            format_tail = user_text.split("Output format (must follow):", 1)[1]
        else:
            format_tail = user_text

        def _parse_agents(s: str) -> List[str]:
            for line in s.splitlines():
                if line.strip().startswith("AGENTS:"):
                    tail = line.split("AGENTS:", 1)[1].strip()
                    return [a.strip() for a in tail.split(",") if a.strip()]
            return []

        def _cap(text: str) -> str:
            return text[: max_output_tokens * 4].rstrip()

        # Judge scoring output.
        if "1) Winner:" in format_tail and "2) Scores:" in format_tail:
            agents = _parse_agents(user_text) or ["Builder", "Skeptic", "Strategist"]
            # Create a spread of scores.
            base = rng.randint(62, 78)
            scores = {a: max(0, min(100, base + rng.randint(-12, 18))) for a in agents}
            winner = max(scores.items(), key=lambda kv: kv[1])[0]
            reasons = [
                "Identified a concrete MVP and reduced scope creep.",
                "Called out a specific failure mode and offered mitigation.",
                "Made tradeoffs explicit (cost, complexity, timeline).",
                "Anchored to user outcomes rather than model theatrics.",
            ]
            rng.shuffle(reasons)
            missing = [
                "Real user validation plan (who, where, how many, success criteria).",
                "Operational guardrails (rate limits, abuse handling, audit logs).",
                "Evaluation: rubric calibration and judge drift monitoring.",
            ]
            rng.shuffle(missing)
            directive = [
                "Force an explicit architecture diagram in words (components + data flow).",
                "Quantify MVP effort (days) and list dependencies.",
            ]
            out = []
            out.append(f"1) Winner: {winner}")
            out.append("2) Scores:")
            out.extend([f"{a}: {scores[a]}" for a in agents])
            out.append("3) Reasons:")
            out.extend([f"- {r}" for r in reasons[: rng.randint(3, 5)]])
            out.append("4) Missing:")
            out.extend([f"- {m}" for m in missing[: rng.randint(2, 4)]])
            out.append("5) Directive:")
            out.extend([f"- {d}" for d in directive[: rng.randint(1, 2)]])
            return _cap("\n".join(out))

        # Final synthesis output.
        if "## Winner" in format_tail and "## End-to-end plan" in format_tail and "## Prototype" in format_tail:
            winner = rng.choice(["Builder", "Skeptic", "OpsRealist", "UserAdvocate"])
            out = []
            out.append("## Winner")
            out.append(f"{winner} — best balance of feasibility, risk control, and a shippable MVP.")
            out.append("")
            out.append("## End-to-end plan")
            out.append("- Goal: Stress-test an idea via multi-agent debate and output a decisive MVP plan.")
            out.append("- Target user: Solo builders, PMs, founders validating execution paths.")
            out.append("- Key assumptions: Users want structured critique; the rubric can be made measurable; output is actionable, not just prose.")
            out.append("- Architecture (components + data flow): CLI/API -> orchestrator -> agents (round-robin) -> judge (scoring + directives) -> synthesizer -> report + saved transcript.")
            out.append("- Guardrails (safety/security/privacy): no secrets in prompts; redaction hooks; prompt-injection aware system prompts; audit logs; rate limits if deployed.")
            out.append("- MVP scope (1-2 weeks): CLI runner, 5-7 personas, judge rubric + scoring, transcript export, basic regression fixtures.")
            out.append("- Metrics: decision usefulness (user rating), time-to-MVP plan, number of actionable risks found, rubric consistency, cost per run.")
            out.append("- Risks + mitigations: hallucinated certainty -> require citations/assumptions; judge bias -> multi-judge calibration; overlong output -> token/section caps.")
            out.append("")
            out.append("## Prototype")
            out.append("- Minimal CLI/flow: `python3 -m debate_arena run --idea '...idea...' --save debate_output.txt`")
            out.append("- Data structures: Agent(name/persona/style), Transcript(rounds), Judge verdict (winner + per-agent scores + missing + directive).")
            out.append("- Prompts/rubric: strict sectioned output for agents and judge; judge rubric = value/feasibility/risk/clarity/evidence.")
            out.append("- Test plan (manual): run demo; confirm judge selection + parseable scores; confirm transcript file writes; confirm deterministic seed behavior.")
            out.append("- Next iteration: add real evaluation set, per-domain agent libraries, and judge drift monitoring.")
            return _cap("\n".join(out))

        # Agent speaking format.
        if "Output format:" in format_tail and "Claim (1-2 sentences)" in format_tail:
            claim = rng.choice(
                [
                    "This idea works if you force structure: rubric-driven debate that ends in a build plan, not vibes.",
                    "The core risk is that multi-agent debate becomes content generation unless you hard-wire measurable outputs.",
                    "You can win by shipping a narrow MVP that produces decisions users can act on within an hour.",
                ]
            )
            ev = [
                "Define success metrics up front (time saved, decision confidence, MVP quality).",
                "Use constrained formats so outputs are parseable and comparable round-to-round.",
                "Make agents disagree by design: assign conflicting objectives and penalize conformity.",
                "Add guardrails: injection resistance, redaction, and refusal handling where needed.",
                "Cap tokens and force prioritization to prevent essay inflation.",
            ]
            atk = [
                "If the rubric is vague, the judge will reward style over substance.",
                "If agents share the same model and prompts, they converge and debate becomes fake diversity.",
                "Without user feedback loops, you can’t tell if the output is actually useful.",
            ]
            con = [
                "A fully automated 'best plan' can mislead; require explicit assumptions and risks.",
                "Some ideas need domain expertise; persona prompts won’t replace it.",
            ]
            rng.shuffle(ev)
            rng.shuffle(atk)
            rng.shuffle(con)
            out = []
            out.append(f"- Claim: {claim}")
            out.append("- Evidence/Reasoning:")
            out.extend([f"  - {b}" for b in ev[: rng.randint(3, 6)]])
            out.append("- Attack:")
            out.extend([f"  - {b}" for b in atk[: rng.randint(2, 4)]])
            out.append("- Concessions:")
            out.extend([f"  - {b}" for b in con[: rng.randint(0, 2)]])
            out.append("- Actionable next step:")
            out.append("  - Implement a round-based transcript + judge scoring loop with deterministic seeds.")
            return _cap("\n".join(out))

        tone = rng.choice(
            [
                "direct",
                "forensic",
                "combative",
                "methodical",
                "sharp",
            ]
        )
        openers = {
            "direct": ["Here’s the core:", "Net: ", "Bottom line:"],
            "forensic": ["Evidence first:", "Let’s isolate constraints:", "Trace the failure modes:"],
            "combative": ["No—here’s what you missed:", "That’s optimistic. Reality:", "You’re hand-waving. Facts:"],
            "methodical": ["Step-by-step:", "We can decompose this:", "Let’s structure it:"],
            "sharp": ["Cutting through noise:", "Stop guessing—do this:", "The winning move:"]
        }
        bullets = [
            "Define the user’s success metric and non-goals.",
            "Reduce the solution to the smallest verifiable MVP.",
            "List risks (technical, operational, legal) and mitigations.",
            "Instrument feedback loops; ship, measure, iterate.",
            "Prefer simple dataflow; avoid premature complexity.",
            "Make the judge rubric explicit and auditable.",
        ]
        rng.shuffle(bullets)

        # Squeeze to max_output_tokens roughly by limiting bullet count.
        n = max(4, min(8, max_output_tokens // 90))
        chosen = bullets[:n]

        closing = rng.choice(
            [
                "If you can’t test it, it’s not a plan.",
                "The debate is theater unless the rubric is measurable.",
                "Now build it and let users veto your assumptions.",
            ]
        )

        text = "\n".join(
            [
                rng.choice(openers[tone]),
                "\n".join([f"- {b}" for b in chosen]),
                closing,
            ]
        )
        return text[: max_output_tokens * 4]  # crude char cap


class OpenAIResponsesLLM(LLM):
    def __init__(self, *, model: str = "gpt-4.1-mini", api_key: Optional[str] = None) -> None:
        self._model = model
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY not set")

    def complete(
        self,
        *,
        messages: List[Message],
        temperature: float = 0.7,
        max_output_tokens: int = 600,
        seed: Optional[int] = None,
    ) -> str:
        # Minimal Responses API request.
        url = "https://api.openai.com/v1/responses"
        payload: Dict[str, Any] = {
            "model": self._model,
            "input": [
                {"role": m.role, "content": [{"type": "input_text", "text": m.content}]}
                for m in messages
            ],
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }
        if seed is not None:
            payload["seed"] = seed

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI HTTPError {e.code}: {body}") from e
        except Exception as e:
            raise RuntimeError(f"OpenAI request failed: {e}") from e

        obj = json.loads(raw)
        # Extract text from output.
        out_texts: List[str] = []
        for item in obj.get("output", []):
            for c in item.get("content", []):
                if c.get("type") in ("output_text", "text"):
                    out_texts.append(c.get("text", ""))
        if not out_texts:
            # Fallback: some SDK shapes differ; keep it robust.
            out_texts.append(json.dumps(obj, indent=2)[:2000])
        # Gentle rate limiting for repeated calls.
        time.sleep(0.05)
        return "\n".join([t for t in out_texts if t]).strip()


def default_llm() -> LLM:
    if os.environ.get("OPENAI_API_KEY"):
        model = os.environ.get("DEBATE_ARENA_MODEL", "gpt-4.1-mini")
        return OpenAIResponsesLLM(model=model)
    return MockLLM()
