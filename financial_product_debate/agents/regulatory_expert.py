"""
Agent 2: SEBI & Regulatory Expert
"""

from .base_agent import BaseAgent, AgentResponse
from ..config import AgentConfig, FinancialProductIdea, AGENT_CONFIGS


class RegulatoryExpertAgent(BaseAgent):
    """
    Deep expertise in Indian financial regulation.
    Goal: Assume worst-case SEBI scrutiny.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[1])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate from a regulatory perspective."""
        
        initial_position = [
            "The 'advisory + system' model sits in regulatory grey zone: if you recommend specific securities or allocation percentages, you need RIA registration under SEBI (Investment Advisers) Regulations, 2013.",
            "Fee structure is constrained: RIAs cannot charge performance fees (only fixed/AUM-based); if you want performance fees, you need PMS license (₹50L min ticket, ₹2 Cr net worth requirement for manager).",
            "The 'no product distribution' claim is clean but limits scale: you cannot earn trail commissions, and clients may leak to execution platforms that offer convenience.",
            "SEBI's proposed RIA amendments (2023-24) increase compliance burden: mandatory audit, net worth requirements (₹50L for individuals, ₹1 Cr for corporates), and stricter client suitability norms.",
            "Cross-selling risk: if you later add insurance or loans to the 'OS', you enter IRDAI/RBI jurisdiction — multi-regulator compliance is expensive and slow."
        ]
        
        fatal_risks = [
            "RIA REGISTRATION BOTTLENECK: SEBI RIA registration requires NISM certifications, net worth compliance, and ongoing regulatory filings. More critically, RIAs are personally liable for unsuitable advice. If one client loses money and complains, SEBI can suspend your registration — killing the business overnight. The 2022 Karvy/DHFL cases have made SEBI extremely aggressive.",
            "PERFORMANCE FEE ILLEGALITY: The proposed model likely wants to charge performance fees ('advisory + performance fee'). Under current RIA regulations, performance-linked fees are prohibited for RIAs. You'd need PMS license, which has ₹50L minimum investment — excluding 80% of your target market. This is a structural dead-end.",
            "EXECUTION LEAKAGE & FRONT-RUNNING RISK: If you recommend but don't execute, clients will execute elsewhere. If you partner with execution platforms, you risk 'indirect commission' allegations. If you get discretionary rights, you need PMS license. There's no clean regulatory path that gives you both advice AND execution without heavy licensing."
        ]
        
        change_conditions = [
            "SEBI creates a new 'Financial Planning' license category (rumored but not implemented) that allows holistic advice with flexible fee structures.",
            "You partner with an existing PMS/AIF manager for execution, staying purely in the 'planning' layer — but this limits your value capture.",
            "You operate as a 'technology platform' providing tools (not advice), with clear disclaimers — but this dilutes the core value proposition.",
            "You structure as a multi-family office (MFO) for UHNI clients (>₹25 Cr), where regulatory flexibility is higher and clients can absorb compliance costs."
        ]
        
        raw_analysis = f"""
REGULATORY DEEP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluating: {product.name}

APPLICABLE REGULATIONS:
1. SEBI (Investment Advisers) Regulations, 2013 (as amended 2020)
2. SEBI (Portfolio Managers) Regulations, 2020
3. SEBI (Alternative Investment Funds) Regulations, 2012
4. SEBI (Research Analysts) Regulations, 2014
5. RBI Master Directions (if loans/credit involved)
6. IRDAI regulations (if insurance advice involved)

LICENSE ANALYSIS:

Option A: Register as RIA
• Pros: Can provide comprehensive financial advice
• Cons:
  - Cannot charge performance fees
  - Net worth requirement: ₹50L (individual), ₹1 Cr (corporate)
  - NISM certifications required for all advisers
  - Personal liability for unsuitable advice
  - Strict advertising restrictions
  - Annual compliance audit required
  - Cannot execute trades or hold client money

Option B: Register as PMS
• Pros: Can charge performance fees, discretionary management
• Cons:
  - ₹50L minimum client investment
  - ₹2 Cr net worth requirement
  - Custody and execution complexity
  - Excludes 80% of HNI market
  - Heavy operational requirements

Option C: Operate as Unregulated 'Fintech'
• Pros: Maximum flexibility
• Cons:
  - Cannot provide specific investment advice
  - Risk of SEBI action for unlicensed advice
  - 'Education' loophole is narrowing
  - Several startups have received show-cause notices

FEE STRUCTURE CONSTRAINTS:

RIA Fee Caps (Current):
• Fixed fee: No cap, but must be 'reasonable'
• AUM-based: 2.5% p.a. maximum
• Performance fee: PROHIBITED

PMS Fee Structure:
• Fixed fee: No regulatory cap
• Performance fee: Allowed (typically 10-20% over hurdle)
• But ₹50L minimum investment requirement

COMPLIANCE COST ESTIMATE:
• RIA registration: ₹2-3L (one-time)
• Annual compliance: ₹10-15L (audit, filings, systems)
• Legal/regulatory counsel: ₹5-10L/year
• Per-client suitability documentation: ₹5-10K/client
• Total: ₹20-30L/year fixed + ₹5-10K per client

REGULATORY RISK SCENARIOS:

Scenario 1: Client Complaint
• Single SAT (Securities Appellate Tribunal) case can cost ₹20-50L in legal fees
• SEBI can suspend registration pending investigation
• Reputational damage is severe in HNI circles

Scenario 2: SEBI Inspection
• Random inspections have increased post-2020
• Non-compliance findings lead to show-cause notices
• Even minor violations can result in warnings that scare clients

Scenario 3: Regulatory Change
• SEBI is actively tightening investment advice regulations
• 2023 consultation paper proposed stricter RIA norms
• Risk of stranded compliance investment if rules change

VERDICT: Regulatory path exists but is narrow and expensive. The fee structure constraint (no performance fees under RIA) fundamentally undermines the business model. Would need to either accept this constraint or target only UHNI segment with PMS/MFO structure.
"""
        
        return self._create_response(
            initial_position=initial_position,
            fatal_risks=fatal_risks,
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
