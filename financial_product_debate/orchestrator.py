"""
Debate Orchestrator - Runs the complete multi-agent debate simulation.
"""

import time
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from .config import FinancialProductIdea, DEFAULT_PRODUCT_IDEA, AGENT_CONFIGS
from .agents import (
    AgentResponse,
    SkepticalVCAgent,
    RegulatoryExpertAgent,
    BehavioralExpertAgent,
    ExecutionRealistAgent,
    BullCaseAgent,
    FinalJudgeAgent,
)
from .agents.final_judge import JudgeVerdict


@dataclass
class DebateResult:
    """Complete result of the multi-agent debate."""
    
    product: FinancialProductIdea
    agent_responses: List[AgentResponse]
    judge_verdict: JudgeVerdict
    execution_time_seconds: float
    timestamp: str
    
    def format_full_output(self) -> str:
        """Format the complete debate output for display."""
        output = []
        
        # Header
        output.append("╔" + "═" * 78 + "╗")
        output.append("║" + " " * 78 + "║")
        output.append("║" + "MULTI-AGENT DEBATE: FINANCIAL PRODUCT VALIDATION".center(78) + "║")
        output.append("║" + "India Focus | Adversarial Evaluation | Final Arbitration".center(78) + "║")
        output.append("║" + " " * 78 + "║")
        output.append("╚" + "═" * 78 + "╝")
        output.append("")
        output.append(f"Timestamp: {self.timestamp}")
        output.append(f"Execution Time: {self.execution_time_seconds:.2f} seconds")
        output.append("")
        
        # Product Context
        output.append(self.product.to_prompt_context())
        output.append("")
        
        # Agent Responses
        output.append("\n" + "█" * 80)
        output.append("█" + "  AGENT EVALUATIONS  ".center(78, "█") + "█")
        output.append("█" * 80)
        
        for response in self.agent_responses:
            output.append(response.format_output())
        
        # Judge Verdict
        output.append("\n" + "█" * 80)
        output.append("█" + "  FINAL JUDGMENT  ".center(78, "█") + "█")
        output.append("█" * 80)
        
        output.append(self.judge_verdict.format_output())
        
        # Footer
        output.append("\n" + "═" * 80)
        output.append("END OF MULTI-AGENT DEBATE EVALUATION")
        output.append("═" * 80)
        
        return "\n".join(output)
    
    def get_summary(self) -> str:
        """Get a brief summary of the verdict."""
        v = self.judge_verdict
        return f"""
EXECUTIVE SUMMARY
═════════════════════════════════════════════════════════════════════════════

Product: {self.product.name}

Verdict: {v.verdict.value}

Scores:
  • Market Pain:         {v.scoring.market_pain}/10
  • Differentiation:     {v.scoring.differentiation}/10
  • Regulatory Safety:   {v.scoring.regulatory_safety}/10
  • Execution Feasibility: {v.scoring.execution_feasibility}/10
  • Wealth Potential:    {v.scoring.wealth_potential}/10
  • AVERAGE:             {v.scoring.average_score():.1f}/10

Category: {v.category.value}

Kill-Shot Risk: [{v.kill_shot_category.value}]
{v.kill_shot_risk[:200]}...

Key Justification:
{chr(10).join(f"  {i+1}. {j}" for i, j in enumerate(v.verdict_justification[:3]))}
"""


class DebateOrchestrator:
    """
    Orchestrates the multi-agent debate for financial product evaluation.
    
    Runs agents in sequence:
    1. Skeptical VC
    2. Regulatory Expert
    3. Behavioral Expert
    4. Execution Realist
    5. Bull Case Architect
    6. Final Judge
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        
        # Initialize agents
        self.agents = [
            SkepticalVCAgent(),
            RegulatoryExpertAgent(),
            BehavioralExpertAgent(),
            ExecutionRealistAgent(),
            BullCaseAgent(),
        ]
        self.judge = FinalJudgeAgent()
    
    def _log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def run_debate(
        self, 
        product: Optional[FinancialProductIdea] = None
    ) -> DebateResult:
        """
        Run the complete multi-agent debate.
        
        Args:
            product: The financial product idea to evaluate. 
                    Defaults to the Money OS / Capital OS idea.
        
        Returns:
            DebateResult containing all agent responses and final verdict.
        """
        start_time = time.time()
        
        if product is None:
            product = DEFAULT_PRODUCT_IDEA
        
        self._log("\n" + "═" * 60)
        self._log("STARTING MULTI-AGENT DEBATE")
        self._log(f"Product: {product.name}")
        self._log("═" * 60 + "\n")
        
        # Run each agent in sequence
        agent_responses: List[AgentResponse] = []
        
        for i, agent in enumerate(self.agents, 1):
            self._log(f"Running Agent {i}: {agent.name}...")
            response = agent.evaluate(product)
            agent_responses.append(response)
            self._log(f"  ✓ Agent {i} complete")
        
        # Run the final judge
        self._log(f"\nRunning Agent 6: {self.judge.name}...")
        judge_verdict = self.judge.evaluate_debate(product, agent_responses)
        self._log(f"  ✓ Final Judge complete")
        
        execution_time = time.time() - start_time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._log(f"\nDebate completed in {execution_time:.2f} seconds")
        
        return DebateResult(
            product=product,
            agent_responses=agent_responses,
            judge_verdict=judge_verdict,
            execution_time_seconds=execution_time,
            timestamp=timestamp
        )


def run_default_debate(verbose: bool = True) -> DebateResult:
    """
    Convenience function to run the debate with default settings.
    
    Returns:
        DebateResult with the complete evaluation.
    """
    orchestrator = DebateOrchestrator(verbose=verbose)
    return orchestrator.run_debate()


def run_custom_debate(
    name: str,
    description: str,
    problem_statement: str,
    solution_buckets: List[str],
    key_features: List[str],
    target_users: List[str],
    revenue_model: str,
    differentiators: List[str],
    verbose: bool = True
) -> DebateResult:
    """
    Run a debate with a custom product idea.
    
    Args:
        name: Product/concept name
        description: Detailed description
        problem_statement: The problem being solved
        solution_buckets: Key solution components
        key_features: List of main features
        target_users: Target user segments
        revenue_model: How the business makes money
        differentiators: What makes this different
        verbose: Whether to print progress
    
    Returns:
        DebateResult with the complete evaluation.
    """
    product = FinancialProductIdea(
        name=name,
        description=description,
        problem_statement=problem_statement,
        solution_buckets=solution_buckets,
        key_features=key_features,
        target_users=target_users,
        revenue_model=revenue_model,
        differentiators=differentiators
    )
    
    orchestrator = DebateOrchestrator(verbose=verbose)
    return orchestrator.run_debate(product)
