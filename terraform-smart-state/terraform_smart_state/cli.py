"""CLI interface for Terraform Smart State."""

import click
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from .state_parser import StateParser
from .plan_parser import PlanParser
from .apply_tracker import ApplyTracker
from .visualizer import PlanVisualizer


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Terraform Smart State - Enhanced Terraform state management and visualization."""
    pass


@cli.command()
@click.option('--state-file', '-s', help='Path to terraform.tfstate file')
@click.option('--output', '-o', help='Output file for enhanced state')
def enhance_state(state_file: Optional[str], output: Optional[str]):
    """Enhance Terraform state file with metadata."""
    try:
        parser = StateParser(state_file)
        parser.load_state()
        
        resources = parser.get_resources()
        console.print(f"[green]✓[/green] Loaded {len(resources)} resources from state")
        
        output_file = parser.save_enhanced_state(output)
        console.print(f"[green]✓[/green] Enhanced state saved to: {output_file}")
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--plan-file', '-p', help='Path to plan JSON file')
@click.option('--terraform-dir', '-d', default='.', help='Terraform directory')
@click.option('--generate', '-g', is_flag=True, help='Generate new plan')
def visualize_plan(plan_file: Optional[str], terraform_dir: str, generate: bool):
    """Visualize Terraform plan in a readable format."""
    try:
        parser = PlanParser(plan_file)
        
        if generate or not plan_file:
            console.print("[yellow]Generating Terraform plan...[/yellow]")
            plan_file = parser.generate_plan(terraform_dir)
            console.print(f"[green]✓[/green] Plan saved to: {plan_file}")
        
        parser.load_plan(plan_file)
        
        visualizer = PlanVisualizer()
        visualizer.visualize_plan(parser)
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--plan-file', '-p', help='Path to plan JSON file')
@click.option('--terraform-dir', '-d', default='.', help='Terraform directory')
@click.option('--generate', '-g', is_flag=True, help='Generate new plan')
@click.option('--auto-apply', '-a', is_flag=True, help='Automatically run terraform apply')
def apply(plan_file: Optional[str], terraform_dir: str, generate: bool, auto_apply: bool):
    """Track Terraform apply operation with comprehensive status reporting."""
    try:
        # Parse plan
        parser = PlanParser(plan_file)
        
        if generate or not plan_file:
            console.print("[yellow]Generating Terraform plan...[/yellow]")
            plan_file = parser.generate_plan(terraform_dir)
        
        parser.load_plan(plan_file)
        changes = parser.plan_data['resource_changes']
        
        # Initialize tracker
        tracker = ApplyTracker()
        tracker.start_apply(changes)
        
        console.print(f"[green]✓[/green] Tracking apply for {len(changes)} resources")
        
        if auto_apply:
            console.print("[yellow]Running terraform apply...[/yellow]")
            try:
                result = subprocess.run(
                    ["terraform", "apply", "-auto-approve", "-json"],
                    cwd=terraform_dir,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                # Parse output
                tracker.parse_apply_output(result.stdout + result.stderr)
                
                # Show status
                visualizer = PlanVisualizer()
                visualizer.visualize_apply_status(tracker)
                
                if result.returncode != 0:
                    console.print(f"[red]✗[/red] Apply completed with errors")
                    sys.exit(result.returncode)
                else:
                    console.print(f"[green]✓[/green] Apply completed successfully")
            except subprocess.CalledProcessError as e:
                console.print(f"[red]✗[/red] Apply failed: {e}")
                visualizer = PlanVisualizer()
                visualizer.visualize_apply_status(tracker)
                sys.exit(1)
        else:
            console.print("[yellow]Use 'terraform apply' and then run 'tss status' to see results[/yellow]")
            console.print("[yellow]Or use --auto-apply flag to run apply automatically[/yellow]")
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--session-file', '-s', default='.terraform-apply-session.json', help='Session file path')
def status(session_file: str):
    """Show status of current or last apply operation."""
    try:
        tracker = ApplyTracker(session_file)
        
        if not Path(session_file).exists():
            console.print("[yellow]No active apply session found[/yellow]")
            return
        
        visualizer = PlanVisualizer()
        visualizer.visualize_apply_status(tracker)
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--session-file', '-s', default='.terraform-apply-session.json', help='Session file path')
@click.option('--format', '-f', type=click.Choice(['json', 'table']), default='table', help='Output format')
def report(session_file: str, format: str):
    """Generate comprehensive report of apply operation."""
    try:
        tracker = ApplyTracker(session_file)
        
        if not Path(session_file).exists():
            console.print("[yellow]No active apply session found[/yellow]")
            return
        
        report_data = tracker.get_comprehensive_report()
        
        if format == 'json':
            console.print(json.dumps(report_data, indent=2))
        else:
            visualizer = PlanVisualizer()
            visualizer.visualize_apply_status(tracker)
        
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--session-file', '-s', default='.terraform-apply-session.json', help='Session file path')
def clear_session(session_file: str):
    """Clear current apply session."""
    try:
        tracker = ApplyTracker(session_file)
        tracker.clear_session()
        console.print(f"[green]✓[/green] Session cleared")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
