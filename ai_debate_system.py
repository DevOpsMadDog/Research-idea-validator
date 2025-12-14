#!/usr/bin/env python3
"""
AI Agent Debate System - Financial Products Analysis
Simulates intense debate between multiple AI agents analyzing financial product gaps in India
"""

import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class AgentRole(Enum):
    """Different AI agent roles with specific expertise"""
    REGULATOR = "Regulatory Compliance Agent"
    INNOVATOR = "Innovation & FinTech Agent"
    MARKET_ANALYST = "Market Research Agent"
    RISK_SPECIALIST = "Risk Management Agent"
    CONSUMER_ADVOCATE = "Consumer Protection Agent"
    BANKING_EXPERT = "Traditional Banking Agent"
    JUDGE = "Supreme Judge Agent"


@dataclass
class Argument:
    """Represents a single argument in the debate"""
    agent: str
    role: str
    statement: str
    evidence: List[str]
    counter_arguments: List[str]
    intensity: int  # 1-10
    timestamp: str


@dataclass
class DebateRound:
    """A single round of debate"""
    round_number: int
    arguments: List[Argument]
    winner: str = None
    judge_comment: str = None


class AIAgent:
    """Base class for AI agents in the debate"""
    
    def __init__(self, name: str, role: AgentRole, personality: Dict[str, Any]):
        self.name = name
        self.role = role
        self.personality = personality
        self.arguments_made = []
        self.score = 0
        self.aggressiveness = personality.get('aggressiveness', 5)
        self.expertise_level = personality.get('expertise', 8)
        
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        """Generate an argument based on agent's role and personality"""
        raise NotImplementedError


class RegulatoryAgent(AIAgent):
    """Focuses on regulatory compliance and legal frameworks"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        regulatory_points = [
            "RBI regulations currently restrict many innovative products",
            "SEBI framework needs modernization for new asset classes",
            "Regulatory sandbox approach could enable innovation safely",
            "Consumer protection must be paramount in any new product",
            "Cross-border regulatory alignment is crucial",
            "Data privacy laws (DPDP Act) impact financial product design",
            "KYC/AML requirements create barriers for new products"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if arg.role != self.role.value:
                    counter_points.append(f"{arg.agent}'s proposal ignores regulatory reality")
        
        intensity = min(10, 5 + round_num + random.randint(0, 2))
        
        statement = random.choice(regulatory_points)
        if counter_points:
            statement += f" | Counter: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "RBI Master Circular on Financial Products",
                "SEBI Regulatory Framework 2024",
                "DPDP Act Compliance Requirements"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class InnovatorAgent(AIAgent):
    """Focuses on innovation and disruptive fintech solutions"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        innovation_points = [
            "India needs decentralized finance (DeFi) products for financial inclusion",
            "AI-powered personalized investment products are missing",
            "Micro-investment platforms for daily savings are underdeveloped",
            "Peer-to-peer lending needs better infrastructure",
            "Crypto-based financial products could serve unbanked populations",
            "Gamified savings products would engage younger demographics",
            "Real-time insurance products for gig economy workers",
            "Fractional real estate investment platforms",
            "Social trading and copy-trading platforms"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if "regulatory" in arg.role.lower() or "risk" in arg.role.lower():
                    counter_points.append(f"{arg.agent} is stifling innovation with outdated thinking")
        
        intensity = min(10, 6 + round_num + random.randint(0, 3))
        
        statement = random.choice(innovation_points)
        if counter_points:
            statement += f" | Rebuttal: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "Global FinTech Innovation Trends 2024",
                "India's Digital Payment Revolution Success",
                "Unbanked Population Statistics (400M+)"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class MarketAnalystAgent(AIAgent):
    """Focuses on market demand and economic viability"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        market_points = [
            "Market research shows 60% demand for better retirement products",
            "Middle-class needs structured products for wealth creation",
            "Rural market needs simplified insurance products",
            "Young professionals lack tax-efficient investment options",
            "SME sector needs better working capital solutions",
            "Women-specific financial products have huge untapped potential",
            "Education financing products are fragmented and expensive",
            "Healthcare financing beyond insurance is missing"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if "innovation" in arg.role.lower():
                    counter_points.append(f"{arg.agent}'s ideas lack market validation")
        
        intensity = min(10, 5 + round_num + random.randint(0, 2))
        
        statement = random.choice(market_points)
        if counter_points:
            statement += f" | Market Reality: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "NSSO Consumer Expenditure Survey",
                "CRISIL Market Research Reports",
                "BCG Financial Services Market Analysis"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class RiskSpecialistAgent(AIAgent):
    """Focuses on risk management and financial stability"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        risk_points = [
            "New products must have robust risk assessment frameworks",
            "Systemic risk from unregulated products threatens financial stability",
            "Credit risk models need enhancement for new product categories",
            "Operational risk from digital products requires new controls",
            "Market risk from volatile assets needs better hedging mechanisms",
            "Liquidity risk in new products could create crises",
            "Concentration risk in fintech lending is concerning"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if "innovation" in arg.role.lower():
                    counter_points.append(f"{arg.agent} underestimates risk implications")
        
        intensity = min(10, 7 + round_num + random.randint(0, 2))
        
        statement = random.choice(risk_points)
        if counter_points:
            statement += f" | Warning: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "RBI Financial Stability Report",
                "Basel III Risk Framework",
                "Historical Financial Crisis Analysis"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class ConsumerAdvocateAgent(AIAgent):
    """Focuses on consumer protection and accessibility"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        consumer_points = [
            "Products must be accessible to non-English speakers",
            "Financial literacy is a barrier - products need simplification",
            "Hidden fees and complex terms exploit consumers",
            "Digital divide prevents rural access to new products",
            "Women face unique barriers in accessing financial products",
            "Elderly population needs age-appropriate products",
            "Transparency in product terms is severely lacking"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if "banking" in arg.role.lower() or "market" in arg.role.lower():
                    counter_points.append(f"{arg.agent} prioritizes profit over consumer welfare")
        
        intensity = min(10, 6 + round_num + random.randint(0, 3))
        
        statement = random.choice(consumer_points)
        if counter_points:
            statement += f" | Consumer Impact: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "Consumer Complaints Data (RBI Ombudsman)",
                "Financial Literacy Survey India",
                "Accessibility Studies"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class BankingExpertAgent(AIAgent):
    """Represents traditional banking perspective"""
    
    def generate_argument(self, topic: str, previous_arguments: List[Argument], round_num: int) -> Argument:
        banking_points = [
            "Traditional products have proven track records",
            "Banks have extensive distribution networks",
            "Regulatory compliance is already established",
            "Customer trust in banks is higher than fintechs",
            "Banks can offer integrated product suites",
            "Risk management infrastructure is mature",
            "Cross-selling opportunities exist with existing customers"
        ]
        
        counter_points = []
        if previous_arguments:
            for arg in previous_arguments[-3:]:
                if "innovation" in arg.role.lower():
                    counter_points.append(f"{arg.agent} ignores banks' competitive advantages")
        
        intensity = min(10, 5 + round_num + random.randint(0, 2))
        
        statement = random.choice(banking_points)
        if counter_points:
            statement += f" | Traditional Value: {random.choice(counter_points)}"
        
        return Argument(
            agent=self.name,
            role=self.role.value,
            statement=statement,
            evidence=[
                "Banking Industry Performance Reports",
                "Customer Trust Surveys",
                "Market Share Analysis"
            ],
            counter_arguments=counter_points,
            intensity=intensity,
            timestamp=datetime.now().isoformat()
        )


class JudgeAgent(AIAgent):
    """Supreme judge that evaluates all arguments"""
    
    def __init__(self, name: str, role: AgentRole, personality: Dict[str, Any]):
        super().__init__(name, role, personality)
        self.evaluation_criteria = [
            "Evidence Quality",
            "Logical Consistency",
            "Feasibility",
            "Market Impact",
            "Risk Assessment",
            "Consumer Benefit",
            "Regulatory Alignment"
        ]
    
    def evaluate_round(self, round: DebateRound, all_arguments: List[Argument]) -> Dict[str, Any]:
        """Evaluate a debate round and score each agent"""
        scores = {}
        comments = {}
        
        for arg in round.arguments:
            score = 0
            
            # Evidence quality (0-20 points)
            score += len(arg.evidence) * 5
            
            # Intensity and engagement (0-15 points)
            score += arg.intensity * 1.5
            
            # Counter-argument quality (0-15 points)
            score += len(arg.counter_arguments) * 5
            
            # Statement clarity and relevance (0-20 points)
            score += 15 if len(arg.statement) > 50 else 10
            
            # Role-specific expertise (0-30 points)
            role_bonus = {
                "Regulatory Compliance Agent": 25,
                "Innovation & FinTech Agent": 28,
                "Market Research Agent": 27,
                "Risk Management Agent": 26,
                "Consumer Protection Agent": 24,
                "Traditional Banking Agent": 23
            }
            score += role_bonus.get(arg.role, 20)
            
            scores[arg.agent] = score
            
            # Generate judge comment
            if score > 80:
                comments[arg.agent] = f"EXCELLENT: {arg.agent} presented compelling arguments with strong evidence. Well-reasoned and impactful."
            elif score > 60:
                comments[arg.agent] = f"STRONG: {arg.agent} made valid points but could strengthen evidence base."
            elif score > 40:
                comments[arg.agent] = f"ADEQUATE: {arg.agent}'s arguments were reasonable but lacked depth."
            else:
                comments[arg.agent] = f"WEAK: {arg.agent} needs to provide more substantial evidence and analysis."
        
        # Determine round winner
        winner = max(scores.items(), key=lambda x: x[1])[0] if scores else None
        
        return {
            "scores": scores,
            "comments": comments,
            "winner": winner,
            "round_summary": f"Round {round.round_number} concluded. {winner} presented the strongest argument."
        }
    
    def final_judgment(self, all_rounds: List[DebateRound], topic: str) -> Dict[str, Any]:
        """Provide final judgment on the entire debate"""
        agent_total_scores = {}
        agent_argument_counts = {}
        
        for round in all_rounds:
            for arg in round.arguments:
                if arg.agent not in agent_total_scores:
                    agent_total_scores[arg.agent] = 0
                    agent_argument_counts[arg.agent] = 0
                agent_total_scores[arg.agent] += arg.intensity * 10
                agent_argument_counts[arg.agent] += 1
        
        # Calculate average scores
        agent_avg_scores = {
            agent: agent_total_scores[agent] / agent_argument_counts[agent]
            for agent in agent_total_scores
        }
        
        overall_winner = max(agent_avg_scores.items(), key=lambda x: x[1])[0] if agent_avg_scores else None
        
        # Generate comprehensive analysis
        judgment = {
            "topic": topic,
            "overall_winner": overall_winner,
            "agent_scores": agent_avg_scores,
            "total_arguments": sum(agent_argument_counts.values()),
            "key_insights": [
                "Regulatory framework needs modernization while maintaining stability",
                "Innovation must balance disruption with consumer protection",
                "Market demand exists but requires proper product-market fit",
                "Risk management cannot be compromised for innovation",
                "Consumer accessibility and literacy are critical success factors"
            ],
            "recommendations": [
                "Establish regulatory sandbox for testing new products",
                "Develop financial literacy programs alongside products",
                "Create risk assessment frameworks for new product categories",
                "Ensure multi-language and multi-channel accessibility",
                "Foster collaboration between traditional banks and fintechs"
            ],
            "top_missing_products": [
                "AI-powered personalized investment advisors",
                "Micro-investment platforms for daily savings",
                "Real-time insurance for gig economy workers",
                "Fractional real estate investment products",
                "Social trading and copy-trading platforms",
                "Simplified retirement planning products",
                "Women-specific financial products",
                "Education financing solutions"
            ]
        }
        
        return judgment


class DebateSystem:
    """Main system orchestrating the AI agent debate"""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.agents: List[AIAgent] = []
        self.rounds: List[DebateRound] = []
        self.all_arguments: List[Argument] = []
        self.judge: JudgeAgent = None
        
    def initialize_agents(self):
        """Initialize all debate agents"""
        self.agents = [
            RegulatoryAgent("RegBot-3000", AgentRole.REGULATOR, {
                "aggressiveness": 7,
                "expertise": 9,
                "style": "authoritative"
            }),
            InnovatorAgent("InnoVator-X", AgentRole.INNOVATOR, {
                "aggressiveness": 9,
                "expertise": 8,
                "style": "disruptive"
            }),
            MarketAnalystAgent("MarketMind", AgentRole.MARKET_ANALYST, {
                "aggressiveness": 6,
                "expertise": 9,
                "style": "analytical"
            }),
            RiskSpecialistAgent("RiskGuard", AgentRole.RISK_SPECIALIST, {
                "aggressiveness": 8,
                "expertise": 9,
                "style": "cautious"
            }),
            ConsumerAdvocateAgent("ConsumerVoice", AgentRole.CONSUMER_ADVOCATE, {
                "aggressiveness": 7,
                "expertise": 8,
                "style": "passionate"
            }),
            BankingExpertAgent("BankMaster", AgentRole.BANKING_EXPERT, {
                "aggressiveness": 5,
                "expertise": 9,
                "style": "traditional"
            })
        ]
        
        self.judge = JudgeAgent("SupremeJudge-AI", AgentRole.JUDGE, {
            "aggressiveness": 0,
            "expertise": 10,
            "style": "impartial"
        })
    
    def conduct_debate(self, num_rounds: int = 5):
        """Conduct the debate across multiple rounds"""
        print(f"\n{'='*80}")
        print(f"AI AGENT DEBATE: {self.topic}")
        print(f"{'='*80}\n")
        
        for round_num in range(1, num_rounds + 1):
            print(f"\n{'─'*80}")
            print(f"ROUND {round_num} - INTENSITY ESCALATING")
            print(f"{'─'*80}\n")
            
            round_arguments = []
            
            # Each agent makes an argument
            for agent in self.agents:
                arg = agent.generate_argument(
                    self.topic,
                    self.all_arguments,
                    round_num
                )
                round_arguments.append(arg)
                self.all_arguments.append(arg)
                
                # Display argument with intensity
                intensity_bar = "█" * arg.intensity + "░" * (10 - arg.intensity)
                print(f"[{arg.agent}] ({arg.role})")
                print(f"Intensity: [{intensity_bar}] {arg.intensity}/10")
                print(f"Statement: {arg.statement}")
                if arg.evidence:
                    print(f"Evidence: {', '.join(arg.evidence[:2])}")
                if arg.counter_arguments:
                    print(f"Counters: {len(arg.counter_arguments)} previous arguments")
                print()
                
                # Simulate thinking time
                time.sleep(0.3)
            
            # Judge evaluates the round
            evaluation = self.judge.evaluate_round(
                DebateRound(round_num, round_arguments),
                self.all_arguments
            )
            
            round_obj = DebateRound(round_num, round_arguments)
            round_obj.winner = evaluation["winner"]
            round_obj.judge_comment = evaluation["round_summary"]
            self.rounds.append(round_obj)
            
            print(f"\n⚖️  JUDGE EVALUATION:")
            print(f"Round Winner: {evaluation['winner']}")
            for agent, comment in evaluation["comments"].items():
                print(f"  • {agent}: {comment}")
            print()
            
            time.sleep(1)
    
    def final_judgment(self):
        """Get final judgment from judge"""
        judgment = self.judge.final_judgment(self.rounds, self.topic)
        
        print(f"\n{'='*80}")
        print("🏆 FINAL JUDGMENT - SUPREME JUDGE AI")
        print(f"{'='*80}\n")
        
        print(f"Topic: {judgment['topic']}\n")
        print(f"Overall Winner: {judgment['overall_winner']}\n")
        
        print("Agent Performance Scores:")
        sorted_scores = sorted(judgment['agent_scores'].items(), 
                             key=lambda x: x[1], reverse=True)
        for agent, score in sorted_scores:
            bar_length = int(score / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            print(f"  {agent:20s} [{bar}] {score:.1f}")
        
        print(f"\n📊 Key Insights:")
        for i, insight in enumerate(judgment['key_insights'], 1):
            print(f"  {i}. {insight}")
        
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(judgment['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n🎯 Top Missing Financial Products in India:")
        for i, product in enumerate(judgment['top_missing_products'], 1):
            print(f"  {i}. {product}")
        
        return judgment


def main():
    """Main execution function"""
    topic = "Missing Financial Products in India: Identifying Gaps and Opportunities"
    
    debate = DebateSystem(topic)
    debate.initialize_agents()
    debate.conduct_debate(num_rounds=5)
    judgment = debate.final_judgment()
    
    # Save results
    output = {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "rounds": [asdict(round) for round in debate.rounds],
        "final_judgment": judgment
    }
    
    with open("debate_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n{'='*80}")
    print("✅ Debate complete! Results saved to debate_results.json")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
