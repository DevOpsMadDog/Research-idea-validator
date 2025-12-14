"""
Configuration for the Financial Product Evaluation Debate System.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class VerdictType(Enum):
    APPROVE = "✅ APPROVE — Build Now"
    CONDITIONAL = "⚠️ CONDITIONAL — Needs Major Pivot"
    REJECT = "❌ REJECT — Not Venture-Scale"


class CategoryType(Enum):
    NEW_CATEGORY = "New Financial Product Category"
    TECH_ADVISORY = "Tech-Enabled Advisory / Family Office"
    PREMIUM_REPACKAGING = "Premium Repackaging"
    NOT_A_BUSINESS = "Interesting Idea, Not a Business"


class RiskType(Enum):
    REGULATORY = "Regulatory"
    BEHAVIORAL = "Behavioral"
    STRUCTURAL = "Structural"
    DISTRIBUTION = "Distribution"
    TRUST = "Trust"


@dataclass
class FinancialProductIdea:
    """Represents a financial product idea to be evaluated."""
    
    name: str
    description: str
    problem_statement: str
    solution_buckets: List[str]
    key_features: List[str]
    target_users: List[str]
    revenue_model: str
    differentiators: List[str]
    
    def to_prompt_context(self) -> str:
        """Convert the idea to a formatted prompt context."""
        return f"""
IDEA UNDER EVALUATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Concept Name: {self.name}

Description:
{self.description}

Problem Statement:
{self.problem_statement}

Solution Buckets:
{chr(10).join(f"  • {bucket}" for bucket in self.solution_buckets)}

Key Features:
{chr(10).join(f"  • {feature}" for feature in self.key_features)}

Target Users:
{chr(10).join(f"  • {user}" for user in self.target_users)}

Revenue Model:
{self.revenue_model}

Key Differentiators:
{chr(10).join(f"  • {diff}" for diff in self.differentiators)}
"""


# Default Product Idea: Money Operating System / Capital OS (India)
DEFAULT_PRODUCT_IDEA = FinancialProductIdea(
    name="Money Operating System / Capital OS (India)",
    description="""India has many mutual funds, PMS, AIFs, and curated platforms (Scriptbox, Kuvera, banks, brokers).
What is missing is a system that manages money as a whole, not products.

This system optimizes cash-flow timing, not just CAGR. It allocates capital across dynamic buckets,
is tax-first (optimizing post-tax outcomes), is cycle-aware (adjusting exposure based on liquidity 
and credit cycles), engineers exits (not just entries), can hold cash intentionally, and sells 
advice + system — not financial products.""",
    
    problem_statement="No system in India manages money holistically across liquidity, growth, and optionality — existing platforms focus on products, not capital optimization.",
    
    solution_buckets=[
        "Survival (liquidity)",
        "Opportunity (dry powder)",
        "Growth (equity)",
        "Yield (income)",
        "Optionality (asymmetric bets)"
    ],
    
    key_features=[
        "Optimizes cash-flow timing, not just CAGR",
        "Tax-first optimization for post-tax outcomes",
        "Cycle-aware exposure adjustment",
        "Exit engineering, not just entry planning",
        "Intentional cash holding capability",
        "Advice + system model, not product distribution"
    ],
    
    target_users=[
        "Indian HNIs",
        "Business owners",
        "Senior professionals",
        "NRIs"
    ],
    
    revenue_model="Subscription + advisory / performance fee. No product distribution commissions.",
    
    differentiators=[
        "Manages money as a whole, not products",
        "Dynamic bucket allocation based on life stage and cycles",
        "Post-tax optimization as primary goal",
        "Conflict-free model (no distribution commissions)",
        "Cash is treated as a legitimate allocation"
    ]
)


@dataclass
class AgentConfig:
    """Configuration for a debate agent."""
    
    agent_id: int
    name: str
    role: str
    persona: str
    evaluation_criteria: List[str]
    adversarial_goal: str
    is_judge: bool = False


# Agent Configurations
AGENT_CONFIGS = [
    AgentConfig(
        agent_id=1,
        name="Skeptical VC (India Focus)",
        role="Tier-1 Indian VC Partner",
        persona="Experienced VC with portfolio pressure and opportunity cost awareness. Seen many pitches fail.",
        evaluation_criteria=[
            "TAM realism",
            "Scalability",
            "Defensibility",
            "Sales cycle",
            "Exit potential"
        ],
        adversarial_goal="Kill the idea if possible — find the fatal flaws that founders are blind to."
    ),
    AgentConfig(
        agent_id=2,
        name="SEBI & Regulatory Expert",
        role="Deep expertise in Indian financial regulation",
        persona="Former regulator or compliance head. Paranoid about regulatory risk. Has seen startups shut down.",
        evaluation_criteria=[
            "RIA vs PMS vs AIF vs advisory classification",
            "Fee legality under current frameworks",
            "Conflict of interest exposure",
            "Risk of regulatory shutdown",
            "Scalability under compliance burden"
        ],
        adversarial_goal="Assume worst-case SEBI scrutiny — identify all regulatory landmines."
    ),
    AgentConfig(
        agent_id=3,
        name="Behavioral Finance & Indian Psychology Expert",
        role="Expert in how Indians actually behave with money",
        persona="Behavioral economist who has studied Indian saving/investing patterns. Cynical about stated preferences.",
        evaluation_criteria=[
            "Trust barriers",
            "Willingness to pay for advice",
            "Override risk (will users follow recommendations?)",
            "'Sounds good, won't follow' problems",
            "RM / bank relationship inertia"
        ],
        adversarial_goal="Be cynical and realistic — expose the gap between what people say and what they do."
    ),
    AgentConfig(
        agent_id=4,
        name="Execution & Ops Realist (Ex-Fintech Operator)",
        role="Built and scaled fintech products in India",
        persona="Ex-operator who has seen the gap between vision and execution. Knows the pain of scaling in India.",
        evaluation_criteria=[
            "Operational complexity",
            "Cost structure",
            "Hiring needs and talent availability",
            "Time to first revenue",
            "Support & compliance overhead"
        ],
        adversarial_goal="Assume limited founder bandwidth — expose hidden operational complexity."
    ),
    AgentConfig(
        agent_id=5,
        name="Bull Case Architect",
        role="Believe this idea could work",
        persona="Thoughtful optimist who sees category-creating potential. Not a cheerleader — a rigorous defender.",
        evaluation_criteria=[
            "Why this is a new category",
            "Why incumbents cannot copy easily",
            "Best wedge use-case",
            "Pricing power",
            "Long-term moat"
        ],
        adversarial_goal="Defend rigorously — build the strongest possible case without hype or wishful thinking."
    ),
    AgentConfig(
        agent_id=6,
        name="FINAL JUDGE (Chief Investment Committee Chair)",
        role="Meta-evaluator and decision maker",
        persona="Experienced IC chair. Does not debate. Decides based on evidence only. Has killed good-sounding ideas.",
        evaluation_criteria=[
            "Cross-agent conflict resolution",
            "Evidence quality assessment",
            "Risk-adjusted potential",
            "Category classification",
            "Final verdict determination"
        ],
        adversarial_goal="Synthesize all perspectives. Make a clear decision. A correct rejection is a success.",
        is_judge=True
    )
]


@dataclass
class JudgeScoring:
    """Scoring dimensions for the final judge."""
    
    market_pain: int = 0  # 0-10: Is this a real, urgent problem in India?
    differentiation: int = 0  # 0-10: Can incumbents copy this easily?
    regulatory_safety: int = 0  # 0-10: Can this scale without SEBI intervention?
    execution_feasibility: int = 0  # 0-10: Can a small team launch in ≤18 months?
    wealth_potential: int = 0  # 0-10: Can this reach ₹100–500 Cr ARR?
    
    market_pain_justification: str = ""
    differentiation_justification: str = ""
    regulatory_safety_justification: str = ""
    execution_feasibility_justification: str = ""
    wealth_potential_justification: str = ""
    
    def total_score(self) -> int:
        return (
            self.market_pain + 
            self.differentiation + 
            self.regulatory_safety + 
            self.execution_feasibility + 
            self.wealth_potential
        )
    
    def average_score(self) -> float:
        return self.total_score() / 5
