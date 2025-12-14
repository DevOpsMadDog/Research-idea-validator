#!/usr/bin/env python3
"""
Visualization system for AI Agent Debate results
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
from datetime import datetime


class DebateVisualizer:
    """Creates visualizations from debate results"""
    
    def __init__(self, results_file: str):
        with open(results_file, 'r') as f:
            self.data = json.load(f)
    
    def plot_agent_performance(self, output_file: str = "agent_performance.png"):
        """Plot agent performance across rounds"""
        agent_scores = defaultdict(list)
        rounds = []
        
        for round_data in self.data['rounds']:
            round_num = round_data['round_number']
            rounds.append(round_num)
            
            for arg in round_data['arguments']:
                agent_scores[arg['agent']].append(arg['intensity'] * 10)
        
        plt.figure(figsize=(12, 6))
        for agent, scores in agent_scores.items():
            plt.plot(rounds, scores[:len(rounds)], marker='o', label=agent, linewidth=2)
        
        plt.xlabel('Round Number', fontsize=12, fontweight='bold')
        plt.ylabel('Performance Score', fontsize=12, fontweight='bold')
        plt.title('AI Agent Performance Across Debate Rounds', fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Saved performance chart to {output_file}")
    
    def plot_intensity_heatmap(self, output_file: str = "intensity_heatmap.png"):
        """Create heatmap of argument intensity"""
        agent_names = []
        round_intensities = defaultdict(lambda: defaultdict(int))
        
        for round_data in self.data['rounds']:
            round_num = round_data['round_number']
            for arg in round_data['arguments']:
                agent = arg['agent']
                if agent not in agent_names:
                    agent_names.append(agent)
                round_intensities[round_num][agent] = arg['intensity']
        
        # Create matrix
        matrix = []
        for agent in agent_names:
            row = []
            for round_num in sorted(round_intensities.keys()):
                row.append(round_intensities[round_num].get(agent, 0))
            matrix.append(row)
        
        plt.figure(figsize=(10, 6))
        plt.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=10)
        plt.colorbar(label='Intensity Level')
        plt.yticks(range(len(agent_names)), agent_names)
        plt.xticks(range(len(sorted(round_intensities.keys()))), 
                   [f"Round {r}" for r in sorted(round_intensities.keys())])
        plt.xlabel('Debate Round', fontsize=12, fontweight='bold')
        plt.ylabel('AI Agent', fontsize=12, fontweight='bold')
        plt.title('Argument Intensity Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Saved intensity heatmap to {output_file}")
    
    def plot_final_scores(self, output_file: str = "final_scores.png"):
        """Plot final agent scores"""
        judgment = self.data['final_judgment']
        agents = list(judgment['agent_scores'].keys())
        scores = list(judgment['agent_scores'].values())
        
        colors = plt.cm.viridis([s/max(scores) for s in scores])
        
        plt.figure(figsize=(10, 6))
        bars = plt.barh(agents, scores, color=colors)
        plt.xlabel('Final Score', fontsize=12, fontweight='bold')
        plt.ylabel('AI Agent', fontsize=12, fontweight='bold')
        plt.title('Final Agent Scores - Debate Winner', fontsize=14, fontweight='bold')
        
        # Add value labels
        for i, (agent, score) in enumerate(zip(agents, scores)):
            plt.text(score + 1, i, f'{score:.1f}', va='center', fontweight='bold')
        
        # Highlight winner
        winner = judgment['overall_winner']
        if winner in agents:
            idx = agents.index(winner)
            bars[idx].set_edgecolor('gold')
            bars[idx].set_linewidth(3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Saved final scores chart to {output_file}")
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n📊 Generating visualizations...")
        self.plot_agent_performance()
        self.plot_intensity_heatmap()
        self.plot_final_scores()
        print("\n✅ All visualizations generated!")


if __name__ == "__main__":
    import sys
    results_file = sys.argv[1] if len(sys.argv) > 1 else "debate_results.json"
    viz = DebateVisualizer(results_file)
    viz.generate_all_visualizations()
