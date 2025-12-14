#!/usr/bin/env python3
"""
Run the Multi-Agent Debate for Financial Product Validation.

This is the main entry point for running the debate simulation.
Execute this file to evaluate the Money OS / Capital OS (India) concept.

Usage:
    python run_debate.py                    # Full output
    python run_debate.py --summary          # Executive summary only
    python run_debate.py --output report.txt  # Save to file
"""

import sys
import os

# Add the workspace to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from financial_product_debate.orchestrator import run_default_debate, run_custom_debate


def main():
    """Run the multi-agent debate with the default Money OS concept."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              MULTI-AGENT DEBATE: FINANCIAL PRODUCT VALIDATION                ║
║                     India Focus | Adversarial Evaluation                     ║
║                                                                              ║
║  This simulation runs 6 independent AI agents to evaluate a financial       ║
║  product idea. Each agent has a specific persona and adversarial goal.      ║
║                                                                              ║
║  Agents:                                                                     ║
║    1. Skeptical VC (India Focus) - Goal: Kill the idea                      ║
║    2. SEBI & Regulatory Expert - Goal: Find regulatory landmines            ║
║    3. Behavioral Finance Expert - Goal: Expose behavior gaps                ║
║    4. Execution & Ops Realist - Goal: Reveal hidden complexity              ║
║    5. Bull Case Architect - Goal: Build rigorous defense                    ║
║    6. Final Judge - Goal: Synthesize and decide                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Run the debate
    result = run_default_debate(verbose=True)
    
    # Print full output
    print(result.format_full_output())
    
    # Also print a clean summary
    print("\n" + "=" * 80)
    print("QUICK REFERENCE SUMMARY")
    print("=" * 80)
    print(result.get_summary())
    
    return result


def run_custom_evaluation():
    """
    Example of running with a custom product idea.
    Modify this function to evaluate your own financial product concepts.
    """
    
    result = run_custom_debate(
        name="Your Product Name",
        description="Detailed description of your product...",
        problem_statement="What problem does it solve?",
        solution_buckets=["Bucket 1", "Bucket 2", "Bucket 3"],
        key_features=["Feature 1", "Feature 2", "Feature 3"],
        target_users=["User Segment 1", "User Segment 2"],
        revenue_model="How you make money",
        differentiators=["What makes you different"],
        verbose=True
    )
    
    print(result.format_full_output())
    return result


if __name__ == "__main__":
    main()
