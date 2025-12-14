"""
Agent modules for the multi-agent debate system.
"""

from .base_agent import BaseAgent, AgentResponse
from .skeptical_vc import SkepticalVCAgent
from .regulatory_expert import RegulatoryExpertAgent
from .behavioral_expert import BehavioralExpertAgent
from .execution_realist import ExecutionRealistAgent
from .bull_case import BullCaseAgent
from .final_judge import FinalJudgeAgent

__all__ = [
    "BaseAgent",
    "AgentResponse",
    "SkepticalVCAgent",
    "RegulatoryExpertAgent",
    "BehavioralExpertAgent",
    "ExecutionRealistAgent",
    "BullCaseAgent",
    "FinalJudgeAgent"
]
