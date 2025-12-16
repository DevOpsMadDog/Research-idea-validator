# Multi-Agent Debate System: Creator Economy Risk Startup

This repository contains a structured multi-agent debate framework designed to create a risk-averse, investor-grade startup concept for de-risking the content creation economy.

## 🎯 Purpose

The system uses multiple AI agents with specific roles to rigorously test and refine a startup concept, ensuring it survives:
- Insurance underwriting scrutiny
- Regulatory compliance (India-first)
- Market validation
- Investor due diligence
- Red team attacks

## 📁 File Structure

- **`DEBATE_MASTER_PROMPT.md`** - Core truth constraints and system overview
- **`AGENT_PROMPTS.md`** - Detailed prompts for each agent role
- **`RED_TEAM_ANALYSIS.md`** - Completed Red Team/Skeptic analysis (Composer 1)
- **`FINAL_SYNTHESIS_TEMPLATE.md`** - Template for GPT-5.2 final synthesis
- **`README.md`** - This file

## 🔄 Execution Flow

### Step 1: Master Prompt
Read `DEBATE_MASTER_PROMPT.md` to understand core constraints.

### Step 2: Actuary/Insurance Agent (Opus 4.5)
Use the prompt from `AGENT_PROMPTS.md` (Section: STEP 2) with Opus 4.5.
**Output:** Underwriting memo defining insurable vs uninsurable risks.

### Step 3: Regulatory & Compliance (Gemini 3 Pro)
Use the prompt from `AGENT_PROMPTS.md` (Section: STEP 3) with Gemini 3 Pro.
**Output:** Compliance roadmap and legal structure recommendations.

### Step 4: Creator Economy Operator (Sonnet 4.5)
Use the prompt from `AGENT_PROMPTS.md` (Section: STEP 4) with Sonnet 4.5.
**Output:** Product strategy and creator segment analysis.

### Step 5: Red Team/Skeptic (Composer 1) ✅ COMPLETED
**See:** `RED_TEAM_ANALYSIS.md`
**Key Findings:**
- Insurance-first concept: **3/10 survivability** (FATAL FLAWS)
- Recommended pivot: SaaS-first (risk scoring + tools), add insurance later
- Pivoted concept: **7/10 survivability**

### Step 6: Final Judge & Curator (GPT-5.2)
Use the prompt from `AGENT_PROMPTS.md` (Section: STEP 6) with GPT-5.2.
**Input:** All outputs from Steps 2-5
**Output:** Complete investor-ready startup concept (use `FINAL_SYNTHESIS_TEMPLATE.md`)

## ⚠️ Critical Rules

1. **GPT-5.2 must NOT debate early** - It only synthesizes final output
2. **Each agent argues from assigned role only** - No role confusion
3. **Reject magical thinking** - All claims must be grounded in evidence
4. **Be conservative** - Optimize for survivability, not hype

## 🎯 Key Insights from Red Team Analysis

The Red Team identified **15+ critical failure modes**, including:

### Fatal Flaws (Cannot Be Fixed):
- **Correlation Risk:** Algorithm changes affect entire portfolio simultaneously
- **Adverse Selection:** Only risky creators buy → death spiral
- **Reinsurance Unavailability:** Reinsurers reject correlated, new risks

### High Risks (Manageable but Dangerous):
- **Regulatory Shutdown:** IRDAI may view as unlicensed insurance
- **Platform Dependency:** APIs can be revoked, platforms can compete
- **Unit Economics:** CAC > LTV likely

### Recommended Pivot:
**SaaS-First Approach:**
- Start with risk scoring + de-risking tools (no insurance)
- Build data moat and prove unit economics
- Add insurance only after 24 months with:
  - Proven risk models
  - Behavior controls
  - Regulatory relationships
  - Capital raised (₹50-100 crores)

## 📊 Expected Outputs

### From Each Agent:
- **Actuary:** 2,000-3,000 word underwriting memo
- **Regulatory:** 2,000-3,000 word compliance roadmap
- **Creator Operator:** 2,000-3,000 word product strategy
- **Red Team:** 2,000-3,000 word failure mode analysis ✅
- **Final Judge:** 5,000-7,000 word investor-ready concept

### Final Synthesis Must Include:
1. One-line thesis
2. Problem & why now
3. Product (MVP → V2 → V3)
4. Creator Risk Scoring Model
5. De-risking Controls (non-insurance)
6. Insurance Design (parametric only)
7. Risk Distribution & Reinsurance Logic
8. Business Model & Unit Economics
9. Go-To-Market Strategy
10. Regulatory Strategy (India-first)
11. Moat & Defensibility
12. 90-Day Execution Plan
13. Risk Register (15+ risks + mitigations)
14. Investor attractiveness score (0-10) + explanation

## 🚀 Next Steps

1. **Execute Steps 2-4** with respective AI models (Opus 4.5, Gemini 3 Pro, Sonnet 4.5)
2. **Review Red Team Analysis** (`RED_TEAM_ANALYSIS.md`) - Already completed
3. **Execute Step 6** with GPT-5.2, incorporating all previous outputs
4. **Refine** based on final synthesis

## 💡 Pro Tips

- **If investors are your goal:** Let GPT-5.2 recommend SaaS-first approach
- **Lower regulation risk:** Start without insurance, add later
- **Faster revenue:** SaaS subscriptions vs. insurance premiums
- **Higher survivability:** Prove model before adding insurance complexity

## 📝 Notes

- All prompts are designed to be copy-pasted directly into respective AI models
- Each agent should work independently (no cross-contamination)
- Final judge (GPT-5.2) synthesizes all inputs into single coherent concept
- System automatically pushes ideas into safer shape through rigorous debate

---

**Status:** Red Team analysis complete. Ready for Steps 2-4 and final synthesis.
