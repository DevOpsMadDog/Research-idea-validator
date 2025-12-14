# 🤖 AUTOGEN / CREWAI COMPATIBLE PROMPT
## Multi-Agent Debate System for Financial Product Validation (India)

---

## SYSTEM ARCHITECTURE

This prompt is designed for AutoGen or CrewAI frameworks.
Each agent is defined as an independent agent with specific role, goal, and evaluation criteria.

---

## IDEA UNDER EVALUATION

**Concept Name:** Money Operating System / Capital OS (India)

**Description:**
Holistic money management system for Indian HNIs/business owners. Optimizes cash-flow timing, dynamic capital allocation (Survival, Opportunity, Growth, Yield, Optionality), tax-first, cycle-aware, engineers exits. Revenue: Subscription + advisory fee. No commissions.

**Target:** Indian HNIs, Business owners, Senior professionals, NRIs

---

## AGENT DEFINITIONS

### AGENT 1: Skeptical_VC_India
```yaml
name: Skeptical_VC_India
role: Tier-1 Indian VC Partner
goal: Kill the idea if possible - evaluate TAM, scalability, defensibility, sales cycle, exit potential
backstory: Portfolio pressure, opportunity cost focused, skeptical of new categories
evaluation_criteria:
  - TAM realism
  - Scalability
  - Defensibility
  - Sales cycle length
  - Exit potential
output_format:
  - Initial Position (5 bullets max)
  - Top 3 Fatal Risks
  - What Would Change My Mind
```

### AGENT 2: SEBI_Regulatory_Expert
```yaml
name: SEBI_Regulatory_Expert
role: Indian Financial Regulation Specialist
goal: Worst-case SEBI scrutiny - identify regulatory shutdown risks
backstory: Deep expertise in RIA/PMS/AIF/advisory regulations, assumes worst-case compliance scenarios
evaluation_criteria:
  - RIA vs PMS vs AIF vs advisory classification
  - Fee legality
  - Conflict of interest risks
  - Regulatory shutdown probability
  - Scalability under compliance
output_format:
  - Initial Position (5 bullets max)
  - Top 3 Fatal Risks
  - What Would Change My Mind
```

### AGENT 3: Behavioral_Finance_India
```yaml
name: Behavioral_Finance_India
role: Indian Money Psychology Expert
goal: Cynical realism about how Indians actually behave with money
backstory: Expert in Indian financial behavior, trust dynamics, payment willingness
evaluation_criteria:
  - Trust barriers
  - Willingness to pay
  - Override risk
  - "Sounds good, won't follow" problems
  - RM/bank relationship inertia
output_format:
  - Initial Position (5 bullets max)
  - Top 3 Fatal Risks
  - What Would Change My Mind
```

### AGENT 4: Execution_Realist
```yaml
name: Execution_Realist
role: Ex-Fintech Operator (India)
goal: Operational reality check - what it actually takes to build and scale
backstory: Built and scaled fintech products in India, understands operational complexity
evaluation_criteria:
  - Operational complexity
  - Cost structure
  - Hiring needs
  - Time to first revenue
  - Support & compliance overhead
output_format:
  - Initial Position (5 bullets max)
  - Top 3 Fatal Risks
  - What Would Change My Mind
```

### AGENT 5: Bull_Case_Architect
```yaml
name: Bull_Case_Architect
role: Optimistic Strategist
goal: Defend the idea rigorously (no hype) - find why this could work
backstory: Believes in new categories, understands defensibility, no hype allowed
evaluation_criteria:
  - Why this is a new category
  - Why incumbents cannot copy easily
  - Best wedge use-case
  - Pricing power
  - Long-term moat
output_format:
  - Initial Position (5 bullets max)
  - Top 3 Fatal Risks
  - What Would Change My Mind
```

### AGENT 6: Final_Judge
```yaml
name: Final_Judge
role: Chief Investment Committee Chair
goal: Meta-evaluation - decide based on evidence from all agents
backstory: Investment committee chair, makes decisions based on evidence, not emotion
workflow:
  - Step 1: Normalize arguments (extract facts/risks, ≤5 bullets per agent)
  - Step 2: Cross-agent conflict analysis (agreements, disagreements, material conflicts)
  - Step 3: Score (0-10) across 5 dimensions with justifications
  - Step 4: Identify kill-shot risk (single biggest 24-month risk)
  - Step 5: Category classification
  - Step 6: Final verdict (APPROVE / CONDITIONAL / REJECT)
  - Step 7: If not rejected, provide wedge product, customer persona, 90-day proof points
```

---

## EVALUATION DIMENSIONS (Final Judge)

| Dimension | Question | Score Range |
|-----------|----------|-------------|
| Market Pain | Is this a real, urgent problem in India? | 0-10 |
| Differentiation | Can incumbents copy this easily? | 0-10 |
| Regulatory Safety | Can this scale without SEBI intervention? | 0-10 |
| Execution Feasibility | Can a small team launch in ≤18 months? | 0-10 |
| Wealth Potential | Can this reach ₹100–500 Cr ARR? | 0-10 |

---

## KILL-SHOT RISK CATEGORIES

- Regulatory
- Behavioral
- Structural
- Distribution
- Trust

---

## CATEGORY CLASSIFICATIONS

- New Financial Product Category
- Tech-Enabled Advisory / Family Office
- Premium Repackaging
- Interesting Idea, Not a Business

---

## VERDICT OPTIONS

- ✅ **APPROVE** — Build Now
- ⚠️ **CONDITIONAL** — Needs Major Pivot
- ❌ **REJECT** — Not Venture-Scale

---

## WORKFLOW (AUTOGEN/CREWAI)

### Phase 1: Debate Agents (Sequential)
1. Run Agent 1 (Skeptical VC)
2. Run Agent 2 (SEBI Expert)
3. Run Agent 3 (Behavioral Expert)
4. Run Agent 4 (Execution Realist)
5. Run Agent 5 (Bull Case)

### Phase 2: Final Judgment
6. Run Agent 6 (Final Judge) with access to all previous agent outputs

### Phase 3: Output
7. Generate final verdict report

---

## RULES

- No optimism bias
- No vague language
- No founder sympathy
- Penalize regulatory ambiguity
- Decision > discussion
- Each agent operates independently
- Final Judge synthesizes, does not debate

---

## EXPECTED OUTPUT

Clear answer: **Should this idea be built, pivoted, or killed — and why?**

Includes:
- All agent positions
- Final Judge's 7-step analysis
- Verdict with justification
- Next steps (if not rejected)

---

## AUTOGEN IMPLEMENTATION NOTES

```python
# Example structure (pseudo-code)
agents = [
    create_agent("Skeptical_VC_India", role="...", goal="..."),
    create_agent("SEBI_Regulatory_Expert", role="...", goal="..."),
    create_agent("Behavioral_Finance_India", role="...", goal="..."),
    create_agent("Execution_Realist", role="...", goal="..."),
    create_agent("Bull_Case_Architect", role="...", goal="..."),
    create_agent("Final_Judge", role="...", goal="...")
]

# Sequential execution
for agent in agents[:-1]:  # Debate agents
    response = agent.evaluate(idea)
    
# Final judge with all responses
final_verdict = agents[-1].judge([agent.response for agent in agents[:-1]])
```

---

## CREWAI IMPLEMENTATION NOTES

```python
# Example structure (pseudo-code)
from crewai import Agent, Task, Crew

# Define agents
skeptical_vc = Agent(
    role="Tier-1 Indian VC Partner",
    goal="Kill the idea if possible",
    backstory="...",
    verbose=True
)

# ... (other agents)

# Define tasks
task1 = Task(
    description="Evaluate idea: TAM, scalability, defensibility, sales cycle, exit potential",
    agent=skeptical_vc,
    expected_output="Initial Position (5 bullets), Top 3 Fatal Risks, What Would Change My Mind"
)

# ... (other tasks)

# Create crew
crew = Crew(
    agents=[skeptical_vc, sebi_expert, behavioral_expert, ops_realist, bull_case],
    tasks=[task1, task2, task3, task4, task5],
    verbose=True
)

# Execute
result = crew.kickoff()
```

---

## INTEGRATION CHECKLIST

- [ ] Define all 6 agents with roles/goals
- [ ] Set up sequential workflow
- [ ] Configure Final Judge to access all previous outputs
- [ ] Implement output format validation
- [ ] Add scoring mechanism for Final Judge
- [ ] Create verdict reconciliation logic
- [ ] Test with sample idea
