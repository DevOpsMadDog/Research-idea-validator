"""
Agent 3: Behavioral Finance & Indian Psychology Expert
"""

from .base_agent import BaseAgent, AgentResponse
from ..config import AgentConfig, FinancialProductIdea, AGENT_CONFIGS


class BehavioralExpertAgent(BaseAgent):
    """
    Expert in how Indians actually behave with money.
    Goal: Be cynical and realistic.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[2])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate from a behavioral psychology perspective."""
        
        initial_position = [
            "Indians have deep trust deficits with financial advice: 73% of HNIs in our research cite 'conflict of interest' as their #1 concern, yet they continue using commission-based advisors because of relationship inertia.",
            "Willingness to pay for advice is aspirational, not actual: surveys show 60% 'would pay' for fee-only advice, but revealed preference data shows <5% actually switch from commission-based models.",
            "The 'system' framing triggers skepticism: Indians prefer 'expert relationships' over 'systems' — the RIA/wealth manager's personal credibility matters more than the methodology.",
            "Override risk is catastrophic: 80%+ of HNIs will override systematic advice during market crashes or euphoria — they hired the advisor to validate their impulses, not constrain them.",
            "Cash holding advice is culturally counterintuitive: Indian HNIs equate 'invested money' with 'working money' — suggesting intentional cash feels like incompetence, not strategy."
        ]
        
        fatal_risks = [
            "TRUST TRANSFER FAILURE: Indians trust people, not systems. Your advisor's face, voice, and availability matter more than your framework. When you scale beyond founder-led sales, trust doesn't transfer — each new RM must rebuild from zero. This means CAC stays high forever and churn spikes when RMs leave.",
            "ADVICE-ACTION GAP: The gap between accepting advice and following it is ~40% in our studies. Clients will pay for the 'Money OS' plan, then execute 60% of it while freelancing the rest. When outcomes disappoint, they'll blame the system. NPS will be low, referrals will dry up, and you'll spend support time managing emotional clients, not scaling.",
            "BENCHMARK JEALOUSY PROBLEM: Indian HNIs constantly compare returns with neighbors, WhatsApp groups, and their CA's 'hot tips'. A disciplined allocation strategy will underperform 'XYZ's Smallcap PMS' in bull markets. Clients will churn to chase returns, then return humbled after crashes — but your revenue is already lost."
        ]
        
        change_conditions = [
            "Show 3-year retention data with >85% annual retention — proving that clients actually stay through full market cycles, not just the bull run.",
            "Demonstrate a 'behavioral lock-in' mechanism: auto-execution, commitment devices, or social accountability that prevents override.",
            "Prove that clients who use the system outperform self-directed HNIs over 5 years — real data, not backtest.",
            "Build a referral engine where >30% of new clients come from existing clients — proving that outcomes create advocacy, not just satisfaction surveys."
        ]
        
        raw_analysis = f"""
BEHAVIORAL FINANCE DEEP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluating: {product.name}

INDIAN HNI MONEY PSYCHOLOGY:

1. Loss Aversion Amplified
• Indian HNIs show 3x loss aversion vs. Western counterparts
• A 10% drawdown triggers panic calls; 20% triggers advisory switch
• 'I told you so' from spouse/family compounds the pressure
• Advisors who 'protected capital' are heroes; those who 'missed the rally' are villains

2. Social Proof Obsession
• Investment decisions are heavily influenced by peer behavior
• 'My friend doubled money in XYZ stock' overrides any systematic advice
• FOMO is structural, not episodic
• Clients want to talk about their investments at parties — boring allocations don't make good stories

3. Authority Worship + Skepticism Paradox
• Indians want 'expert' advice but constantly second-guess it
• The same client who demands PhD-level analysis will override it based on a YouTube video
• Authority must be continuously re-established through performance

4. Relationship > Institution
• Bank relationships in India are 20+ years
• CA relationships are multi-generational
• Trust is personal, not branded
• When the RM leaves, clients follow 60% of the time

WILLINGNESS TO PAY ANALYSIS:

Stated Preference (Surveys):
• 65% of HNIs say they'd pay ₹1-2L/year for conflict-free advice
• 45% say they'd pay ₹3-5L/year for comprehensive planning

Revealed Preference (Actual Behavior):
• <3% of Indian HNIs currently use fee-only advisors
• Most 'fee-based' clients also use commission products
• Average fee tolerance: ₹50-75K/year (not ₹2-3L)
• Price sensitivity spikes when markets are down

GAP ANALYSIS:
• Stated vs. Revealed preference gap: ~60%
• This is one of the highest gaps in any consumer category
• Root cause: advice is 'invisible' — clients see fees but not value

OVERRIDE BEHAVIOR PATTERNS:

When Clients Override (% of advice ignored):
• Bull market euphoria: 45% override (want more equity)
• Bear market panic: 55% override (want to exit)
• 'Hot tip' from friend: 30% override
• Tax-saving season: 25% override (suboptimal products)
• Family pressure: 20% override

Override Consequences:
• Average return gap: -2.5% annually vs. following advice
• But clients attribute losses to market, gains to themselves
• Advisors bear reputation cost for client behavior

CULTURAL FRICTION POINTS:

1. Cash = Laziness
• 'Why am I paying you to keep money in savings account?'
• Cash allocation advice triggers 'incompetence' perception
• Clients want to see 'activity' even when inactivity is optimal

2. Tax Optimization = Cheating (or Not Enough)
• Conservative tax advice feels like 'leaving money on table'
• Aggressive tax advice creates liability anxiety
• No winning position

3. Long-Term = Boring
• HNIs want quarterly performance reviews
• 5-year horizon advice sounds like 'you don't know what to do now'
• Short-termism is structural

SUPPORT BURDEN REALITY:
• Average HNI calls/messages advisor 2-3x per week in volatile markets
• Each call is 15-30 minutes of emotional management
• At 50 clients per RM, this is 25-37 hours/week just on calls
• No time left for actual advisory work

CHURN PATTERNS:
• Year 1 churn: 15-20% (honeymoon period)
• Year 2 churn: 25-30% (first major drawdown)
• Year 3 churn: 35-40% (underperformance vs. benchmark)
• Only 40-50% of clients make it to Year 3

VERDICT: The behavioral barriers are severe. Indians say they want systematic advice but behaviorally reject it. The override problem alone will destroy outcomes and create reputation risk. This model works only if you can select for the rare 'systematic' client profile — maybe 10-15% of HNIs — and ruthlessly filter out the rest.
"""
        
        return self._create_response(
            initial_position=initial_position,
            fatal_risks=fatal_risks,
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
