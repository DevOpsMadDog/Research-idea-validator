"""
Agent 4: Execution & Ops Realist (Ex-Fintech Operator)
"""

from .base_agent import BaseAgent, AgentResponse
from ..config import AgentConfig, FinancialProductIdea, AGENT_CONFIGS


class ExecutionRealistAgent(BaseAgent):
    """
    Built and scaled fintech products in India.
    Goal: Assume limited founder bandwidth — expose hidden complexity.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[3])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate from an execution and operations perspective."""
        
        initial_position = [
            "Onboarding complexity will kill early growth: each HNI client requires 15-20 hours of setup (KYC, account linking, document collection, goal discovery, tax history) — at 10 clients/month, you need 200 hours/month just for onboarding.",
            "Technology build is deceptively complex: 'bucket allocation' requires integration with 10+ account aggregators, real-time NAV feeds, tax lot tracking, and rebalancing logic — this is 18-24 months of engineering, not 6 months.",
            "Talent arbitrage is a myth: good wealth advisors in India cost ₹30-50L/year; junior advisors at ₹10-15L require 2-3 years of training before they can handle HNIs independently — there's no shortcut.",
            "Compliance operations are a hidden tax: RIA compliance requires per-client suitability documentation, annual risk profiling updates, trade rationale logging — this is 2-3 FTEs just for a 500-client book.",
            "Support burden scales linearly: HNI clients expect white-glove service; each client generates 50+ support interactions per year; at 500 clients, you need 5-7 FTEs just for client success."
        ]
        
        fatal_risks = [
            "INTEGRATION HELL: To deliver 'Money OS', you need to aggregate data from 15+ sources (banks, demat, MF platforms, insurance, property records, loan accounts). Each integration is 2-3 months. Account aggregators (AA framework) help but cover only 60% of sources. You'll spend 2 years just building the data layer, burning ₹2-3 Cr, before you can deliver the core value prop.",
            "ADVISOR UNIT ECONOMICS DEATH SPIRAL: Each senior advisor (₹40L cost) can handle 40-50 HNI relationships. At ₹2L/client revenue, that's ₹80-100L revenue per advisor. After advisor cost, you have ₹40-60L gross margin per advisor. Now add: tech (₹10L), compliance (₹5L), support (₹10L), office/infra (₹5L), management overhead (₹10L). You're left with ₹0-20L per advisor at scale. This is a 0-20% net margin business.",
            "TIME TO FIRST REVENUE IS 18+ MONTHS: You need: (1) RIA license (6-9 months), (2) Tech MVP (6-9 months), (3) First 10 clients (3-6 months), (4) Proof of retention (12 months). Investors will see zero revenue for 18 months, limited proof for 30 months. This is a hard fundraise story without serious founder credibility."
        ]
        
        change_conditions = [
            "Prove you can acquire first 50 clients with founder-only sales (no hired RMs) at <₹20K CAC — this proves organic demand.",
            "Demonstrate a 'productized' onboarding flow that reduces setup time to <5 hours per client — this proves operational leverage.",
            "Show a tech architecture that uses AA framework + open banking to achieve 80% data coverage without custom integrations.",
            "Build a junior advisor training program that gets advisors to 'independent' status in 12 months instead of 36 months.",
            "Partner with an existing RIA/family office for compliance infrastructure, focusing your build on the tech layer only."
        ]
        
        raw_analysis = f"""
EXECUTION & OPERATIONS DEEP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluating: {product.name}

OPERATIONAL COMPLEXITY MAP:

Layer 1: Client Onboarding
├── KYC & Documentation (3-5 hours)
│   ├── PAN verification
│   ├── Address proof
│   ├── Bank account verification
│   ├── Nominee details
│   └── Risk profiling questionnaire
├── Financial Discovery (5-8 hours)
│   ├── Asset inventory (all accounts)
│   ├── Liability mapping
│   ├── Income/expense analysis
│   ├── Tax situation review
│   ├── Goal articulation
│   └── Family structure mapping
├── Account Aggregation (2-3 hours)
│   ├── Bank account linking
│   ├── Demat account linking
│   ├── MF folio linking
│   ├── Insurance policy upload
│   └── Property document collection
└── Plan Creation (3-5 hours)
    ├── Current state analysis
    ├── Gap identification
    ├── Bucket allocation design
    └── Implementation roadmap

Total per client: 15-20 hours
At ₹2L/year revenue: ₹10-13K per hour of onboarding
If advisor costs ₹40L/year: ₹2K/hour fully loaded
Onboarding cost per client: ₹30-40K
PAYBACK PERIOD: 2-3 months of fees just for onboarding

Layer 2: Technology Stack Requirements

Must Build:
├── Account Aggregation Layer
│   ├── AA framework integration (Finvu, Onemoney, etc.)
│   ├── Demat account parsers (CDSL, NSDL)
│   ├── MF platform APIs (CAMS, Karvy, BSE)
│   ├── Insurance document OCR
│   └── Manual entry fallback UI
├── Portfolio Analytics Engine
│   ├── Multi-asset consolidation
│   ├── Real-time valuation
│   ├── Tax lot tracking (FIFO, specific lot)
│   ├── XIRR calculations
│   └── Benchmark comparisons
├── Planning & Allocation Module
│   ├── Goal-based planning logic
│   ├── Bucket allocation algorithm
│   ├── Rebalancing triggers
│   ├── Tax-loss harvesting
│   └── What-if scenarios
├── Client Dashboard
│   ├── Real-time net worth
│   ├── Bucket allocation view
│   ├── Performance tracking
│   ├── Document vault
│   └── Communication log
└── Advisor Dashboard
    ├── Client portfolio overview
    ├── Alert management
    ├── Compliance documentation
    ├── Recommendation tracker
    └── Revenue/pipeline management

Estimated Engineering:
• Backend: 3-4 senior engineers × 18 months = ₹1.5-2 Cr
• Frontend: 2 engineers × 18 months = ₹60-80L
• Data/Analytics: 1 engineer × 18 months = ₹30-40L
• DevOps/Infra: 1 engineer × 18 months = ₹30-40L
• QA: 1 engineer × 12 months = ₹20-25L
TOTAL TECH BUILD: ₹3-4 Cr over 18 months

Layer 3: Team Scaling Model

Year 1 Team (0-100 clients):
• Founders (CEO, CTO): 2
• Senior Advisor: 1 (₹40L)
• Junior Advisor: 1 (₹15L)
• Engineer: 3 (₹1.2 Cr)
• Ops/Compliance: 1 (₹15L)
• Client Support: 1 (₹8L)
Total payroll: ₹2 Cr/year
Revenue needed to break even: ₹2.5 Cr (125 clients at ₹2L)

Year 2 Team (100-300 clients):
• Management: 3 (founders + COO)
• Senior Advisors: 3 (₹1.2 Cr)
• Junior Advisors: 4 (₹60L)
• Engineering: 5 (₹2 Cr)
• Ops/Compliance: 3 (₹45L)
• Client Support: 4 (₹32L)
Total payroll: ₹5 Cr/year
Revenue needed: ₹6 Cr (300 clients at ₹2L)
Margin: 15-20%

Year 3 Team (300-500 clients):
• Management: 5
• Advisors: 10 (₹3.5 Cr)
• Engineering: 6 (₹2.5 Cr)
• Ops/Compliance: 5 (₹75L)
• Client Support: 6 (₹50L)
Total payroll: ₹8 Cr/year
Revenue needed: ₹10 Cr (500 clients at ₹2L)
Margin: 20-25%

CRITICAL PATH ANALYSIS:

Month 0-6: Foundation
• RIA application filed
• Core team hired (4-5 people)
• Tech architecture finalized
• First 5 beta clients (founders' network)

Month 6-12: MVP Launch
• RIA license received
• MVP platform live
• 20-30 paying clients
• First advisor hired

Month 12-18: Early Scaling
• Platform V2 with full features
• 50-100 clients
• 2-3 advisors
• First retention data available

Month 18-24: Validation
• 100-150 clients
• Proof of retention
• Unit economics validated
• Series A ready (maybe)

FOUNDER BANDWIDTH REALITY:
With 2 founders, assuming 60-hour weeks:
• Client acquisition/sales: 40 hours/week
• Product/tech oversight: 20 hours/week
• Ops/compliance: 15 hours/week
• Hiring/team: 10 hours/week
• Fundraising: 15 hours/week
• Admin/other: 20 hours/week

TOTAL NEEDED: 120 hours/week
AVAILABLE: 120 hours/week (2 founders)
MARGIN FOR ERROR: Zero

VERDICT: This is buildable but requires exceptional execution discipline. The integration complexity is underestimated, the talent model is expensive, and the time to meaningful revenue is long. Would need ₹5-7 Cr seed funding and 24+ months of runway to reach Series A proof points.
"""
        
        return self._create_response(
            initial_position=initial_position,
            fatal_risks=fatal_risks,
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
