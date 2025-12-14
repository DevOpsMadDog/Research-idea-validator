# Multi-Agent Debate System for Financial Product Validation (India)

A structured multi-agent evaluation framework for rigorously assessing financial product ideas targeting the Indian market. This system simulates adversarial debate between specialized AI agents, culminating in a final judge arbitration.

## 🎯 Purpose

The goal is **not agreement, but truth**. This system:

- Runs independent, adversarial agent evaluations
- Surfaces fatal flaws before you invest time/money
- Exposes regulatory, behavioral, and execution risks
- Produces actionable verdicts: Build, Pivot, or Kill

## 🤖 Agents

| Agent | Role | Adversarial Goal |
|-------|------|-----------------|
| **Agent 1: Skeptical VC** | Tier-1 Indian VC Partner | Kill the idea if possible |
| **Agent 2: SEBI Expert** | Regulatory Deep Expert | Find all regulatory landmines |
| **Agent 3: Behavioral Expert** | Indian Money Psychology | Expose behavior-intention gaps |
| **Agent 4: Ops Realist** | Ex-Fintech Operator | Reveal hidden operational complexity |
| **Agent 5: Bull Case** | Rigorous Optimist | Build the strongest possible defense |
| **Agent 6: Final Judge** | IC Chair / Meta-Evaluator | Synthesize and decide based on evidence |

## 📁 Project Structure

```
financial_product_debate/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── config.py            # Configuration, product definition, scoring
├── orchestrator.py      # Debate orchestration logic
└── agents/
    ├── __init__.py
    ├── base_agent.py    # Base agent class
    ├── skeptical_vc.py  # Agent 1
    ├── regulatory_expert.py  # Agent 2
    ├── behavioral_expert.py  # Agent 3
    ├── execution_realist.py  # Agent 4
    ├── bull_case.py     # Agent 5
    └── final_judge.py   # Agent 6 (Final Arbiter)

run_debate.py            # Main execution script
```

## 🚀 Quick Start

### Run the Default Debate

```bash
# Run full evaluation
python run_debate.py

# Or use the module directly
python -m financial_product_debate

# Summary only
python -m financial_product_debate --summary

# Save to file
python -m financial_product_debate --output report.txt
```

### Run Programmatically

```python
from financial_product_debate.orchestrator import run_default_debate, run_custom_debate

# Run with default Money OS / Capital OS concept
result = run_default_debate()
print(result.format_full_output())

# Run with custom product
result = run_custom_debate(
    name="Your Product Name",
    description="What it does...",
    problem_statement="The problem being solved",
    solution_buckets=["Bucket 1", "Bucket 2"],
    key_features=["Feature 1", "Feature 2"],
    target_users=["Segment 1", "Segment 2"],
    revenue_model="How you make money",
    differentiators=["What makes you unique"]
)
```

## 📊 Output Format

### Agent Response Format

Each agent (1-5) responds with:
1. **Initial Position** (5 bullets max)
2. **Top 3 Fatal Risks**
3. **What Would Change My Mind**

### Final Judge Process

The Final Judge (Agent 6) performs:

| Step | Action |
|------|--------|
| 1 | Normalize arguments from all agents |
| 2 | Cross-agent conflict analysis |
| 3 | Score idea (0-10) on 5 dimensions |
| 4 | Identify kill-shot risk |
| 5 | Classify category |
| 6 | Render final verdict |
| 7 | Build recommendations (if not rejected) |

### Scoring Dimensions

| Dimension | Question |
|-----------|----------|
| Market Pain | Is this a real, urgent problem in India? |
| Differentiation | Can incumbents copy this easily? |
| Regulatory Safety | Can this scale without SEBI intervention? |
| Execution Feasibility | Can a small team launch in ≤18 months? |
| Wealth Potential | Can this reach ₹100–500 Cr ARR? |

### Verdict Options

- ✅ **APPROVE** — Build Now
- ⚠️ **CONDITIONAL** — Needs Major Pivot
- ❌ **REJECT** — Not Venture-Scale

## 🏦 Default Product: Money OS / Capital OS (India)

The default evaluation is for a "Money Operating System" concept:

**Problem:** India has many mutual funds, PMS, AIFs, and platforms — but no system manages money as a whole, not products.

**Solution:** A capital allocation system that:
- Optimizes cash-flow timing, not just CAGR
- Allocates across dynamic buckets (Survival, Opportunity, Growth, Yield, Optionality)
- Is tax-first, optimizing post-tax outcomes
- Is cycle-aware, adjusting for liquidity and credit cycles
- Engineers exits, not just entries
- Sells advice + system, not financial products

**Target:** Indian HNIs, business owners, senior professionals, NRIs

**Revenue:** Subscription + advisory fee (no distribution commissions)

## 📋 Hard Rules (Enforced)

- ❌ No optimism bias
- ❌ No vague language
- ❌ No founder sympathy
- ⚠️ Penalize regulatory ambiguity
- ✅ Decision > Discussion
- ✅ A correct rejection is a success

## 🔧 Customization

### Adding New Agents

1. Create a new file in `agents/`
2. Inherit from `BaseAgent`
3. Implement the `evaluate()` method
4. Add to `agents/__init__.py`
5. Include in `orchestrator.py`

### Modifying Scoring

Edit `config.py` to adjust:
- Scoring dimensions
- Verdict thresholds
- Category classifications
- Risk types

## 📝 Example Output

```
═══════════════════════════════════════════════════════════════════════════════
AGENT 1 — Skeptical VC (India Focus)
═══════════════════════════════════════════════════════════════════════════════

📌 INITIAL POSITION
────────────────────────────────────────
  1. TAM is theoretically large but addressable market for paid advisory is <500K
  2. This is a services business masquerading as a tech platform
  ...

⚠️  TOP 3 FATAL RISKS
────────────────────────────────────────
  1. UNIT ECONOMICS TRAP: High-touch advisory requires expensive RMs...
  2. DISTRIBUTION DEATH: Indian HNIs trust their CA, banker, or family office...
  3. CATEGORY CONFUSION: 'Money OS' is too abstract for the market...
```

## 🎯 Use Cases

1. **Pre-fundraise validation** — Test your pitch before investor meetings
2. **Pivot decisions** — Evaluate alternative directions
3. **Competitor analysis** — Assess competing concepts
4. **Team alignment** — Build shared understanding of risks
5. **Board preparation** — Anticipate tough questions

## 📄 License

MIT License - Use freely for evaluating financial product ideas.

---

*Built for rigorous, adversarial evaluation of financial products in the Indian market.*
