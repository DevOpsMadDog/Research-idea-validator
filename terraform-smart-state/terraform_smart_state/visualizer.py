"""Visualize Terraform plans and state with rich formatting."""

from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box
from rich.text import Text

from .plan_parser import PlanParser, ResourceChange, ChangeAction
from .apply_tracker import ApplyTracker


class PlanVisualizer:
    """Visualize Terraform plans in a human-readable format."""
    
    def __init__(self):
        self.console = Console()
    
    def _get_action_color(self, action: ChangeAction) -> str:
        """Get color for action type."""
        colors = {
            ChangeAction.CREATE: "green",
            ChangeAction.UPDATE: "yellow",
            ChangeAction.DELETE: "red",
            ChangeAction.REPLACE: "magenta",
            ChangeAction.NO_OP: "dim",
        }
        return colors.get(action, "white")
    
    def _get_action_symbol(self, action: ChangeAction) -> str:
        """Get symbol for action type."""
        symbols = {
            ChangeAction.CREATE: "+",
            ChangeAction.UPDATE: "~",
            ChangeAction.DELETE: "-",
            ChangeAction.REPLACE: "±",
            ChangeAction.NO_OP: " ",
        }
        return symbols.get(action, "?")
    
    def visualize_plan(self, plan_parser: PlanParser):
        """Visualize Terraform plan in a formatted way."""
        if not plan_parser.plan_data:
            plan_parser.load_plan()
        
        # Summary panel
        summary = plan_parser.get_summary()
        summary_text = f"""
[bold]Total Changes:[/bold] {summary['total_changes']}
[green]To Create:[/green] {summary['to_create']}
[yellow]To Update:[/yellow] {summary['to_update']}
[red]To Delete:[/red] {summary['to_delete']}
[magenta]To Replace:[/magenta] {summary['to_replace']}
[bold]Providers:[/bold] {', '.join(summary['providers'])}
"""
        self.console.print(Panel(summary_text, title="Plan Summary", border_style="blue"))
        
        # Group by action
        by_action = plan_parser.get_changes_by_action()
        
        for action in [ChangeAction.CREATE, ChangeAction.UPDATE, ChangeAction.DELETE, ChangeAction.REPLACE]:
            if action not in by_action or not by_action[action]:
                continue
            
            changes = by_action[action]
            color = self._get_action_color(action)
            symbol = self._get_action_symbol(action)
            
            table = Table(
                title=f"{symbol} {action.value.upper()} ({len(changes)} resources)",
                box=box.ROUNDED,
                border_style=color,
                show_header=True,
                header_style=color
            )
            
            table.add_column("Resource Address", style="cyan", no_wrap=False)
            table.add_column("Type", style="dim")
            table.add_column("Provider", style="dim")
            table.add_column("Requires Replacement", style="yellow")
            
            for change in changes:
                table.add_row(
                    change.address,
                    change.resource_type,
                    change.provider,
                    "Yes" if change.requires_replacement else "No"
                )
            
            self.console.print("\n")
            self.console.print(table)
        
        # Group by provider
        by_provider = plan_parser.get_changes_by_provider()
        if len(by_provider) > 1:
            self.console.print("\n")
            provider_tree = Tree("📦 Changes by Provider")
            
            for provider, changes in by_provider.items():
                provider_branch = provider_tree.add(f"[bold]{provider}[/bold] ({len(changes)} changes)")
                for change in changes[:5]:  # Show first 5
                    action_color = self._get_action_color(change.action)
                    symbol = self._get_action_symbol(change.action)
                    provider_branch.add(f"[{action_color}]{symbol}[/{action_color}] {change.address}")
                if len(changes) > 5:
                    provider_branch.add(f"[dim]... and {len(changes) - 5} more[/dim]")
            
            self.console.print(provider_tree)
    
    def visualize_apply_status(self, tracker: ApplyTracker):
        """Visualize apply operation status."""
        report = tracker.get_comprehensive_report()
        summary = report['summary']
        
        # Progress bar
        progress = summary['progress_percent']
        progress_color = "green" if summary['failed'] == 0 else "yellow" if summary['failed'] < summary['total'] / 2 else "red"
        
        status_text = f"""
[bold]Session ID:[/bold] {summary['session_id']}
[bold]Started:[/bold] {summary['started_at']}

[bold]Progress:[/bold] [{progress_color}]{progress:.1f}%[/{progress_color}]
[green]✓ Succeeded:[/green] {summary['succeeded']}
[red]✗ Failed:[/red] {summary['failed']}
[yellow]⏳ Pending:[/yellow] {summary['pending']}
[bold]Total:[/bold] {summary['total']}
"""
        self.console.print(Panel(status_text, title="Apply Status", border_style=progress_color))
        
        # Failed resources
        if report['failed']:
            self.console.print("\n")
            failed_table = Table(
                title=f"❌ Failed Resources ({len(report['failed'])})",
                box=box.ROUNDED,
                border_style="red",
                show_header=True
            )
            failed_table.add_column("Resource Address", style="red")
            failed_table.add_column("Error", style="dim")
            
            for failed in report['failed']:
                error = failed['result'].get('error_message', 'Unknown error')
                # Truncate long errors
                if len(error) > 100:
                    error = error[:100] + "..."
                failed_table.add_row(failed['address'], error)
            
            self.console.print(failed_table)
        
        # Succeeded resources
        if report['succeeded']:
            self.console.print("\n")
            success_table = Table(
                title=f"✅ Succeeded Resources ({len(report['succeeded'])})",
                box=box.ROUNDED,
                border_style="green",
                show_header=True
            )
            success_table.add_column("Resource Address", style="green")
            success_table.add_column("Completed At", style="dim")
            
            for succeeded in report['succeeded']:
                completed = succeeded['result'].get('completed_at', 'Unknown')
                success_table.add_row(succeeded['address'], completed)
            
            self.console.print(success_table)
        
        # Pending resources
        if report['pending']:
            self.console.print("\n")
            pending_text = f"[yellow]⏳ Pending Resources ({len(report['pending'])}):[/yellow]\n"
            for addr in report['pending'][:10]:
                pending_text += f"  • {addr}\n"
            if len(report['pending']) > 10:
                pending_text += f"  ... and {len(report['pending']) - 10} more\n"
            
            self.console.print(Panel(pending_text, border_style="yellow"))
