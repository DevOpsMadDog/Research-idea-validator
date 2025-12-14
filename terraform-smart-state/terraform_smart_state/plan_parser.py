"""Parse and visualize Terraform plan output."""

import json
import os
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ChangeAction(str, Enum):
    """Terraform change actions."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    REPLACE = "replace"
    NO_OP = "no-op"
    READ = "read"


@dataclass
class ResourceChange:
    """Represents a resource change in Terraform plan."""
    address: str
    action: ChangeAction
    resource_type: str
    resource_name: str
    provider: str
    before: Optional[Dict] = None
    after: Optional[Dict] = None
    replaced_by: Optional[str] = None
    requires_replacement: bool = False
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class PlanParser:
    """Parse and analyze Terraform plan output."""
    
    def __init__(self, plan_file: Optional[str] = None):
        """
        Initialize plan parser.
        
        Args:
            plan_file: Path to plan JSON file. If None, will run terraform plan.
        """
        self.plan_file = plan_file
        self.plan_data: Optional[Dict] = None
        
    def generate_plan(self, terraform_dir: str = ".", output_file: str = "plan.json") -> str:
        """Generate Terraform plan and save as JSON."""
        cmd = [
            "terraform", "plan",
            "-out=tfplan",
            "-json"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=terraform_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Save plan output
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            
            return output_file
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to generate plan: {e.stderr}")
    
    def load_plan(self, plan_file: Optional[str] = None) -> Dict:
        """Load plan from JSON file."""
        plan_file = plan_file or self.plan_file
        if not plan_file or not os.path.exists(plan_file):
            raise FileNotFoundError(f"Plan file not found: {plan_file}")
        
        with open(plan_file, 'r') as f:
            # Terraform plan JSON is line-delimited JSON
            lines = f.readlines()
            plan_messages = []
            for line in lines:
                if line.strip():
                    plan_messages.append(json.loads(line))
            
            self.plan_data = {
                'messages': plan_messages,
                'resource_changes': self._extract_resource_changes(plan_messages),
            }
        
        return self.plan_data
    
    def _extract_resource_changes(self, messages: List[Dict]) -> List[ResourceChange]:
        """Extract resource changes from plan messages."""
        changes = []
        
        for msg in messages:
            if msg.get('type') == 'planned_change':
                change = msg.get('change', {})
                actions = change.get('actions', [])
                
                if not actions or actions == ['no-op']:
                    continue
                
                address = change.get('address', '')
                resource_type = change.get('type', '')
                
                # Parse address to get resource name
                parts = address.split('.')
                resource_name = parts[-1] if len(parts) > 1 else address
                
                # Determine primary action
                if 'create' in actions:
                    action = ChangeAction.CREATE
                elif 'delete' in actions:
                    action = ChangeAction.DELETE
                elif 'replace' in actions:
                    action = ChangeAction.REPLACE
                elif 'update' in actions:
                    action = ChangeAction.UPDATE
                else:
                    action = ChangeAction.NO_OP
                
                resource_change = ResourceChange(
                    address=address,
                    action=action,
                    resource_type=resource_type,
                    resource_name=resource_name,
                    provider=change.get('provider_name', 'unknown'),
                    before=change.get('before'),
                    after=change.get('after'),
                    requires_replacement='replace' in actions,
                    dependencies=change.get('required_replace', []),
                )
                
                changes.append(resource_change)
        
        return changes
    
    def get_changes_by_action(self) -> Dict[ChangeAction, List[ResourceChange]]:
        """Group changes by action type."""
        if not self.plan_data:
            self.load_plan()
        
        grouped = {}
        for change in self.plan_data['resource_changes']:
            if change.action not in grouped:
                grouped[change.action] = []
            grouped[change.action].append(change)
        
        return grouped
    
    def get_changes_by_provider(self) -> Dict[str, List[ResourceChange]]:
        """Group changes by provider."""
        if not self.plan_data:
            self.load_plan()
        
        grouped = {}
        for change in self.plan_data['resource_changes']:
            provider = change.provider
            if provider not in grouped:
                grouped[provider] = []
            grouped[provider].append(change)
        
        return grouped
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph from changes."""
        if not self.plan_data:
            self.load_plan()
        
        graph = {}
        for change in self.plan_data['resource_changes']:
            graph[change.address] = change.dependencies
        
        return graph
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the plan."""
        if not self.plan_data:
            self.load_plan()
        
        changes = self.plan_data['resource_changes']
        by_action = self.get_changes_by_action()
        
        return {
            'total_changes': len(changes),
            'to_create': len(by_action.get(ChangeAction.CREATE, [])),
            'to_update': len(by_action.get(ChangeAction.UPDATE, [])),
            'to_delete': len(by_action.get(ChangeAction.DELETE, [])),
            'to_replace': len(by_action.get(ChangeAction.REPLACE, [])),
            'providers': list(set(c.provider for c in changes)),
        }
