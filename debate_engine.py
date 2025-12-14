"""
Multi-Agent Debate Engine
Manages intense debates between AI agents with scoring and argument tracking
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class DebatePhase(Enum):
    OPENING = "opening"
    REBUTTAL = "rebuttal"
    CROSS_EXAMINATION = "cross_examination"
    CLOSING = "closing"


@dataclass
class Argument:
    agent_id: str
    agent_name: str
    phase: str
    round_number: int
    content: str
    timestamp: str
    targets: List[str]  # Which agents/arguments this responds to
    strength_score: float = 0.0
    evidence_score: float = 0.0
    logic_score: float = 0.0
    
    def total_score(self) -> float:
        return self.strength_score + self.evidence_score + self.logic_score


@dataclass
class DebateRound:
    round_number: int
    phase: DebatePhase
    arguments: List[Argument]
    summary: str = ""
    
    def get_scores_by_agent(self) -> Dict[str, float]:
        scores = {}
        for arg in self.arguments:
            if arg.agent_id not in scores:
                scores[arg.agent_id] = 0.0
            scores[arg.agent_id] += arg.total_score()
        return scores


class DebateEngine:
    """Core debate engine managing multi-round debates with scoring"""
    
    def __init__(self, topic: str, max_rounds: int = 5):
        self.topic = topic
        self.max_rounds = max_rounds
        self.rounds: List[DebateRound] = []
        self.current_round = 0
        self.agents: List[Dict[str, Any]] = []
        self.judge_evaluations: List[Dict[str, Any]] = []
        self.start_time = datetime.now().isoformat()
        
    def register_agent(self, agent_id: str, agent_name: str, role: str, perspective: str):
        """Register an agent to participate in the debate"""
        self.agents.append({
            "id": agent_id,
            "name": agent_name,
            "role": role,
            "perspective": perspective,
            "total_score": 0.0,
            "arguments_made": 0
        })
        
    def start_round(self, phase: DebatePhase) -> int:
        """Start a new debate round"""
        self.current_round += 1
        new_round = DebateRound(
            round_number=self.current_round,
            phase=phase,
            arguments=[]
        )
        self.rounds.append(new_round)
        return self.current_round
    
    def add_argument(self, agent_id: str, agent_name: str, content: str, 
                     targets: List[str] = None) -> Argument:
        """Add an argument to the current round"""
        if not self.rounds:
            raise ValueError("No active round. Call start_round() first.")
        
        current = self.rounds[-1]
        argument = Argument(
            agent_id=agent_id,
            agent_name=agent_name,
            phase=current.phase.value,
            round_number=self.current_round,
            content=content,
            timestamp=datetime.now().isoformat(),
            targets=targets or []
        )
        current.arguments.append(argument)
        
        # Update agent stats
        for agent in self.agents:
            if agent["id"] == agent_id:
                agent["arguments_made"] += 1
                break
                
        return argument
    
    def score_argument(self, argument: Argument, strength: float, 
                       evidence: float, logic: float):
        """Score an argument on multiple dimensions"""
        argument.strength_score = max(0.0, min(10.0, strength))
        argument.evidence_score = max(0.0, min(10.0, evidence))
        argument.logic_score = max(0.0, min(10.0, logic))
        
        # Update agent total score
        for agent in self.agents:
            if agent["id"] == argument.agent_id:
                agent["total_score"] += argument.total_score()
                break
    
    def get_current_standings(self) -> List[Dict[str, Any]]:
        """Get current leaderboard"""
        sorted_agents = sorted(self.agents, key=lambda x: x["total_score"], reverse=True)
        return sorted_agents
    
    def get_debate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive debate summary"""
        return {
            "topic": self.topic,
            "start_time": self.start_time,
            "end_time": datetime.now().isoformat(),
            "total_rounds": len(self.rounds),
            "total_arguments": sum(len(r.arguments) for r in self.rounds),
            "participating_agents": len(self.agents),
            "final_standings": self.get_current_standings(),
            "rounds": [
                {
                    "round": r.round_number,
                    "phase": r.phase.value,
                    "arguments_count": len(r.arguments),
                    "scores_by_agent": r.get_scores_by_agent()
                }
                for r in self.rounds
            ]
        }
    
    def add_judge_evaluation(self, round_number: int, evaluation: Dict[str, Any]):
        """Add judge's evaluation for a round"""
        self.judge_evaluations.append({
            "round": round_number,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat()
        })
    
    def export_debate(self, filepath: str):
        """Export complete debate to JSON"""
        export_data = {
            "metadata": {
                "topic": self.topic,
                "start_time": self.start_time,
                "end_time": datetime.now().isoformat(),
                "total_rounds": len(self.rounds),
                "max_rounds": self.max_rounds
            },
            "agents": self.agents,
            "rounds": [
                {
                    "round_number": r.round_number,
                    "phase": r.phase.value,
                    "summary": r.summary,
                    "arguments": [asdict(arg) for arg in r.arguments]
                }
                for r in self.rounds
            ],
            "judge_evaluations": self.judge_evaluations,
            "final_standings": self.get_current_standings(),
            "summary": self.get_debate_summary()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return export_data
