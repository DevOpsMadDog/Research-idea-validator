"""
Collection Infrastructure Service
Unified collection system for all financial products
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid

from core.database import db


class CollectionMethod(Enum):
    UPI_AUTOPAY = "upi_autopay"
    NACH_MANDATE = "nach_mandate"
    SALARY_DEDUCTION = "salary_deduction"
    PLATFORM_DEDUCTION = "platform_deduction"
    MANUAL_PAYMENT = "manual_payment"


class CollectionStatus(Enum):
    SCHEDULED = "scheduled"
    INITIATED = "initiated"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    RETRYING = "retrying"
    WAIVED = "waived"


@dataclass
class CollectionSchedule:
    """Represents a scheduled collection"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    product_type: str = ""
    product_id: str = ""
    
    amount: float = 0.0
    due_date: datetime = field(default_factory=datetime.now)
    
    method: CollectionMethod = CollectionMethod.UPI_AUTOPAY
    status: CollectionStatus = CollectionStatus.SCHEDULED
    
    retry_count: int = 0
    max_retries: int = 3
    
    mandate_id: Optional[str] = None
    upi_vpa: Optional[str] = None
    bank_account: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    last_attempt: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    notes: str = ""


@dataclass
class Mandate:
    """UPI/NACH mandate for recurring collections"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    
    type: str = ""  # upi_autopay, nach
    
    max_amount: float = 0.0
    frequency: str = "monthly"  # daily, weekly, monthly, on_demand
    
    upi_vpa: Optional[str] = None
    bank_account: Optional[str] = None
    ifsc: Optional[str] = None
    
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


class CollectionService:
    """
    Unified Collection Infrastructure
    
    Supports:
    1. UPI AutoPay mandates
    2. NACH (bank) mandates
    3. Salary deduction (employer integration)
    4. Platform deduction (gig workers)
    5. Income-based repayment (% of earnings)
    
    This is critical infrastructure that reduces collection costs
    from 5-10% to <1% of amount collected.
    """
    
    def __init__(self):
        self._mandates: Dict[str, Mandate] = {}
        self._schedules: Dict[str, CollectionSchedule] = {}
        self._collections: Dict[str, List[Dict]] = {}  # user_id -> collection history
    
    def create_upi_mandate(
        self,
        user_id: str,
        upi_vpa: str,
        max_amount: float,
        frequency: str = "monthly",
        duration_months: int = 12
    ) -> Mandate:
        """
        Create UPI AutoPay mandate
        User authorizes recurring debits up to max_amount
        """
        mandate = Mandate(
            user_id=user_id,
            type="upi_autopay",
            max_amount=max_amount,
            frequency=frequency,
            upi_vpa=upi_vpa,
            end_date=datetime.now() + timedelta(days=duration_months * 30),
        )
        
        self._mandates[mandate.id] = mandate
        db.store_product('mandate', mandate.id, {
            'id': mandate.id,
            'user_id': user_id,
            'type': mandate.type,
            'max_amount': max_amount,
            'upi_vpa': upi_vpa,
            'is_active': True,
        })
        
        return mandate
    
    def create_nach_mandate(
        self,
        user_id: str,
        bank_account: str,
        ifsc: str,
        max_amount: float,
        frequency: str = "monthly",
        duration_months: int = 24
    ) -> Mandate:
        """
        Create NACH (bank) mandate
        More reliable for larger amounts, longer duration
        """
        mandate = Mandate(
            user_id=user_id,
            type="nach",
            max_amount=max_amount,
            frequency=frequency,
            bank_account=bank_account,
            ifsc=ifsc,
            end_date=datetime.now() + timedelta(days=duration_months * 30),
        )
        
        self._mandates[mandate.id] = mandate
        db.store_product('mandate', mandate.id, {
            'id': mandate.id,
            'user_id': user_id,
            'type': mandate.type,
            'max_amount': max_amount,
            'bank_account': bank_account[-4:],  # Store only last 4 digits
            'is_active': True,
        })
        
        return mandate
    
    def schedule_collection(
        self,
        user_id: str,
        product_type: str,
        product_id: str,
        amount: float,
        due_date: datetime,
        mandate_id: Optional[str] = None,
        method: CollectionMethod = CollectionMethod.UPI_AUTOPAY
    ) -> CollectionSchedule:
        """
        Schedule a collection for a specific date
        """
        schedule = CollectionSchedule(
            user_id=user_id,
            product_type=product_type,
            product_id=product_id,
            amount=amount,
            due_date=due_date,
            method=method,
            mandate_id=mandate_id,
        )
        
        self._schedules[schedule.id] = schedule
        
        return schedule
    
    def schedule_recurring_collections(
        self,
        user_id: str,
        product_type: str,
        product_id: str,
        amount: float,
        frequency: str,
        start_date: datetime,
        num_collections: int,
        mandate_id: Optional[str] = None
    ) -> List[CollectionSchedule]:
        """
        Schedule multiple recurring collections
        """
        schedules = []
        current_date = start_date
        
        for i in range(num_collections):
            schedule = self.schedule_collection(
                user_id=user_id,
                product_type=product_type,
                product_id=product_id,
                amount=amount,
                due_date=current_date,
                mandate_id=mandate_id,
            )
            schedules.append(schedule)
            
            # Calculate next date based on frequency
            if frequency == "daily":
                current_date += timedelta(days=1)
            elif frequency == "weekly":
                current_date += timedelta(weeks=1)
            elif frequency == "monthly":
                current_date += timedelta(days=30)
            elif frequency == "quarterly":
                current_date += timedelta(days=90)
        
        return schedules
    
    def execute_collection(
        self, 
        schedule_id: str
    ) -> Dict[str, Any]:
        """
        Execute a scheduled collection
        In production, this would integrate with UPI/NACH APIs
        """
        schedule = self._schedules.get(schedule_id)
        if not schedule:
            return {'success': False, 'error': 'Schedule not found'}
        
        schedule.status = CollectionStatus.INITIATED
        schedule.last_attempt = datetime.now()
        
        # Simulate collection (in production: real API calls)
        result = self._simulate_collection(schedule)
        
        if result['success']:
            schedule.status = CollectionStatus.SUCCESSFUL
            schedule.completed_at = datetime.now()
            
            # Record in history
            if schedule.user_id not in self._collections:
                self._collections[schedule.user_id] = []
            
            self._collections[schedule.user_id].append({
                'schedule_id': schedule_id,
                'amount': schedule.amount,
                'date': datetime.now().isoformat(),
                'method': schedule.method.value,
                'product_type': schedule.product_type,
                'product_id': schedule.product_id,
            })
        else:
            schedule.retry_count += 1
            if schedule.retry_count >= schedule.max_retries:
                schedule.status = CollectionStatus.FAILED
            else:
                schedule.status = CollectionStatus.RETRYING
        
        return result
    
    def process_income_based_collection(
        self,
        user_id: str,
        product_id: str,
        income_amount: float,
        income_share_percentage: float
    ) -> Dict[str, Any]:
        """
        Process income-based collection (for ISAs)
        Deducts percentage of income when salary is credited
        """
        collection_amount = income_amount * income_share_percentage
        
        # Find or create collection schedule
        schedule = CollectionSchedule(
            user_id=user_id,
            product_type='isa',
            product_id=product_id,
            amount=collection_amount,
            due_date=datetime.now(),
            method=CollectionMethod.SALARY_DEDUCTION,
        )
        
        self._schedules[schedule.id] = schedule
        
        # Execute immediately
        result = self.execute_collection(schedule.id)
        result['income_amount'] = income_amount
        result['income_share_percentage'] = income_share_percentage
        result['collection_amount'] = collection_amount
        
        return result
    
    def get_user_mandates(self, user_id: str) -> List[Mandate]:
        """Get all active mandates for a user"""
        return [m for m in self._mandates.values() 
                if m.user_id == user_id and m.is_active]
    
    def get_pending_collections(self, user_id: str) -> List[CollectionSchedule]:
        """Get pending collections for a user"""
        return [s for s in self._schedules.values()
                if s.user_id == user_id and s.status == CollectionStatus.SCHEDULED]
    
    def get_collection_history(self, user_id: str) -> List[Dict]:
        """Get collection history for a user"""
        return self._collections.get(user_id, [])
    
    def get_collection_stats(self, user_id: str) -> Dict[str, Any]:
        """Get collection statistics for a user"""
        history = self._collections.get(user_id, [])
        pending = self.get_pending_collections(user_id)
        
        total_collected = sum(c['amount'] for c in history)
        total_pending = sum(s.amount for s in pending)
        
        return {
            'total_collected': total_collected,
            'total_pending': total_pending,
            'collection_count': len(history),
            'pending_count': len(pending),
            'active_mandates': len(self.get_user_mandates(user_id)),
        }
    
    def revoke_mandate(self, mandate_id: str) -> bool:
        """Revoke a mandate"""
        mandate = self._mandates.get(mandate_id)
        if mandate:
            mandate.is_active = False
            return True
        return False
    
    # Private methods
    
    def _simulate_collection(self, schedule: CollectionSchedule) -> Dict[str, Any]:
        """
        Simulate collection for demo
        In production: integrate with UPI/NACH APIs
        """
        import random
        
        # Simulate 90% success rate
        success = random.random() < 0.90
        
        if success:
            return {
                'success': True,
                'amount': schedule.amount,
                'transaction_id': str(uuid.uuid4()),
                'method': schedule.method.value,
                'timestamp': datetime.now().isoformat(),
            }
        else:
            failure_reasons = [
                'Insufficient balance',
                'Technical error',
                'Mandate limit exceeded',
                'Account dormant',
            ]
            return {
                'success': False,
                'error': random.choice(failure_reasons),
                'retry_scheduled': schedule.retry_count < schedule.max_retries,
            }


# Global service instance
collection_service = CollectionService()
