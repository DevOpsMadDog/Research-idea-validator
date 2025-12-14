"""Track Terraform apply operations and handle partial failures."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum

from .plan_parser import ResourceChange, ChangeAction


class ResourceStatus(str, Enum):
    """Resource status during apply."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ApplyResult:
    """Result of a resource apply operation."""
    address: str
    status: ResourceStatus
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    output: Optional[Dict] = None


class ApplyTracker:
    """Track Terraform apply operations and handle partial failures."""
    
    def __init__(self, session_file: str = ".terraform-apply-session.json"):
        """
        Initialize apply tracker.
        
        Args:
            session_file: File to store apply session data.
        """
        self.session_file = session_file
        self.session_data: Dict[str, Any] = {
            'session_id': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat(),
            'planned_resources': [],
            'results': {},
            'failed_resources': [],
            'succeeded_resources': [],
            'pending_resources': [],
        }
        self._load_session()
    
    def _load_session(self):
        """Load existing session data if available."""
        if Path(self.session_file).exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
            except Exception:
                # Start fresh if session file is corrupted
                pass
    
    def _save_session(self):
        """Save session data to file."""
        self.session_data['last_updated'] = datetime.now().isoformat()
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def start_apply(self, planned_resources: List[ResourceChange]):
        """Start tracking a new apply operation."""
        self.session_data = {
            'session_id': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat(),
            'planned_resources': [r.address for r in planned_resources],
            'results': {},
            'failed_resources': [],
            'succeeded_resources': [],
            'pending_resources': [r.address for r in planned_resources],
        }
        self._save_session()
    
    def record_resource_start(self, address: str):
        """Record that a resource apply has started."""
        if address not in self.session_data['results']:
            self.session_data['results'][address] = {
                'status': ResourceStatus.IN_PROGRESS.value,
                'started_at': datetime.now().isoformat(),
            }
        else:
            self.session_data['results'][address]['status'] = ResourceStatus.IN_PROGRESS.value
            self.session_data['results'][address]['started_at'] = datetime.now().isoformat()
        
        if address in self.session_data['pending_resources']:
            self.session_data['pending_resources'].remove(address)
        
        self._save_session()
    
    def record_resource_success(self, address: str, output: Optional[Dict] = None):
        """Record successful resource apply."""
        if address not in self.session_data['results']:
            self.session_data['results'][address] = {}
        
        self.session_data['results'][address].update({
            'status': ResourceStatus.SUCCESS.value,
            'completed_at': datetime.now().isoformat(),
            'output': output,
        })
        
        if address not in self.session_data['succeeded_resources']:
            self.session_data['succeeded_resources'].append(address)
        
        if address in self.session_data['failed_resources']:
            self.session_data['failed_resources'].remove(address)
        
        self._save_session()
    
    def record_resource_failure(self, address: str, error_message: str):
        """Record failed resource apply."""
        if address not in self.session_data['results']:
            self.session_data['results'][address] = {}
        
        self.session_data['results'][address].update({
            'status': ResourceStatus.FAILED.value,
            'completed_at': datetime.now().isoformat(),
            'error_message': error_message,
        })
        
        if address not in self.session_data['failed_resources']:
            self.session_data['failed_resources'].append(address)
        
        self._save_session()
    
    def parse_apply_output(self, output: str) -> Dict[str, ApplyResult]:
        """Parse terraform apply output to extract resource statuses."""
        results = {}
        lines = output.split('\n')
        
        current_resource = None
        in_error = False
        error_buffer = []
        
        for line in lines:
            # Look for resource creation/update messages
            if 'Creating...' in line or 'Modifying...' in line:
                # Extract resource address
                parts = line.split()
                if len(parts) > 1:
                    current_resource = parts[1].strip()
                    self.record_resource_start(current_resource)
            
            elif 'Creation complete' in line or 'Modifications complete' in line:
                if current_resource:
                    self.record_resource_success(current_resource)
                    current_resource = None
            
            elif 'Error:' in line or 'failed' in line.lower():
                in_error = True
                error_buffer.append(line)
                if current_resource:
                    error_msg = '\n'.join(error_buffer)
                    self.record_resource_failure(current_resource, error_msg)
                    current_resource = None
                    error_buffer = []
                    in_error = False
            
            elif in_error:
                error_buffer.append(line)
        
        return results
    
    def get_failed_resources(self) -> List[str]:
        """Get list of failed resource addresses."""
        return self.session_data.get('failed_resources', [])
    
    def get_succeeded_resources(self) -> List[str]:
        """Get list of succeeded resource addresses."""
        return self.session_data.get('succeeded_resources', [])
    
    def get_pending_resources(self) -> List[str]:
        """Get list of pending resource addresses."""
        return self.session_data.get('pending_resources', [])
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary."""
        total = len(self.session_data.get('planned_resources', []))
        succeeded = len(self.session_data.get('succeeded_resources', []))
        failed = len(self.session_data.get('failed_resources', []))
        pending = len(self.session_data.get('pending_resources', []))
        
        return {
            'total': total,
            'succeeded': succeeded,
            'failed': failed,
            'pending': pending,
            'progress_percent': ((succeeded + failed) / total * 100) if total > 0 else 0,
            'session_id': self.session_data.get('session_id'),
            'started_at': self.session_data.get('started_at'),
        }
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Get comprehensive report of all resources."""
        return {
            'summary': self.get_status_summary(),
            'succeeded': [
                {
                    'address': addr,
                    'result': self.session_data['results'].get(addr, {})
                }
                for addr in self.session_data.get('succeeded_resources', [])
            ],
            'failed': [
                {
                    'address': addr,
                    'result': self.session_data['results'].get(addr, {})
                }
                for addr in self.session_data.get('failed_resources', [])
            ],
            'pending': self.session_data.get('pending_resources', []),
        }
    
    def clear_session(self):
        """Clear current session data."""
        if Path(self.session_file).exists():
            Path(self.session_file).unlink()
        self.session_data = {
            'session_id': datetime.now().isoformat(),
            'started_at': datetime.now().isoformat(),
            'planned_resources': [],
            'results': {},
            'failed_resources': [],
            'succeeded_resources': [],
            'pending_resources': [],
        }
