"""Parse and enhance Terraform state files."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class StateParser:
    """Parse and manage Terraform state files with enhanced metadata."""
    
    def __init__(self, state_file: Optional[str] = None):
        """
        Initialize state parser.
        
        Args:
            state_file: Path to terraform.tfstate file. If None, searches for it.
        """
        self.state_file = state_file or self._find_state_file()
        self.state_data: Optional[Dict] = None
        self.enhanced_metadata: Dict[str, Any] = {}
        
    def _find_state_file(self) -> Optional[str]:
        """Find terraform.tfstate file in current directory."""
        current_dir = Path.cwd()
        state_file = current_dir / "terraform.tfstate"
        if state_file.exists():
            return str(state_file)
        return None
    
    def load_state(self) -> Dict:
        """Load and parse Terraform state file."""
        if not self.state_file or not os.path.exists(self.state_file):
            raise FileNotFoundError(f"State file not found: {self.state_file}")
        
        with open(self.state_file, 'r') as f:
            self.state_data = json.load(f)
        
        return self.state_data
    
    def get_resources(self) -> List[Dict]:
        """Extract all resources from state."""
        if not self.state_data:
            self.load_state()
        
        resources = []
        if 'resources' in self.state_data:
            for resource in self.state_data['resources']:
                for instance in resource.get('instances', []):
                    resources.append({
                        'type': resource.get('type', 'unknown'),
                        'name': resource.get('name', 'unknown'),
                        'provider': resource.get('provider', 'unknown'),
                        'attributes': instance.get('attributes', {}),
                        'dependencies': instance.get('dependencies', []),
                        'schema_version': instance.get('schema_version', 0),
                    })
        
        return resources
    
    def get_resource_by_address(self, address: str) -> Optional[Dict]:
        """Get a specific resource by its address."""
        resources = self.get_resources()
        for resource in resources:
            resource_address = f"{resource['type']}.{resource['name']}"
            if address in resource_address or resource_address == address:
                return resource
        return None
    
    def add_metadata(self, resource_address: str, metadata: Dict[str, Any]):
        """Add custom metadata to a resource."""
        if resource_address not in self.enhanced_metadata:
            self.enhanced_metadata[resource_address] = {}
        
        self.enhanced_metadata[resource_address].update({
            **metadata,
            'last_updated': datetime.now().isoformat(),
        })
    
    def get_resource_status(self, resource_address: str) -> Dict[str, Any]:
        """Get comprehensive status for a resource."""
        resource = self.get_resource_by_address(resource_address)
        metadata = self.enhanced_metadata.get(resource_address, {})
        
        return {
            'resource': resource,
            'metadata': metadata,
            'exists': resource is not None,
            'status': metadata.get('status', 'unknown'),
            'created_at': metadata.get('created_at'),
            'last_updated': metadata.get('last_updated'),
            'apply_attempts': metadata.get('apply_attempts', 0),
            'last_error': metadata.get('last_error'),
        }
    
    def save_enhanced_state(self, output_file: Optional[str] = None):
        """Save enhanced state with metadata."""
        output_file = output_file or "terraform.enhanced.tfstate"
        
        enhanced_state = {
            'terraform_version': self.state_data.get('version', 0),
            'serial': self.state_data.get('serial', 0),
            'lineage': self.state_data.get('lineage'),
            'resources': self.state_data.get('resources', []),
            'enhanced_metadata': self.enhanced_metadata,
            'generated_at': datetime.now().isoformat(),
        }
        
        with open(output_file, 'w') as f:
            json.dump(enhanced_state, f, indent=2)
        
        return output_file
