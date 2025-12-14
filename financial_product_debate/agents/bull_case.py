"""
Agent 5: Bull Case Architect
"""

from .base_agent import BaseAgent, AgentResponse
from ..config import AgentConfig, FinancialProductIdea, AGENT_CONFIGS


class BullCaseAgent(BaseAgent):
    """
    Believe this idea could work.
    Goal: Defend rigorously — no hype.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[4])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate with a constructive but rigorous perspective."""
        
        initial_position = [
            "THIS IS A NEW CATEGORY, NOT A BETTER PRODUCT: India has product distributors (MFDs), asset managers (AMCs, PMS), and relationship managers (private banks). No one owns 'capital allocation intelligence'. The wedge is advice without product conflict — this is genuinely differentiated.",
            "INCUMBENTS CANNOT COPY EASILY: Banks earn ₹2-4% distribution income; switching to fee-only cannibalizes their core revenue. PMS/AIFs are product manufacturers, not advisors. Family offices are high-cost and don't scale. Structural incentive misalignment protects the moat.",
            "THE ₹25L-₹5CR SEGMENT IS UNDERSERVED: Too rich for robo-advisors, too small for family offices. This 'mass affluent+' segment (~2-3M households) has no good option today. Banks give them junior RMs; MFDs give them commission products; they deserve better.",
            "TIMING IS RIGHT: Account Aggregator (AA) framework reduces data integration cost by 70%. SEBI's conflict-of-interest focus legitimizes fee-only models. Post-COVID digital adoption by HNIs is 3x higher. The infrastructure and behavior shifts now support this model.",
            "PRICING POWER IS REAL: If you save a ₹5 Cr client ₹10-15L annually in taxes, fees, and behavioral mistakes, they will pay ₹2-3L happily. The value gap is 5-10x the fee. This is not a 'nice to have' — it's quantifiable ROI."
        ]
        
        fatal_risks = [
            "CATEGORY CREATION REQUIRES PATIENCE: New categories take 5-7 years to mature. Investors expecting 3-year exits will be disappointed. This needs patient capital (family offices, strategic investors) not traditional VCs with 5-year fund cycles.",
            "FOUNDER-MARKET FIT IS CRITICAL: This only works if founders have deep wealth management credibility AND tech/product capability. The intersection is rare. Without it, HNI trust won't transfer and tech will be mediocre.",
            "BEHAVIORAL CHANGE IS THE REAL PRODUCT: You're not selling software; you're selling discipline. The hardest part is getting clients to follow the system through drawdowns. Without behavioral lock-in mechanisms, outcomes will disappoint."
        ]
        
        change_conditions = [
            "I would become more skeptical if: early clients show <70% advice adherence rates — this means the behavioral product isn't working.",
            "I would become more skeptical if: incumbents launch fee-only divisions with serious investment (not just PR) — this erodes differentiation.",
            "I would become more skeptical if: RIA regulations become so burdensome that compliance costs exceed 20% of revenue — this destroys unit economics."
        ]
        
        raw_analysis = f"""
BULL CASE DEEP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluating: {product.name}

WHY THIS IS A NEW CATEGORY:

Current Market Structure:
┌─────────────────────────────────────────────────────────────┐
│  PRODUCT MANUFACTURERS  │  DISTRIBUTORS  │  ADVISORS        │
├─────────────────────────────────────────────────────────────┤
│  AMCs (MF)              │  MFDs          │  RIAs (<500)     │
│  PMS Managers           │  Banks         │  Family Offices  │
│  AIFs                   │  Brokers       │  CAs (informal)  │
│  Insurance Cos          │  Fintechs      │                  │
└─────────────────────────────────────────────────────────────┘

What's Missing:
• Product manufacturers optimize for AUM, not client outcomes
• Distributors optimize for commissions, not allocation
• RIAs are subscale and fragmented
• Family offices are ₹50L+/year, not accessible

THE GAP: "Capital Allocation Intelligence as a Service"
• Product-agnostic
• Fee-only
• Tech-enabled
• Accessible to ₹1-10 Cr segment

WHY INCUMBENTS CANNOT COPY:

1. Banks (HDFC, ICICI, Kotak Private):
   • Distribution income: ₹5,000-15,000 Cr annually
   • Switching to fee-only = 80% revenue destruction
   • Board/shareholder pressure prevents this
   • Incentive structure misaligned at RM level too

2. Wealth Platforms (Scripbox, Kuvera, Groww):
   • Business model: MF distribution commission
   • Pivoting to advice = different skillset + licensing
   • They optimize for volume, not depth
   • HNI service quality would suffer

3. PMS/AIF Managers (Marcellus, Alchemy):
   • They ARE the product; can't be product-agnostic
   • No incentive to recommend competitor products
   • ₹50L minimum excludes mass affluent

4. Family Offices (Waterfield, IIFL One):
   • Cost structure: ₹50L-1Cr/year minimum
   • Not accessible to ₹1-5 Cr segment
   • Talent model doesn't scale

STRUCTURAL MOAT:
"You cannot compete with someone whose income depends on 
doing the thing you're trying to stop."

WHY THE TIMING IS NOW:

1. Account Aggregator (AA) Revolution
   • Launched 2021, gaining adoption
   • Reduces data aggregation cost from ₹50K to ₹5K per client
   • Enables 'consolidated view' without manual data entry
   • Critical infrastructure unlock

2. SEBI Regulatory Tailwinds
   • 2020: Stricter disclosure norms for distributors
   • 2022: True-to-label regulations
   • 2023: Enhanced conflict-of-interest requirements
   • Direction is clear: transparency + client protection

3. Behavioral Shift Post-COVID
   • HNI digital comfort increased dramatically
   • Willingness to engage remotely proven
   • Video-first advisory is now accepted
   • Reduces geographic constraints

4. Market Volatility Creates Demand
   • 2020 crash exposed bad advice
   • 2021-22 crypto mania showed behavioral risks
   • 2023 small/mid bubble creating anxiety
   • Clients are questioning their current setup

BEST WEDGE USE-CASE:

Primary Wedge: "TAX-FIRST PORTFOLIO REVIEW"
• Offer free/low-cost tax analysis of current portfolio
• Show client they're leaking ₹3-10L annually
• Quantifiable, immediate value
• Natural upsell to full service
• CAC: ₹10-20K
• Conversion to paid: 15-25%

Secondary Wedge: "EXECUTIVE LIQUIDITY EVENT"
• Target executives with ESOPs/RSUs vesting
• Help them navigate 30% tax + 10% STCG
• High-intent, time-sensitive moment
• ₹50L-2Cr average ticket
• Naturally converts to ongoing relationship

PRICING POWER ANALYSIS:

Value Creation per ₹5 Cr Client:
├── Tax optimization: ₹5-10L/year
├── Fee reduction (MF→direct): ₹1-2L/year
├── Behavioral alpha: ₹5-10L/year (conservative)
├── Time savings: ₹1-2L/year (implicit)
└── TOTAL VALUE: ₹12-24L/year

Fee Charged: ₹2-3L/year
Value/Fee Ratio: 5-10x
Willingness to Pay: HIGH (when demonstrated)

LONG-TERM MOAT EVOLUTION:

Year 1-3: Trust Moat
• Founder credibility
• Early client outcomes
• Referral network

Year 3-5: Data Moat
• Portfolio patterns across clients
• Tax optimization playbooks
• Behavioral intervention library

Year 5-7: Network Moat
• Client community
• Professional network (CAs, lawyers)
• Talent pipeline

Year 7+: Brand Moat
• 'Default choice' for segment
• Pricing power
• Acquisition target for banks

PATH TO ₹100 CR ARR:

Conservative Scenario:
• Year 3: 300 clients × ₹2L = ₹6 Cr
• Year 5: 800 clients × ₹2.5L = ₹20 Cr
• Year 7: 2,000 clients × ₹3L = ₹60 Cr
• Year 9: 4,000 clients × ₹3.5L = ₹140 Cr

This requires:
• 40% annual client growth
• 10% annual price increase
• 85% annual retention
• All achievable for category leader

VERDICT: This is a genuine category-creation opportunity. The structural barriers protecting the moat are real. The timing is right. The primary risk is execution and patience, not market or competition. Would recommend building, but with patient capital and realistic 7-10 year timeline.
"""
        
        return self._create_response(
            initial_position=initial_position,
            fatal_risks=fatal_risks,
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
