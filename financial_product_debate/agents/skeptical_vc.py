"""
Agent 1: Skeptical VC (India Focus)
"""

from .base_agent import BaseAgent, AgentResponse
from ..config import AgentConfig, FinancialProductIdea, AGENT_CONFIGS


class SkepticalVCAgent(BaseAgent):
    """
    Tier-1 Indian VC partner with portfolio pressure and opportunity cost awareness.
    Goal: Kill the idea if possible.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[0])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate from a skeptical VC perspective."""
        
        # Skeptical VC Analysis
        initial_position = [
            "TAM is theoretically large (Indian HNIs ~3-4M households) but addressable market for paid advisory is <500K, and willingness to pay for 'system' vs 'product' is unproven.",
            "This is a services business masquerading as a tech platform — CAC will be high, LTV will leak to relationship managers, and margins will compress under competition.",
            "No clear moat: the 'bucket allocation' framework can be replicated by any wealth manager in 6 months; incumbents (IIFL, 360 One, Waterfield) have distribution and trust.",
            "Sales cycle for HNIs is 3-6 months minimum, requires white-glove onboarding, and scales linearly with headcount — this is not a venture-scale business.",
            "Exit potential is weak: acquirers want AUM or distribution, not advisory revenue; strategic value is limited without product manufacturing capability."
        ]
        
        fatal_risks = [
            "UNIT ECONOMICS TRAP: High-touch advisory for HNIs requires expensive RMs (₹25-50L/year), limiting gross margins to 40-50%. With ₹2-3L annual subscription per client, you need 500+ clients just to break even on a 10-person team. This is a lifestyle business, not venture-scale.",
            "DISTRIBUTION DEATH: Indian HNIs trust their CA, banker, or family office. Breaking this trust takes 2-3 years per client. No viral loop, no referral engine, no scalable distribution. You'll burn ₹50-100 Cr building a 1000-client business.",
            "CATEGORY CONFUSION: 'Money OS' is too abstract for the market. HNIs buy products (PMS, AIF) or relationships (family office). A 'system' with no products is a hard sell — you'll spend 80% of sales time on education, not conversion."
        ]
        
        change_conditions = [
            "Show me 50 paying customers at ₹2L+ annual fee with <3 month sales cycle and >80% retention — this proves willingness to pay and product-market fit.",
            "Demonstrate a wedge product (tax optimization tool, liquidity dashboard) with self-serve adoption before layering advisory — this proves distribution.",
            "Prove you can hire and retain advisors at ₹10-15L/year (not ₹40L) who can deliver the same quality — this proves margin expansion potential.",
            "Show incumbents have structural reasons they cannot copy this (regulatory, tech debt, incentive misalignment) — not just 'they haven't done it yet'."
        ]
        
        raw_analysis = f"""
SKEPTICAL VC DEEP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluating: {product.name}

TAM ASSESSMENT:
• Indian HNI households (>₹5 Cr investable): ~3-4 million
• Actually addressable (digitally savvy, open to new platforms): ~500K
• Willing to pay subscription (not commission): ~50-100K
• Realistic serviceable market in Year 1-3: 2,000-5,000 clients
• This is a ₹50-100 Cr revenue ceiling, not ₹500 Cr

SCALABILITY CONCERNS:
• Advisory is inherently high-touch
• Each RM can handle 30-50 HNI relationships max
• Tech can automate reporting but not relationship
• Scaling means hiring, not software leverage

DEFENSIBILITY GAPS:
• Framework is replicable in 6 months
• No proprietary data advantage
• No network effects
• No switching costs (client can take strategy elsewhere)
• Incumbents have trust + distribution + products

SALES CYCLE REALITY:
• HNI decision cycles: 3-6 months
• Requires multiple meetings, spouse involvement
• High onboarding complexity (multiple accounts, tax docs)
• Each sale costs ₹50-100K in fully-loaded RM time

EXIT SCENARIOS:
• IPO: Unlikely at <₹500 Cr ARR, which will take 10+ years
• Strategic acquisition: Wealth managers want AUM, not advisory
• PE rollup: Possible at 5-7x revenue, but that's ₹50-100 Cr exit
• This is a ₹100-200 Cr exit at best, not venture-scale

VC MATH:
• Need 10x return for Series A check
• If I write ₹20 Cr check at ₹80 Cr valuation
• Need ₹800 Cr exit for 10x
• Revenue multiple for advisory: 3-5x
• Need ₹160-270 Cr ARR at exit
• Time to reach: 8-10 years if everything works
• IRR: <20% — below threshold

VERDICT: This is a great business for a founder who wants to build a ₹50-100 Cr revenue lifestyle business over 10 years. It is NOT a venture-scale opportunity. Would pass.
"""
        
        return self._create_response(
            initial_position=initial_position,
            fatal_risks=fatal_risks,
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
