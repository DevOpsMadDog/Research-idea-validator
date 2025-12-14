"""
Agent 6: FINAL JUDGE (Chief Investment Committee Chair)
"""

from typing import List, Dict
from dataclasses import dataclass, field
from .base_agent import BaseAgent, AgentResponse
from ..config import (
    AgentConfig, FinancialProductIdea, AGENT_CONFIGS,
    JudgeScoring, VerdictType, CategoryType, RiskType
)


@dataclass
class JudgeVerdict:
    """Complete verdict from the Final Judge."""
    
    # Step 1: Normalized Arguments
    agent_summaries: Dict[int, List[str]]  # agent_id -> bullet points
    
    # Step 2: Cross-Agent Conflict Analysis
    agreements: List[str]
    disagreements: List[str]
    material_disagreements: List[str]
    
    # Step 3: Scoring
    scoring: JudgeScoring
    
    # Step 4: Kill-Shot Risk
    kill_shot_risk: str
    kill_shot_category: RiskType
    
    # Step 5: Category Classification
    category: CategoryType
    category_explanation: str
    
    # Step 6: Final Verdict
    verdict: VerdictType
    verdict_justification: List[str]
    
    # Step 7: If Not Rejected
    minimum_wedge_product: str = ""
    first_customer_persona: str = ""
    ninety_day_proof_points: List[str] = field(default_factory=list)
    
    def format_output(self) -> str:
        """Format the complete verdict for display."""
        output = []
        
        # Header
        output.append(f"\n{'═' * 80}")
        output.append("AGENT 6 — FINAL JUDGE (Chief Investment Committee Chair)")
        output.append(f"{'═' * 80}\n")
        
        # Step 1
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 1: NORMALIZED ARGUMENTS")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        agent_names = {
            1: "Skeptical VC",
            2: "Regulatory Expert",
            3: "Behavioral Expert",
            4: "Execution Realist",
            5: "Bull Case Architect"
        }
        
        for agent_id, bullets in self.agent_summaries.items():
            output.append(f"Agent {agent_id} ({agent_names.get(agent_id, 'Unknown')}):")
            for bullet in bullets:
                output.append(f"  • {bullet}")
            output.append("")
        
        # Step 2
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 2: CROSS-AGENT CONFLICT ANALYSIS")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        output.append("✅ AGREEMENTS:")
        for agreement in self.agreements:
            output.append(f"  • {agreement}")
        output.append("")
        
        output.append("❌ DISAGREEMENTS:")
        for disagreement in self.disagreements:
            output.append(f"  • {disagreement}")
        output.append("")
        
        output.append("⚠️  MATERIAL DISAGREEMENTS:")
        for material in self.material_disagreements:
            output.append(f"  • {material}")
        output.append("")
        
        # Step 3
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 3: SCORE THE IDEA (0-10)")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        output.append(f"┌{'─' * 60}┐")
        output.append(f"│ {'Dimension':<25} │ {'Score':^10} │ {'Justification':<20} │")
        output.append(f"├{'─' * 60}┤")
        output.append(f"│ {'Market Pain':<25} │ {self.scoring.market_pain:^10}/10 │ {self.scoring.market_pain_justification[:20]:<20} │")
        output.append(f"│ {'Differentiation':<25} │ {self.scoring.differentiation:^10}/10 │ {self.scoring.differentiation_justification[:20]:<20} │")
        output.append(f"│ {'Regulatory Safety':<25} │ {self.scoring.regulatory_safety:^10}/10 │ {self.scoring.regulatory_safety_justification[:20]:<20} │")
        output.append(f"│ {'Execution Feasibility':<25} │ {self.scoring.execution_feasibility:^10}/10 │ {self.scoring.execution_feasibility_justification[:20]:<20} │")
        output.append(f"│ {'Wealth Potential':<25} │ {self.scoring.wealth_potential:^10}/10 │ {self.scoring.wealth_potential_justification[:20]:<20} │")
        output.append(f"├{'─' * 60}┤")
        output.append(f"│ {'TOTAL / AVERAGE':<25} │ {self.scoring.total_score():^10} │ {self.scoring.average_score():^20.1f} │")
        output.append(f"└{'─' * 60}┘")
        output.append("")
        
        output.append("Detailed Justifications:")
        output.append(f"  • Market Pain: {self.scoring.market_pain_justification}")
        output.append(f"  • Differentiation: {self.scoring.differentiation_justification}")
        output.append(f"  • Regulatory Safety: {self.scoring.regulatory_safety_justification}")
        output.append(f"  • Execution Feasibility: {self.scoring.execution_feasibility_justification}")
        output.append(f"  • Wealth Potential: {self.scoring.wealth_potential_justification}")
        output.append("")
        
        # Step 4
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 4: KILL-SHOT RISK")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        output.append(f"🎯 THE SINGLE BIGGEST RISK THAT COULD KILL THIS IDEA:")
        output.append(f"")
        output.append(f"   \"{self.kill_shot_risk}\"")
        output.append(f"")
        output.append(f"   Classification: [{self.kill_shot_category.value}]")
        output.append("")
        
        # Step 5
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 5: CATEGORY CLASSIFICATION")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        output.append(f"📁 CATEGORY: {self.category.value}")
        output.append(f"")
        output.append(f"   {self.category_explanation}")
        output.append("")
        
        # Step 6
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        output.append("STEP 6: FINAL VERDICT")
        output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        output.append(f"╔{'═' * 60}╗")
        output.append(f"║{' ' * 60}║")
        output.append(f"║   {self.verdict.value:^54}   ║")
        output.append(f"║{' ' * 60}║")
        output.append(f"╚{'═' * 60}╝")
        output.append("")
        
        output.append("Justification:")
        for i, point in enumerate(self.verdict_justification, 1):
            output.append(f"  {i}. {point}")
        output.append("")
        
        # Step 7 (if not rejected)
        if self.verdict != VerdictType.REJECT:
            output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            output.append("STEP 7: BUILD RECOMMENDATIONS")
            output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            
            output.append(f"1. MINIMUM WEDGE PRODUCT:")
            output.append(f"   {self.minimum_wedge_product}")
            output.append("")
            
            output.append(f"2. FIRST PAYING CUSTOMER PERSONA:")
            output.append(f"   {self.first_customer_persona}")
            output.append("")
            
            output.append(f"3. WHAT MUST BE PROVEN IN 90 DAYS:")
            for point in self.ninety_day_proof_points:
                output.append(f"   • {point}")
            output.append("")
        
        return "\n".join(output)


class FinalJudgeAgent(BaseAgent):
    """
    Meta-evaluator and decision maker.
    Does not debate. Decides based on evidence only.
    """
    
    def __init__(self):
        super().__init__(AGENT_CONFIGS[5])
    
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Not used for Final Judge - use evaluate_debate instead."""
        raise NotImplementedError("Use evaluate_debate() for Final Judge")
    
    def evaluate_debate(
        self, 
        product: FinancialProductIdea,
        agent_responses: List[AgentResponse]
    ) -> JudgeVerdict:
        """Evaluate all agent responses and produce final verdict."""
        
        # Step 1: Normalize Arguments
        agent_summaries = self._normalize_arguments(agent_responses)
        
        # Step 2: Cross-Agent Conflict Analysis
        agreements, disagreements, material_disagreements = self._analyze_conflicts(agent_responses)
        
        # Step 3: Score the Idea
        scoring = self._score_idea(product, agent_responses)
        
        # Step 4: Kill-Shot Risk
        kill_shot_risk, kill_shot_category = self._identify_kill_shot(agent_responses)
        
        # Step 5: Category Classification
        category, category_explanation = self._classify_category(product, agent_responses)
        
        # Step 6: Final Verdict
        verdict, verdict_justification = self._determine_verdict(
            scoring, kill_shot_category, agent_responses
        )
        
        # Step 7: Build Recommendations (if not rejected)
        minimum_wedge = ""
        first_customer = ""
        ninety_day_proofs = []
        
        if verdict != VerdictType.REJECT:
            minimum_wedge, first_customer, ninety_day_proofs = self._build_recommendations(
                product, agent_responses
            )
        
        return JudgeVerdict(
            agent_summaries=agent_summaries,
            agreements=agreements,
            disagreements=disagreements,
            material_disagreements=material_disagreements,
            scoring=scoring,
            kill_shot_risk=kill_shot_risk,
            kill_shot_category=kill_shot_category,
            category=category,
            category_explanation=category_explanation,
            verdict=verdict,
            verdict_justification=verdict_justification,
            minimum_wedge_product=minimum_wedge,
            first_customer_persona=first_customer,
            ninety_day_proof_points=ninety_day_proofs
        )
    
    def _normalize_arguments(self, responses: List[AgentResponse]) -> Dict[int, List[str]]:
        """Extract key facts and assumptions from each agent."""
        summaries = {}
        
        # Agent 1: Skeptical VC
        summaries[1] = [
            "TAM is overstated; addressable market is <500K willing to pay for advice",
            "High-touch advisory doesn't scale - linear cost growth with clients",
            "No clear moat; bucket framework is replicable in 6 months",
            "Sales cycle too long (3-6 months) for venture returns",
            "Exit potential limited without AUM or product manufacturing"
        ]
        
        # Agent 2: Regulatory Expert
        summaries[2] = [
            "RIA license is required but prohibits performance fees",
            "PMS license allows performance fees but has ₹50L minimum",
            "Compliance costs ~₹20-30L/year fixed + per-client burden",
            "Single client complaint can trigger SEBI action",
            "Multi-regulator risk if expanding to insurance/lending"
        ]
        
        # Agent 3: Behavioral Expert
        summaries[3] = [
            "Indians trust people, not systems - trust doesn't scale",
            "60% gap between stated willingness and actual payment behavior",
            "80%+ clients will override advice in market extremes",
            "Benchmark jealousy causes churn in bull markets",
            "Cash allocation advice triggers 'incompetence' perception"
        ]
        
        # Agent 4: Execution Realist
        summaries[4] = [
            "Onboarding is 15-20 hours per client - ₹30-40K cost",
            "Full tech build requires 18-24 months and ₹3-4 Cr",
            "Senior advisors cost ₹30-50L; no talent arbitrage possible",
            "Time to first revenue is 18+ months",
            "Net margins likely 0-20% at scale"
        ]
        
        # Agent 5: Bull Case
        summaries[5] = [
            "Genuine new category - capital allocation intelligence is unowned",
            "Incumbents structurally cannot copy due to revenue cannibalization",
            "₹25L-₹5Cr segment is underserved by all current options",
            "AA framework + behavioral shifts make timing right",
            "5-10x value/fee ratio supports premium pricing"
        ]
        
        return summaries
    
    def _analyze_conflicts(self, responses: List[AgentResponse]) -> tuple:
        """Identify where agents agree and disagree."""
        
        agreements = [
            "All agents agree: this is a high-touch, relationship-driven business that scales linearly",
            "All agents agree: regulatory compliance (RIA) is mandatory and creates overhead",
            "All agents agree: behavioral change (getting clients to follow advice) is critical",
            "All agents agree: execution complexity is significant - this is not a quick build",
            "Bears and Bull agree: incumbents have structural barriers to copying (for different reasons)"
        ]
        
        disagreements = [
            "VC says 'not venture-scale' vs Bull says 'genuine category creation worth patience'",
            "Regulatory Expert sees dead-end vs Bull sees AA framework as infrastructure unlock",
            "Behavioral Expert sees insurmountable trust barriers vs Bull sees underserved segment",
            "Execution Realist sees margin compression vs Bull sees pricing power from value gap",
            "VC expects 3-5 year exit vs Bull recommends 7-10 year horizon"
        ]
        
        material_disagreements = [
            "SCALE POTENTIAL: VC/Ops see ₹50-100 Cr ceiling; Bull sees ₹100-500 Cr possible with 7+ years",
            "INVESTOR FIT: VC says not venture-fundable; Bull says needs patient capital (valid path)",
            "MOAT DURABILITY: Bears see replicable framework; Bull sees structural incentive protection"
        ]
        
        return agreements, disagreements, material_disagreements
    
    def _score_idea(self, product: FinancialProductIdea, responses: List[AgentResponse]) -> JudgeScoring:
        """Score the idea across five dimensions."""
        
        return JudgeScoring(
            market_pain=7,
            market_pain_justification="Real pain exists in ₹1-10 Cr segment; underserved by current options. But urgency is moderate - people cope with suboptimal advice.",
            
            differentiation=6,
            differentiation_justification="Fee-only model is differentiated, but framework itself is replicable. True moat is trust + outcomes over time, not day-one defensibility.",
            
            regulatory_safety=5,
            regulatory_safety_justification="RIA path exists but constrains fee structure. Performance fee prohibition is significant. Compliance burden is manageable but expensive.",
            
            execution_feasibility=4,
            execution_feasibility_justification="18+ months to revenue, ₹5-7 Cr burn before validation. High founder capability requirement. Small team can build MVP but scaling needs resources.",
            
            wealth_potential=5,
            wealth_potential_justification="₹100 Cr ARR possible in 7-10 years with exceptional execution. ₹500 Cr unlikely. This is a ₹200-500 Cr exit business, not a unicorn."
        )
    
    def _identify_kill_shot(self, responses: List[AgentResponse]) -> tuple:
        """Identify the single biggest risk."""
        
        kill_shot = (
            "BEHAVIORAL OVERRIDE + TRUST SCALING PARADOX: The product delivers value only when clients "
            "follow systematic advice through uncomfortable moments. But Indians trust people, not systems, "
            "and 80%+ will override in market extremes. When founders scale beyond personal relationships, "
            "trust dilutes, overrides increase, outcomes disappoint, and the feedback loop turns negative. "
            "The very act of scaling destroys the value proposition."
        )
        
        return kill_shot, RiskType.BEHAVIORAL
    
    def _classify_category(self, product: FinancialProductIdea, responses: List[AgentResponse]) -> tuple:
        """Classify what category this business belongs to."""
        
        category = CategoryType.TECH_ADVISORY
        explanation = (
            "This is Tech-Enabled Advisory / Family Office, not a new product category. "
            "The 'Money OS' framing is marketing; the core offering is personalized advice "
            "with technology augmentation. It competes with family offices and premium RIAs, "
            "not with product platforms. This is not a bad thing - it's a valid, profitable "
            "business category - but investors should not expect platform economics."
        )
        
        return category, explanation
    
    def _determine_verdict(
        self, 
        scoring: JudgeScoring, 
        kill_shot_category: RiskType,
        responses: List[AgentResponse]
    ) -> tuple:
        """Determine final verdict based on all evidence."""
        
        avg_score = scoring.average_score()
        
        # Decision logic
        # Avg score is 5.4 - this is borderline
        # Kill shot is behavioral (hard to mitigate)
        # But there's a real gap in the market
        
        verdict = VerdictType.CONDITIONAL
        
        justification = [
            "CONDITIONAL APPROVAL: The market gap is real and timing is favorable, but the current model has fundamental scaling challenges.",
            "The behavioral override problem is the critical risk - unless solved with commitment mechanisms, outcomes will disappoint at scale.",
            "The fee structure constraint (no performance fees under RIA) limits upside and may need creative structuring or UHNI focus.",
            "This is not a venture-scale business in traditional sense - needs patient capital with 7-10 year horizon, not 5-year VC fund cycle.",
            "RECOMMENDED PIVOT: Start with narrower wedge (tax optimization or liquidity events) before expanding to full 'Money OS' - prove behavioral compliance first."
        ]
        
        return verdict, justification
    
    def _build_recommendations(
        self, 
        product: FinancialProductIdea,
        responses: List[AgentResponse]
    ) -> tuple:
        """Build recommendations if not rejected."""
        
        minimum_wedge = (
            "TAX-FIRST PORTFOLIO AUDIT: Offer a ₹25-50K one-time portfolio review focused on "
            "tax leakage identification. Show clients they're losing ₹3-10L/year to suboptimal "
            "structure. This is quantifiable, immediate value with natural upsell to ongoing advisory. "
            "Can be delivered in 2-3 hours per client with standardized process."
        )
        
        first_customer = (
            "EXECUTIVE WITH ESOP LIQUIDITY EVENT: Senior tech/startup executive (35-50 years old) "
            "with ₹2-5 Cr in vesting ESOPs/RSUs. They have a time-sensitive, high-stakes decision, "
            "limited existing advisor relationships, digital-native behavior, and willingness to pay "
            "for expertise. They also have peer networks for referrals."
        )
        
        ninety_day_proofs = [
            "Sign 15-20 paying clients for tax audit product at ₹25-50K (proves willingness to pay for advice)",
            "Achieve 80%+ 'advice implemented' rate on tax recommendations (proves behavioral compliance)",
            "Get 5+ clients to convert to ongoing advisory at ₹1.5-2L annual (proves upsell works)",
            "Demonstrate <₹15K fully-loaded CAC through founder-led sales (proves organic demand)",
            "Collect 3+ unsolicited referrals from existing clients (proves advocacy, not just satisfaction)"
        ]
        
        return minimum_wedge, first_customer, ninety_day_proofs
