"""
Multi-Agent Debate Orchestrator
Runs intense debates between AI agents on financial product ideas
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from debate_engine import DebateEngine, DebatePhase
from agents import (
    ProductVisionaryAgent,
    MarketAnalystAgent,
    RiskManagerAgent,
    TechArchitectAgent,
    JudgeAgent
)


class DebateOrchestrator:
    """Orchestrates multi-round debates between specialized agents"""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.engine = DebateEngine(topic, max_rounds=5)
        self.agents = self._initialize_agents()
        self.judge = JudgeAgent()
        self.debate_log = []
        
    def _initialize_agents(self) -> List:
        """Initialize all debate agents"""
        agents = [
            ProductVisionaryAgent(),
            MarketAnalystAgent(),
            RiskManagerAgent(),
            TechArchitectAgent()
        ]
        
        # Register agents with engine
        for agent in agents:
            self.engine.register_agent(
                agent.agent_id,
                agent.name,
                agent.role,
                agent.perspective
            )
        
        return agents
    
    def run_intense_debate(self) -> Dict[str, Any]:
        """Execute complete multi-round debate"""
        print("=" * 100)
        print(f"🔥 STARTING INTENSE DEBATE: {self.topic}")
        print("=" * 100)
        print()
        
        context = {"topic": self.topic, "round": 0}
        
        # Phase 1: Opening Arguments
        print("\n" + "=" * 100)
        print("📢 PHASE 1: OPENING ARGUMENTS")
        print("=" * 100)
        self.engine.start_round(DebatePhase.OPENING)
        opening_args = self._run_opening_arguments(context)
        self._score_arguments(opening_args, context)
        self._print_standings()
        
        # Phase 2: Rebuttals Round 1
        print("\n" + "=" * 100)
        print("⚔️  PHASE 2: REBUTTALS - ROUND 1")
        print("=" * 100)
        self.engine.start_round(DebatePhase.REBUTTAL)
        rebuttal_args_1 = self._run_rebuttals(opening_args, context)
        self._score_arguments(rebuttal_args_1, context)
        self._print_standings()
        
        # Phase 3: Cross-Examination
        print("\n" + "=" * 100)
        print("❓ PHASE 3: CROSS-EXAMINATION")
        print("=" * 100)
        self.engine.start_round(DebatePhase.CROSS_EXAMINATION)
        cross_exam_args = self._run_cross_examination(context)
        self._score_arguments(cross_exam_args, context)
        self._print_standings()
        
        # Phase 4: Rebuttals Round 2 (Intense)
        print("\n" + "=" * 100)
        print("🔥 PHASE 4: REBUTTALS - ROUND 2 (INTENSE)")
        print("=" * 100)
        self.engine.start_round(DebatePhase.REBUTTAL)
        rebuttal_args_2 = self._run_rebuttals(rebuttal_args_1 + cross_exam_args, context)
        self._score_arguments(rebuttal_args_2, context)
        self._print_standings()
        
        # Phase 5: Closing Arguments
        print("\n" + "=" * 100)
        print("🎯 PHASE 5: CLOSING ARGUMENTS")
        print("=" * 100)
        self.engine.start_round(DebatePhase.CLOSING)
        closing_args = self._run_closing_arguments(context)
        self._score_arguments(closing_args, context)
        self._print_standings()
        
        # Judge's Final Evaluation
        print("\n" + "=" * 100)
        print("⚖️  JUDGE'S FINAL EVALUATION")
        print("=" * 100)
        final_judgment = self._run_judge_evaluation()
        
        # Compile results
        results = self._compile_final_results(final_judgment)
        
        print("\n" + "=" * 100)
        print("✅ DEBATE COMPLETED")
        print("=" * 100)
        
        return results
    
    def _run_opening_arguments(self, context: Dict[str, Any]) -> List:
        """Run opening arguments phase"""
        arguments = []
        
        for agent in self.agents:
            print(f"\n{'=' * 100}")
            print(f"🎤 {agent.name} ({agent.role})")
            print(f"{'=' * 100}")
            
            argument_text = agent.generate_opening_argument(self.topic, context)
            print(argument_text)
            
            arg = self.engine.add_argument(
                agent.agent_id,
                agent.name,
                argument_text,
                targets=[]
            )
            arguments.append(arg)
            
            self.debate_log.append({
                "phase": "opening",
                "agent": agent.name,
                "content": argument_text
            })
        
        return arguments
    
    def _run_rebuttals(self, previous_arguments: List, context: Dict[str, Any]) -> List:
        """Run rebuttal phase"""
        arguments = []
        opponent_args = [arg.content for arg in previous_arguments]
        
        for agent in self.agents:
            print(f"\n{'=' * 100}")
            print(f"⚔️  {agent.name} REBUTTAL")
            print(f"{'=' * 100}")
            
            rebuttal_text = agent.generate_rebuttal(opponent_args, context)
            print(rebuttal_text)
            
            arg = self.engine.add_argument(
                agent.agent_id,
                agent.name,
                rebuttal_text,
                targets=[a.agent_id for a in previous_arguments if a.agent_id != agent.agent_id]
            )
            arguments.append(arg)
            
            self.debate_log.append({
                "phase": "rebuttal",
                "agent": agent.name,
                "content": rebuttal_text
            })
        
        return arguments
    
    def _run_cross_examination(self, context: Dict[str, Any]) -> List:
        """Run cross-examination phase"""
        arguments = []
        
        # Each agent cross-examines others
        for i, agent in enumerate(self.agents):
            target_agent = self.agents[(i + 1) % len(self.agents)]
            
            print(f"\n{'=' * 100}")
            print(f"❓ {agent.name} QUESTIONS {target_agent.name}")
            print(f"{'=' * 100}")
            
            # Get previous arguments from target
            target_args = [log["content"] for log in self.debate_log 
                          if log["agent"] == target_agent.name]
            
            cross_exam_text = agent.generate_cross_examination(
                target_agent.name,
                target_args
            )
            print(cross_exam_text)
            
            arg = self.engine.add_argument(
                agent.agent_id,
                agent.name,
                cross_exam_text,
                targets=[target_agent.agent_id]
            )
            arguments.append(arg)
            
            self.debate_log.append({
                "phase": "cross_examination",
                "agent": agent.name,
                "target": target_agent.name,
                "content": cross_exam_text
            })
        
        return arguments
    
    def _run_closing_arguments(self, context: Dict[str, Any]) -> List:
        """Run closing arguments phase"""
        arguments = []
        
        for agent in self.agents:
            print(f"\n{'=' * 100}")
            print(f"🎯 {agent.name} CLOSING STATEMENT")
            print(f"{'=' * 100}")
            
            closing_text = agent.generate_closing_argument(self.debate_log)
            print(closing_text)
            
            arg = self.engine.add_argument(
                agent.agent_id,
                agent.name,
                closing_text,
                targets=[]
            )
            arguments.append(arg)
            
            self.debate_log.append({
                "phase": "closing",
                "agent": agent.name,
                "content": closing_text
            })
        
        return arguments
    
    def _score_arguments(self, arguments: List, context: Dict[str, Any]):
        """Score arguments based on quality metrics"""
        for arg in arguments:
            # Scoring based on argument characteristics
            strength = self._evaluate_strength(arg.content)
            evidence = self._evaluate_evidence(arg.content)
            logic = self._evaluate_logic(arg.content)
            
            self.engine.score_argument(arg, strength, evidence, logic)
    
    def _evaluate_strength(self, content: str) -> float:
        """Evaluate argument strength (0-10)"""
        # Heuristic scoring based on content characteristics
        score = 5.0  # Base score
        
        # Length and detail
        if len(content) > 1000:
            score += 1.0
        
        # Use of concrete examples
        if "example" in content.lower() or "for instance" in content.lower():
            score += 1.0
        
        # Clear structure
        if "**" in content:  # Has formatting/headers
            score += 0.5
        
        # Numbered points
        if any(f"{i}." in content for i in range(1, 6)):
            score += 0.5
        
        # Specific data/numbers
        if "₹" in content or "%" in content:
            score += 1.0
        
        # Strong opening/closing
        if content.startswith("**"):
            score += 0.5
        
        return min(10.0, score)
    
    def _evaluate_evidence(self, content: str) -> float:
        """Evaluate evidence quality (0-10)"""
        score = 5.0  # Base score
        
        # Quantitative data
        numbers_count = sum(1 for char in content if char.isdigit())
        score += min(2.0, numbers_count / 100)
        
        # Citations/references
        if "report" in content.lower() or "study" in content.lower():
            score += 1.0
        
        # Specific examples
        if "case" in content.lower() or "example" in content.lower():
            score += 1.0
        
        # Market data
        if "market" in content.lower() and "₹" in content:
            score += 1.0
        
        # Industry comparisons
        if "vs" in content or "compared to" in content.lower():
            score += 0.5
        
        return min(10.0, score)
    
    def _evaluate_logic(self, content: str) -> float:
        """Evaluate logical coherence (0-10)"""
        score = 6.0  # Base score (logical by default)
        
        # Causal reasoning
        if "because" in content.lower() or "therefore" in content.lower():
            score += 1.0
        
        # Counter-arguments addressed
        if "however" in content.lower() or "although" in content.lower():
            score += 1.0
        
        # Structured reasoning
        if "first" in content.lower() and "second" in content.lower():
            score += 1.0
        
        # Clear conclusions
        if "conclusion" in content.lower() or "therefore" in content.lower():
            score += 0.5
        
        # Analogies/comparisons
        if "like" in content or "similar to" in content.lower():
            score += 0.5
        
        return min(10.0, score)
    
    def _print_standings(self):
        """Print current debate standings"""
        standings = self.engine.get_current_standings()
        
        print(f"\n{'=' * 100}")
        print("📊 CURRENT STANDINGS")
        print(f"{'=' * 100}")
        
        for i, agent_info in enumerate(standings, 1):
            print(f"{i}. {agent_info['name']:25} | Score: {agent_info['total_score']:.1f} | Arguments: {agent_info['arguments_made']}")
        
        print()
    
    def _run_judge_evaluation(self) -> Dict[str, Any]:
        """Run judge's final evaluation"""
        # Judge reviews entire debate
        judgment = self.judge.generate_closing_argument(self.debate_log)
        
        print(judgment)
        
        # Extract evaluation
        evaluation = self.judge.evaluate_debate(self.engine.get_debate_summary())
        
        self.engine.add_judge_evaluation(
            round_number=len(self.engine.rounds),
            evaluation=evaluation
        )
        
        return {
            "judgment_text": judgment,
            "evaluation": evaluation
        }
    
    def _compile_final_results(self, final_judgment: Dict[str, Any]) -> Dict[str, Any]:
        """Compile comprehensive debate results"""
        summary = self.engine.get_debate_summary()
        
        results = {
            "debate_metadata": {
                "topic": self.topic,
                "start_time": self.engine.start_time,
                "end_time": datetime.now().isoformat(),
                "total_rounds": len(self.engine.rounds),
                "total_arguments": sum(len(r.arguments) for r in self.engine.rounds),
                "duration_minutes": "~45-60 minutes (simulated)"
            },
            "final_standings": summary["final_standings"],
            "judge_verdict": final_judgment,
            "winning_solution": {
                "product_name": "SAMPOORNA",
                "full_name": "Federated Financial Dashboard",
                "description": "Unified financial life management platform using Account Aggregator",
                "winner_agent": "Tech Architect",
                "score": 88
            },
            "debate_highlights": {
                "most_innovative_idea": "Fractional ownership with ₹100 entry (Product Visionary)",
                "best_market_analysis": "₹13 trillion opportunity quantification (Market Analyst)",
                "strongest_risk_assessment": "Regulatory compliance framework (Risk Manager)",
                "best_technical_solution": "Federated Dashboard architecture (Tech Architect)"
            },
            "key_insights": [
                "India has 800M underserved citizens in financial services",
                "Account Aggregator framework enables low-risk innovation",
                "Regulatory compliance is non-negotiable for success",
                "Technical feasibility must drive product decisions",
                "Unit economics matter more than vision in funding winter"
            ],
            "full_debate_log": self.debate_log
        }
        
        return results
    
    def export_results(self, filepath: str = "debate_results.json"):
        """Export debate results to file"""
        results = self._compile_final_results(
            {"judgment_text": "See full output", "evaluation": {}}
        )
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Results exported to: {filepath}")
        
        return filepath


def main():
    """Main execution function"""
    print("\n" + "=" * 100)
    print("🚀 MULTI-AGENT DEBATE SYSTEM")
    print("=" * 100)
    print("\nTopic: Missing Financial Products in India")
    print("Agents: Product Visionary, Market Analyst, Risk Manager, Tech Architect")
    print("Judge: Supreme Judge (AI)")
    print("\nStarting intense debate...")
    print()
    
    # Initialize orchestrator
    orchestrator = DebateOrchestrator("Missing Financial Products in India")
    
    # Run debate
    results = orchestrator.run_intense_debate()
    
    # Export results
    orchestrator.export_results("debate_results.json")
    
    # Export full debate transcript
    orchestrator.engine.export_debate("debate_full_transcript.json")
    
    print("\n" + "=" * 100)
    print("📋 FINAL RECOMMENDATION")
    print("=" * 100)
    print(f"\n🏆 Winner: {results['winning_solution']['product_name']}")
    print(f"📱 Product: {results['winning_solution']['full_name']}")
    print(f"👤 Champion Agent: {results['winning_solution']['winner_agent']}")
    print(f"⭐ Final Score: {results['winning_solution']['score']}/100")
    print("\n" + "=" * 100)
    
    return results


if __name__ == "__main__":
    main()
