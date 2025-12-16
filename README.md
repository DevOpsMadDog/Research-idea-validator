# Cursor.ai Debate Pack — Creator Risk Scoring + Parametric Protection

**Purpose:** Run a structured multi-model debate inside Cursor to produce a *risk-averse, investor-grade* startup concept that measures creator risk, de-risks operations, and offers only narrowly scoped *parametric* protection (not "views down" insurance).

---

## Quick Start

1. **Review Debate Master Context:** `/workspace/00-DEBATE-MASTER-CONTEXT.md`
2. **Execute Role Prompts:** Use prompts in `/workspace/01-ROLE-PROMPTS/` with assigned models
3. **Review Red Team Output:** `/workspace/02-RED-TEAM-OUTPUT.md` (already completed)
4. **Synthesize with Final Judge:** Use `/workspace/01-ROLE-PROMPTS/05-FINAL-JUDGE.md` with GPT-5.2

---

## Agent Assignments

| Role | Model | Status | Output File |
|---|---|---|---|
| Actuary / Insurance & Reinsurance | Opus 4.5 | ⏳ Pending | `04-ACTUARY-OUTPUT.md` |
| Regulatory & Compliance (India-first) | Gemini 3 Pro | ⏳ Pending | `05-REGULATORY-OUTPUT.md` |
| Creator Economy Operator (Product/GTM) | Sonnet 4.5 | ⏳ Pending | `06-CREATOR-ECONOMY-OUTPUT.md` |
| Red Team / Skeptic | Composer 1 | ✅ Complete | `02-RED-TEAM-OUTPUT.md` |
| Final Judge / Curator | GPT-5.2 | ⏳ Pending | `07-FINAL-JUDGE-OUTPUT.md` |

---

## Execution Instructions

### Step 1: Actuary Role (Opus 4.5)

1. Open Cursor with Opus 4.5 selected
2. Paste contents of `00-DEBATE-MASTER-CONTEXT.md`
3. Paste contents of `01-ROLE-PROMPTS/01-ACTUARY-INSURANCE.md`
4. Save output to `04-ACTUARY-OUTPUT.md`

### Step 2: Regulatory Role (Gemini 3 Pro)

1. Open Cursor with Gemini 3 Pro selected
2. Paste contents of `00-DEBATE-MASTER-CONTEXT.md`
3. Paste contents of `01-ROLE-PROMPTS/02-REGULATORY-COMPLIANCE.md`
4. Save output to `05-REGULATORY-OUTPUT.md`

### Step 3: Creator Economy Role (Sonnet 4.5)

1. Open Cursor with Sonnet 4.5 selected
2. Paste contents of `00-DEBATE-MASTER-CONTEXT.md`
3. Paste contents of `01-ROLE-PROMPTS/03-CREATOR-ECONOMY-OPERATOR.md`
4. Save output to `06-CREATOR-ECONOMY-OUTPUT.md`

### Step 4: Final Judge (GPT-5.2)

1. Open Cursor with GPT-5.2 selected
2. Paste contents of `00-DEBATE-MASTER-CONTEXT.md`
3. Paste contents of `01-ROLE-PROMPTS/05-FINAL-JUDGE.md`
4. Include all role outputs:
   - `04-ACTUARY-OUTPUT.md`
   - `05-REGULATORY-OUTPUT.md`
   - `06-CREATOR-ECONOMY-OUTPUT.md`
   - `02-RED-TEAM-OUTPUT.md`
5. Include scoring rubric: `03-SCORING-RUBRIC.md`
6. Save output to `07-FINAL-JUDGE-OUTPUT.md`

---

## File Structure

```
/workspace/
├── 00-DEBATE-MASTER-CONTEXT.md          # Master context (paste to all agents)
├── 01-ROLE-PROMPTS/
│   ├── 01-ACTUARY-INSURANCE.md          # Actuary role prompt
│   ├── 02-REGULATORY-COMPLIANCE.md      # Regulatory role prompt
│   ├── 03-CREATOR-ECONOMY-OPERATOR.md   # Creator economy role prompt
│   ├── 04-RED-TEAM-SKEPTIC.md           # Red team role prompt (reference)
│   └── 05-FINAL-JUDGE.md                # Final judge prompt
├── 02-RED-TEAM-OUTPUT.md                # ✅ Red team analysis (complete)
├── 03-SCORING-RUBRIC.md                 # Scoring rubric for final judge
├── 04-ACTUARY-OUTPUT.md                 # ⏳ Actuary output (pending)
├── 05-REGULATORY-OUTPUT.md              # ⏳ Regulatory output (pending)
├── 06-CREATOR-ECONOMY-OUTPUT.md         # ⏳ Creator economy output (pending)
└── 07-FINAL-JUDGE-OUTPUT.md             # ⏳ Final synthesis (pending)
```

---

## Key Constraints (Non-Negotiable)

- General income volatility and algorithm changes are **NOT** directly insurable
- Only narrow, parametric, externally verifiable risks can be insured
- Systemic/correlated risks must be excluded, capped, or shifted to partners
- Moral hazard must be controlled with gating, exclusions, and deductibles
- Solution must be viable under conservative insurance + regulatory logic

---

## Red Team Findings (Summary)

The Red Team analysis identifies **20+ critical failure modes** across:
- Insurance & actuarial risks (correlation, moral hazard, reinsurance rejection)
- Regulatory & compliance risks (IRDAI licensing, mis-selling, data privacy)
- Fraud & operational risks (identity fraud, data manipulation, collusion)
- Platform dependency risks (API revocation, policy changes, competitive displacement)
- Market & unit economics risks (low willingness to pay, high CAC, churn)

**Key Recommendation:** Pivot to pure SaaS risk intelligence platform. Defer insurance until distribution, data moat, and regulatory clarity are established (18-24 months).

**Full analysis:** See `02-RED-TEAM-OUTPUT.md`

---

## Notes

- **GPT-5.2 Rule:** Must not debate early. Only judge + synthesize after all roles complete.
- **Conservative Approach:** Optimize for survivability, not hype.
- **MVP Focus:** Prefer solutions that can ship in 90 days.
- **India-First:** All regulatory analysis assumes India launch, globally extensible.

---

## Next Steps

1. Execute remaining role prompts (Actuary, Regulatory, Creator Economy)
2. Synthesize with Final Judge (GPT-5.2)
3. Review final output for investor-grade concept
4. Iterate if needed based on synthesis
