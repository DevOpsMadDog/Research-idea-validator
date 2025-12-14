# Multi-Agent Debate System for Financial Product Validation

Complete prompt system for evaluating financial product ideas using multi-agent debate + final judge.

---

## 📁 Files Overview

### 1. `multi-agent-debate-prompt.md` ⭐ **START HERE**
**The original, full-featured prompt**
- Complete 6-agent system (5 debate agents + 1 final judge)
- Detailed instructions for each agent
- 7-step final judge evaluation process
- Ready to paste into Cursor.ai

**Use when:** You want the full, comprehensive evaluation system

---

### 2. `multi-agent-debate-prompt-compressed.md`
**Condensed version for quick use**
- Same structure, less verbose
- Faster to read and execute
- All essential components preserved

**Use when:** You need a quicker evaluation or have token limits

---

### 3. `multi-agent-debate-prompt-with-shortseller.md`
**Enhanced version with dual-judge system**
- Adds a 7th agent: Short-Seller / Contrarian Analyst
- Two independent judges evaluate separately
- Reconciliation process if judges disagree
- Catches fatal flaws others might miss

**Use when:** You want maximum rigor and adversarial analysis

---

### 4. `multi-agent-debate-prompt-autogen-crewai.md`
**Framework-compatible version**
- Structured for AutoGen or CrewAI integration
- YAML-style agent definitions
- Pseudo-code examples for implementation
- Integration checklist included

**Use when:** You're building an automated multi-agent system

---

### 5. `multi-agent-debate-prompt-build-roadmap.md`
**Post-evaluation roadmap generator**
- Converts verdict into actionable build plan
- Handles APPROVE, CONDITIONAL, and REJECT scenarios
- Phase-by-phase execution plan
- Risk mitigation checklists

**Use when:** You've completed the debate and need next steps

---

## 🚀 Quick Start

1. **Choose your prompt:**
   - Start with `multi-agent-debate-prompt.md` for full evaluation
   - Or use `compressed` version for speed

2. **Paste into Cursor.ai:**
   - Copy the entire contents of your chosen file
   - Paste into Cursor.ai chat
   - Let it run all agents sequentially

3. **Get verdict:**
   - Review all agent positions
   - See Final Judge's 7-step analysis
   - Get clear APPROVE / CONDITIONAL / REJECT decision

4. **Generate roadmap (optional):**
   - If approved/conditional, use `build-roadmap.md`
   - Paste the verdict into that prompt
   - Get detailed execution plan

---

## 🎯 Agent Roles

| Agent | Role | Goal |
|-------|------|------|
| 1. Skeptical VC | Tier-1 Indian VC Partner | Kill the idea if possible |
| 2. SEBI Expert | Financial Regulation Specialist | Worst-case regulatory scrutiny |
| 3. Behavioral Expert | Indian Money Psychology | Cynical realism about behavior |
| 4. Execution Realist | Ex-Fintech Operator | Operational reality check |
| 5. Bull Case | Optimistic Strategist | Defend rigorously (no hype) |
| 6. Final Judge | Investment Committee Chair | Meta-evaluation & verdict |

*(Version with short-seller adds Agent 7: Contrarian Analyst)*

---

## 📊 Evaluation Dimensions

Final Judge scores across 5 dimensions (0-10):
1. **Market Pain** - Is this a real, urgent problem?
2. **Differentiation** - Can incumbents copy easily?
3. **Regulatory Safety** - Can this scale without SEBI intervention?
4. **Execution Feasibility** - Can small team launch in ≤18 months?
5. **Wealth Potential** - Can this reach ₹100-500 Cr ARR?

---

## ✅ Verdict Options

- ✅ **APPROVE** — Build Now
- ⚠️ **CONDITIONAL** — Needs Major Pivot
- ❌ **REJECT** — Not Venture-Scale

---

## 🔧 Customization

To adapt for different ideas:
1. Replace the "IDEA UNDER EVALUATION" section
2. Adjust agent evaluation criteria if needed
3. Modify scoring dimensions for your domain
4. Update target metrics (e.g., ARR goals)

---

## 📝 Notes

- All prompts are self-contained (no external references)
- Designed for Indian financial products (can be adapted)
- Hard rules enforce rigor (no optimism bias)
- A correct rejection is considered a success

---

## 🤝 Next Steps

After running the debate:
- Use build roadmap generator for execution plan
- Integrate with AutoGen/CrewAI for automation
- Create regulatory compliance checklist
- Generate customer discovery interview guide

---

## 💡 Tips

- **For first-time use:** Start with the compressed version
- **For maximum rigor:** Use the short-seller version
- **For automation:** Use the AutoGen/CrewAI version
- **For execution:** Always generate a roadmap after approval

---

**Created for evaluating financial product ideas in India.**
**Adapt as needed for your specific use case.**
