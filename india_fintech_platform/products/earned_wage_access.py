"""
Earned Wage Access (EWA) Product
Access wages earned but not yet paid - without predatory interest

This is the #1 priority product from the AI Debate:
- Highest impact for daily wage/gig workers
- Technology exists (UPI mandates)
- Low regulatory complexity
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

from core.models import User, Transaction, TransactionStatus
from core.database import db
from core.config import config
from services.credit_identity import credit_identity_service
from services.income_verification import income_verification_service
from services.collection import collection_service, CollectionMethod


class EWAStatus(Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DISBURSED = "disbursed"
    PARTIALLY_REPAID = "partially_repaid"
    FULLY_REPAID = "fully_repaid"
    OVERDUE = "overdue"
    DEFAULTED = "defaulted"


@dataclass
class EWARequest:
    """Request for earned wage access"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    
    # Request details
    requested_amount: float = 0.0
    approved_amount: float = 0.0
    
    # Earnings context
    earned_wages: float = 0.0  # Wages earned so far this period
    pay_period_end: datetime = field(default_factory=datetime.now)
    employer_id: Optional[str] = None
    employer_name: Optional[str] = None
    
    # Status
    status: EWAStatus = EWAStatus.PENDING_APPROVAL
    
    # Fees (transparent, NOT interest)
    processing_fee: float = 0.0
    express_fee: float = 0.0  # For instant disbursement
    total_fee: float = 0.0
    
    # Repayment
    repayment_amount: float = 0.0  # Amount to be collected on payday
    repayment_date: datetime = field(default_factory=datetime.now)
    amount_repaid: float = 0.0
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    disbursed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # UPI details for disbursement
    upi_vpa: Optional[str] = None
    bank_account: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'requested_amount': self.requested_amount,
            'approved_amount': self.approved_amount,
            'earned_wages': self.earned_wages,
            'status': self.status.value,
            'processing_fee': self.processing_fee,
            'total_fee': self.total_fee,
            'repayment_amount': self.repayment_amount,
            'repayment_date': self.repayment_date.isoformat(),
            'created_at': self.created_at.isoformat(),
        }


class EarnedWageAccessProduct:
    """
    Earned Wage Access Product
    
    Allows workers to access a portion of wages they've already earned
    but haven't been paid yet. Key features:
    
    1. NOT a loan - accessing your own money
    2. Transparent flat fee (no hidden interest)
    3. Automatic repayment on payday
    4. Works for salaried, gig workers, daily wage
    5. Builds credit history for the unbanked
    
    This solves the income volatility problem for 400M+ Indians.
    """
    
    def __init__(self):
        self.max_advance_percentage = config.ewa_max_advance_percentage
        self.processing_fee_percentage = config.ewa_processing_fee_percentage
        self.max_amount = config.ewa_max_amount
        self.product_type = "ewa"
    
    def check_eligibility(self, user_id: str) -> Dict[str, Any]:
        """
        Check if user is eligible for EWA
        
        Requirements:
        - Valid KYC
        - Income verification (any source)
        - No outstanding EWA overdue
        - Minimum credit score (very low bar - 400)
        """
        user = db.get_user(user_id)
        if not user:
            return {'eligible': False, 'reason': 'User not found'}
        
        # Check KYC
        if user.kyc_status.value != 'verified':
            return {'eligible': False, 'reason': 'KYC verification required'}
        
        # Check income
        if user.monthly_income <= 0:
            income_check = income_verification_service.get_verification(user_id)
            if not income_check or income_check.verified_amount <= 0:
                return {'eligible': False, 'reason': 'Income verification required'}
        
        # Check credit score (very low bar)
        credit_decision = credit_identity_service.get_credit_decision(
            user_id, self.product_type, 1000
        )
        if not credit_decision.get('approved'):
            return {
                'eligible': False, 
                'reason': 'Credit check failed',
                'details': credit_decision.get('reasons', [])
            }
        
        # Check for overdue EWA
        existing_ewa = self._get_active_ewa(user_id)
        if existing_ewa and existing_ewa.status == EWAStatus.OVERDUE:
            return {'eligible': False, 'reason': 'Outstanding overdue advance'}
        
        # Calculate available amount
        monthly_income = user.monthly_income or credit_decision.get('max_amount', 0)
        days_into_period = datetime.now().day
        earned_estimate = (monthly_income / 30) * days_into_period
        max_available = min(
            earned_estimate * self.max_advance_percentage,
            self.max_amount
        )
        
        return {
            'eligible': True,
            'max_available': max_available,
            'earned_wages_estimate': earned_estimate,
            'credit_score': credit_decision.get('credit_score'),
            'processing_fee_rate': self.processing_fee_percentage,
        }
    
    def request_advance(
        self,
        user_id: str,
        amount: float,
        upi_vpa: Optional[str] = None,
        express_disbursal: bool = False
    ) -> EWARequest:
        """
        Request an earned wage advance
        """
        # Check eligibility
        eligibility = self.check_eligibility(user_id)
        if not eligibility['eligible']:
            request = EWARequest(
                user_id=user_id,
                requested_amount=amount,
                status=EWAStatus.PENDING_APPROVAL,
            )
            db.store_product(self.product_type, request.id, {
                **request.to_dict(),
                'rejection_reason': eligibility['reason']
            })
            return request
        
        # Calculate approved amount
        max_available = eligibility['max_available']
        approved_amount = min(amount, max_available)
        
        # Calculate fees
        processing_fee = approved_amount * self.processing_fee_percentage
        express_fee = approved_amount * 0.005 if express_disbursal else 0  # 0.5% for express
        total_fee = processing_fee + express_fee
        
        # Calculate repayment
        repayment_amount = approved_amount + total_fee
        
        # Calculate repayment date (next payday - assume end of month)
        today = datetime.now()
        if today.day >= 28:
            repayment_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
        else:
            repayment_date = today.replace(day=28)
        
        # Create request
        user = db.get_user(user_id)
        request = EWARequest(
            user_id=user_id,
            requested_amount=amount,
            approved_amount=approved_amount,
            earned_wages=eligibility['earned_wages_estimate'],
            pay_period_end=repayment_date,
            employer_name=user.employer_name if user else None,
            status=EWAStatus.APPROVED,
            processing_fee=processing_fee,
            express_fee=express_fee,
            total_fee=total_fee,
            repayment_amount=repayment_amount,
            repayment_date=repayment_date,
            upi_vpa=upi_vpa,
            approved_at=datetime.now(),
        )
        
        db.store_product(self.product_type, request.id, request.to_dict())
        
        return request
    
    def disburse_advance(self, request_id: str) -> Dict[str, Any]:
        """
        Disburse the approved advance to user's account
        """
        request_data = db.get_product(self.product_type, request_id)
        if not request_data:
            return {'success': False, 'error': 'Request not found'}
        
        if request_data['status'] != EWAStatus.APPROVED.value:
            return {'success': False, 'error': f"Invalid status: {request_data['status']}"}
        
        # Simulate disbursement (in production: actual UPI/bank transfer)
        transaction = Transaction(
            user_id=request_data['user_id'],
            type='credit',
            amount=request_data['approved_amount'],
            description=f"EWA Disbursement - {request_id[:8]}",
            status=TransactionStatus.COMPLETED,
        )
        db.create_transaction(transaction)
        
        # Update request status
        request_data['status'] = EWAStatus.DISBURSED.value
        request_data['disbursed_at'] = datetime.now().isoformat()
        db.update_product(self.product_type, request_id, request_data)
        
        # Schedule repayment collection
        collection_service.schedule_collection(
            user_id=request_data['user_id'],
            product_type=self.product_type,
            product_id=request_id,
            amount=request_data['repayment_amount'],
            due_date=datetime.fromisoformat(request_data['repayment_date']),
            method=CollectionMethod.UPI_AUTOPAY,
        )
        
        return {
            'success': True,
            'transaction_id': transaction.id,
            'amount': request_data['approved_amount'],
            'repayment_date': request_data['repayment_date'],
            'repayment_amount': request_data['repayment_amount'],
        }
    
    def process_repayment(
        self, 
        request_id: str, 
        amount: float
    ) -> Dict[str, Any]:
        """
        Process repayment for an EWA advance
        """
        request_data = db.get_product(self.product_type, request_id)
        if not request_data:
            return {'success': False, 'error': 'Request not found'}
        
        if request_data['status'] not in [
            EWAStatus.DISBURSED.value, 
            EWAStatus.PARTIALLY_REPAID.value,
            EWAStatus.OVERDUE.value
        ]:
            return {'success': False, 'error': f"Invalid status for repayment"}
        
        # Update repayment
        current_repaid = request_data.get('amount_repaid', 0)
        new_repaid = current_repaid + amount
        request_data['amount_repaid'] = new_repaid
        
        # Check if fully repaid
        if new_repaid >= request_data['repayment_amount']:
            request_data['status'] = EWAStatus.FULLY_REPAID.value
            request_data['completed_at'] = datetime.now().isoformat()
            
            # Update credit score positively
            credit_identity_service.update_from_upi_data(
                request_data['user_id'],
                [{'amount': amount, 'type': 'debit', 'timestamp': datetime.now().isoformat()}]
            )
        else:
            request_data['status'] = EWAStatus.PARTIALLY_REPAID.value
        
        db.update_product(self.product_type, request_id, request_data)
        
        # Record transaction
        transaction = Transaction(
            user_id=request_data['user_id'],
            type='debit',
            amount=amount,
            description=f"EWA Repayment - {request_id[:8]}",
            status=TransactionStatus.COMPLETED,
        )
        db.create_transaction(transaction)
        
        return {
            'success': True,
            'amount_paid': amount,
            'total_repaid': new_repaid,
            'remaining': max(0, request_data['repayment_amount'] - new_repaid),
            'status': request_data['status'],
        }
    
    def get_user_ewa_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all EWA requests for a user"""
        return db.get_user_products(self.product_type, user_id)
    
    def get_ewa_stats(self, user_id: str) -> Dict[str, Any]:
        """Get EWA statistics for a user"""
        history = self.get_user_ewa_history(user_id)
        
        total_advanced = sum(r.get('approved_amount', 0) for r in history)
        total_fees = sum(r.get('total_fee', 0) for r in history)
        total_repaid = sum(r.get('amount_repaid', 0) for r in history)
        
        completed = [r for r in history if r.get('status') == EWAStatus.FULLY_REPAID.value]
        active = [r for r in history if r.get('status') in [
            EWAStatus.DISBURSED.value, EWAStatus.PARTIALLY_REPAID.value
        ]]
        
        return {
            'total_advances': len(history),
            'completed_advances': len(completed),
            'active_advances': len(active),
            'total_advanced': total_advanced,
            'total_fees_paid': total_fees,
            'total_repaid': total_repaid,
            'effective_apr': (total_fees / total_advanced * 12 * 100) if total_advanced > 0 else 0,
        }
    
    # Private methods
    
    def _get_active_ewa(self, user_id: str) -> Optional[EWARequest]:
        """Get any active (not fully repaid) EWA for user"""
        history = self.get_user_ewa_history(user_id)
        for ewa_data in history:
            if ewa_data.get('status') in [
                EWAStatus.DISBURSED.value,
                EWAStatus.PARTIALLY_REPAID.value,
                EWAStatus.OVERDUE.value,
            ]:
                return EWARequest(**{k: v for k, v in ewa_data.items() 
                                    if k in EWARequest.__dataclass_fields__})
        return None


# Global product instance
ewa_product = EarnedWageAccessProduct()
