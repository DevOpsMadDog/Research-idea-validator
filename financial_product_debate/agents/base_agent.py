"""
Base Agent class for the multi-agent debate system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from ..config import AgentConfig, FinancialProductIdea


@dataclass
class AgentResponse:
    """Structured response from a debate agent."""
    
    agent_id: int
    agent_name: str
    initial_position: List[str]  # Max 5 bullets
    fatal_risks: List[str]  # Top 3
    change_conditions: List[str]  # What would change my mind
    raw_analysis: str = ""  # Full analysis text
    
    def format_output(self) -> str:
        """Format the response for display."""
        output = []
        output.append(f"\n{'═' * 80}")
        output.append(f"AGENT {self.agent_id} — {self.agent_name}")
        output.append(f"{'═' * 80}\n")
        
        output.append("📌 INITIAL POSITION")
        output.append("─" * 40)
        for i, point in enumerate(self.initial_position[:5], 1):
            output.append(f"  {i}. {point}")
        output.append("")
        
        output.append("⚠️  TOP 3 FATAL RISKS")
        output.append("─" * 40)
        for i, risk in enumerate(self.fatal_risks[:3], 1):
            output.append(f"  {i}. {risk}")
        output.append("")
        
        output.append("🔄 WHAT WOULD CHANGE MY MIND")
        output.append("─" * 40)
        for condition in self.change_conditions:
            output.append(f"  • {condition}")
        output.append("")
        
        return "\n".join(output)


class BaseAgent(ABC):
    """Base class for all debate agents."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.agent_id = config.agent_id
        self.name = config.name
        self.role = config.role
        self.persona = config.persona
        self.evaluation_criteria = config.evaluation_criteria
        self.adversarial_goal = config.adversarial_goal
        self.is_judge = config.is_judge
    
    def get_system_prompt(self) -> str:
        """Generate the system prompt for this agent."""
        return f"""You are {self.name}.

ROLE: {self.role}

PERSONA: {self.persona}

YOUR EVALUATION CRITERIA:
{chr(10).join(f"  • {c}" for c in self.evaluation_criteria)}

YOUR ADVERSARIAL GOAL:
{self.adversarial_goal}

HARD RULES:
• No optimism bias
• No vague language
• No founder sympathy
• Penalize regulatory ambiguity
• Decision > discussion
• Be specific and actionable
• Back claims with reasoning"""
    
    @abstractmethod
    def evaluate(self, product: FinancialProductIdea) -> AgentResponse:
        """Evaluate the financial product and return structured response."""
        pass
    
    def _create_response(
        self,
        initial_position: List[str],
        fatal_risks: List[str],
        change_conditions: List[str],
        raw_analysis: str = ""
    ) -> AgentResponse:
        """Helper to create a structured response."""
        return AgentResponse(
            agent_id=self.agent_id,
            agent_name=self.name,
            initial_position=initial_position[:5],
            fatal_risks=fatal_risks[:3],
            change_conditions=change_conditions,
            raw_analysis=raw_analysis
        )
