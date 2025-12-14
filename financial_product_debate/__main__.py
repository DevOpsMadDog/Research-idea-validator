"""
Main entry point for running the multi-agent debate.

Usage:
    python -m financial_product_debate
    python -m financial_product_debate --summary
    python -m financial_product_debate --output report.txt
"""

import argparse
import sys
from .orchestrator import run_default_debate


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Debate System for Financial Product Validation (India)"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print only the executive summary instead of full output"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Save output to a file"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress messages"
    )
    
    args = parser.parse_args()
    
    # Run the debate
    result = run_default_debate(verbose=not args.quiet)
    
    # Generate output
    if args.summary:
        output = result.get_summary()
    else:
        output = result.format_full_output()
    
    # Print or save
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\nOutput saved to: {args.output}")
    else:
        print(output)
    
    # Return exit code based on verdict
    verdict_str = result.judge_verdict.verdict.value
    if "APPROVE" in verdict_str:
        return 0
    elif "CONDITIONAL" in verdict_str:
        return 1
    else:  # REJECT
        return 2


if __name__ == "__main__":
    sys.exit(main())
