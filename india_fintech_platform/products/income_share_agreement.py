"""
Income Share Agreement (ISA) Product
Pay for education as a percentage of future income

This is the controversial but high-potential product from the AI Debate:
- Aligns incentives between education providers and students
- Students pay nothing upfront
- Payment only when earning above threshold
- Capped at 2x education cost
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


class ISAStatus(Enum):
    APPLICATION = "application"
    EDUCATION_IN_PROGRESS = "education_in_progress"
    GRACE_PERIOD = "grace_period"
    REPAYMENT_ACTIVE = "repayment_active"
    REPAYMENT_PAUSED = "repayment_paused"  # If income below threshold
    COMPLETED = "completed"
    CAPPED_OUT = "capped_out"  # Hit 2x cap
    DEFAULTED = "defaulted"


@dataclass
class ISAContract:
    """Income Share Agreement contract"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    
    # Education details
    education_provider_id: str = ""
    education_provider_name: str = ""
    program_name: str = ""
    program_duration_months: int = 0
    
    # Funding
    education_cost: float = 0.0
    funded_amount: float = 0.0  # May be partial funding
    
    # ISA Terms
    income_share_percentage: float = 0.15  # 15% default
    payment_duration_months: int = 48  # 4 years
    minimum_income_threshold: float = 300000.0  # ₹3 LPA - no payment below this
    payment_cap_multiplier: float = 2.0  # Max 2x funded amount
    
    # Calculated caps
    payment_cap: float = 0.0  # funded_amount * cap_multiplier
    
    # Status tracking
    status: ISAStatus = ISAStatus.APPLICATION
    
    # Payment tracking
    total_payments_made: float = 0.0
    payments_count: int = 0
    last_payment_date: Optional[datetime] = None
    
    # Timeline
    program_start_date: Optional[datetime] = None
    program_end_date: Optional[datetime] = None
    grace_period_end: Optional[datetime] = None
    repayment_start_date: Optional[datetime] = None
    repayment_end_date: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'education_provider_name': self.education_provider_name,
            'program_name': self.program_name,
            'program_duration_months': self.program_duration_months,
            'education_cost': self.education_cost,
            'funded_amount': self.funded_amount,
            'income_share_percentage': self.income_share_percentage,
            'payment_duration_months': self.payment_duration_months,
            'minimum_income_threshold': self.minimum_income_threshold,
            'payment_cap': self.payment_cap,
            'status': self.status.value,
            'total_payments_made': self.total_payments_made,
            'payments_count': self.payments_count,
            'created_at': self.created_at.isoformat(),
        }


@dataclass
class ISAPayment:
    """Individual ISA payment record"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    contract_id: str = ""
    user_id: str = ""
    
    # Income that triggered this payment
    income_month: str = ""  # YYYY-MM format
    gross_income: float = 0.0
    
    # Calculation
    income_share_percentage: float = 0.15
    calculated_payment: float = 0.0
    actual_payment: float = 0.0  # May be less if cap reached
    
    # Status
    status: str = "pending"  # pending, completed, failed, waived
    
    # Timestamps
    due_date: datetime = field(default_factory=datetime.now)
    paid_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'income_month': self.income_month,
            'gross_income': self.gross_income,
            'calculated_payment': self.calculated_payment,
            'actual_payment': self.actual_payment,
            'status': self.status,
            'due_date': self.due_date.isoformat(),
        }


class IncomeShareAgreementProduct:
    """
    Income Share Agreement Product
    
    Revolutionary education financing that:
    1. Requires $0 upfront from student
    2. Payment is percentage of income (typically 15%)
    3. Only pay when earning above threshold (₹3 LPA)
    4. Capped at 2x education cost (consumer protection)
    5. Aligns incentives - school only profits if student succeeds
    
    Regulatory considerations (from debate):
    - Currently in sandbox/pilot phase
    - Legal structure: Revenue-based financing
    - Requires RBI coordination
    """
    
    def __init__(self):
        self.default_income_share = config.isa_income_share_percentage
        self.default_duration = config.isa_payment_duration_months
        self.default_threshold = config.isa_minimum_income_threshold
        self.default_cap_multiplier = config.isa_cap_multiplier
        self.product_type = "isa"
    
    def check_eligibility(
        self, 
        user_id: str, 
        program_cost: float
    ) -> Dict[str, Any]:
        """
        Check if user is eligible for ISA
        
        Requirements:
        - Valid KYC
        - Accepted into eligible education program
        - No existing ISA in default
        - Credit score above minimum (500)
        - Age 18-40
        """
        user = db.get_user(user_id)
        if not user:
            return {'eligible': False, 'reason': 'User not found'}
        
        # Check KYC
        if user.kyc_status.value != 'verified':
            return {'eligible': False, 'reason': 'KYC verification required'}
        
        # Check age
        if user.date_of_birth:
            age = (datetime.now().date() - user.date_of_birth).days // 365
            if age < 18:
                return {'eligible': False, 'reason': 'Must be 18 or older'}
            if age > 40:
                return {'eligible': False, 'reason': 'Age limit exceeded (40 years)'}
        
        # Check credit score
        credit_decision = credit_identity_service.get_credit_decision(
            user_id, self.product_type, program_cost
        )
        if not credit_decision.get('approved'):
            return {
                'eligible': False,
                'reason': 'Credit assessment failed',
                'details': credit_decision.get('reasons', [])
            }
        
        # Check for existing defaulted ISA
        existing_isas = db.get_user_products(self.product_type, user_id)
        for isa in existing_isas:
            if isa.get('status') == ISAStatus.DEFAULTED.value:
                return {'eligible': False, 'reason': 'Existing ISA in default'}
        
        # Calculate terms
        income_share = self.default_income_share
        payment_cap = program_cost * self.default_cap_multiplier
        
        # Estimate monthly payment if earning ₹10 LPA
        example_salary = 1000000 / 12  # ₹10 LPA monthly
        example_payment = example_salary * income_share
        
        return {
            'eligible': True,
            'max_funding': min(program_cost, credit_decision.get('max_amount', 500000)),
            'terms': {
                'income_share_percentage': income_share * 100,
                'payment_duration_months': self.default_duration,
                'minimum_income_threshold': self.default_threshold,
                'payment_cap': payment_cap,
            },
            'example': {
                'at_10_lpa': {
                    'monthly_payment': example_payment,
                    'annual_payment': example_payment * 12,
                }
            },
            'credit_score': credit_decision.get('credit_score'),
        }
    
    def create_contract(
        self,
        user_id: str,
        education_provider_id: str,
        education_provider_name: str,
        program_name: str,
        program_duration_months: int,
        education_cost: float,
        funded_amount: Optional[float] = None,
        custom_income_share: Optional[float] = None,
    ) -> ISAContract:
        """
        Create an ISA contract
        """
        # Check eligibility first
        eligibility = self.check_eligibility(user_id, education_cost)
        if not eligibility['eligible']:
            raise ValueError(f"User not eligible: {eligibility['reason']}")
        
        # Use defaults or custom values
        income_share = custom_income_share or self.default_income_share
        funding = funded_amount or min(education_cost, eligibility['max_funding'])
        payment_cap = funding * self.default_cap_multiplier
        
        contract = ISAContract(
            user_id=user_id,
            education_provider_id=education_provider_id,
            education_provider_name=education_provider_name,
            program_name=program_name,
            program_duration_months=program_duration_months,
            education_cost=education_cost,
            funded_amount=funding,
            income_share_percentage=income_share,
            payment_duration_months=self.default_duration,
            minimum_income_threshold=self.default_threshold,
            payment_cap_multiplier=self.default_cap_multiplier,
            payment_cap=payment_cap,
            status=ISAStatus.APPLICATION,
        )
        
        db.store_product(self.product_type, contract.id, contract.to_dict())
        
        return contract
    
    def activate_contract(
        self, 
        contract_id: str,
        program_start_date: datetime
    ) -> Dict[str, Any]:
        """
        Activate contract when student enrolls
        Disburses funds to education provider
        """
        contract_data = db.get_product(self.product_type, contract_id)
        if not contract_data:
            return {'success': False, 'error': 'Contract not found'}
        
        if contract_data['status'] != ISAStatus.APPLICATION.value:
            return {'success': False, 'error': f"Invalid status: {contract_data['status']}"}
        
        # Calculate key dates
        program_end = program_start_date + timedelta(days=contract_data['program_duration_months'] * 30)
        grace_end = program_end + timedelta(days=90)  # 3 month grace period
        repayment_end = grace_end + timedelta(days=contract_data['payment_duration_months'] * 30)
        
        # Update contract
        contract_data.update({
            'status': ISAStatus.EDUCATION_IN_PROGRESS.value,
            'program_start_date': program_start_date.isoformat(),
            'program_end_date': program_end.isoformat(),
            'grace_period_end': grace_end.isoformat(),
            'repayment_start_date': grace_end.isoformat(),
            'repayment_end_date': repayment_end.isoformat(),
            'updated_at': datetime.now().isoformat(),
        })
        
        db.update_product(self.product_type, contract_id, contract_data)
        
        # Create disbursement transaction (to education provider)
        transaction = Transaction(
            user_id=contract_data['user_id'],
            type='disbursement',
            amount=contract_data['funded_amount'],
            description=f"ISA Disbursement to {contract_data['education_provider_name']}",
            status=TransactionStatus.COMPLETED,
        )
        db.create_transaction(transaction)
        
        return {
            'success': True,
            'contract_id': contract_id,
            'funded_amount': contract_data['funded_amount'],
            'program_end_date': program_end.isoformat(),
            'repayment_start_date': grace_end.isoformat(),
        }
    
    def start_repayment(self, contract_id: str) -> Dict[str, Any]:
        """
        Transition contract to repayment phase
        Called automatically after grace period or manually
        """
        contract_data = db.get_product(self.product_type, contract_id)
        if not contract_data:
            return {'success': False, 'error': 'Contract not found'}
        
        if contract_data['status'] not in [
            ISAStatus.EDUCATION_IN_PROGRESS.value,
            ISAStatus.GRACE_PERIOD.value
        ]:
            return {'success': False, 'error': f"Invalid status: {contract_data['status']}"}
        
        contract_data['status'] = ISAStatus.REPAYMENT_ACTIVE.value
        contract_data['updated_at'] = datetime.now().isoformat()
        
        db.update_product(self.product_type, contract_id, contract_data)
        
        return {
            'success': True,
            'status': ISAStatus.REPAYMENT_ACTIVE.value,
            'income_share_percentage': contract_data['income_share_percentage'],
            'minimum_threshold': contract_data['minimum_income_threshold'],
            'payment_cap_remaining': contract_data['payment_cap'] - contract_data['total_payments_made'],
        }
    
    def process_income_event(
        self,
        contract_id: str,
        income_month: str,  # YYYY-MM
        gross_income: float
    ) -> ISAPayment:
        """
        Process an income event and calculate/collect ISA payment
        
        This is called when income is detected (from bank, employer, etc.)
        """
        contract_data = db.get_product(self.product_type, contract_id)
        if not contract_data:
            raise ValueError('Contract not found')
        
        if contract_data['status'] != ISAStatus.REPAYMENT_ACTIVE.value:
            raise ValueError(f"Contract not in repayment: {contract_data['status']}")
        
        # Annualize income to check threshold
        annual_income = gross_income * 12
        
        # Check if income below threshold
        if annual_income < contract_data['minimum_income_threshold']:
            payment = ISAPayment(
                contract_id=contract_id,
                user_id=contract_data['user_id'],
                income_month=income_month,
                gross_income=gross_income,
                income_share_percentage=contract_data['income_share_percentage'],
                calculated_payment=0,
                actual_payment=0,
                status='waived',
            )
            db.store_product('isa_payment', payment.id, payment.to_dict())
            return payment
        
        # Calculate payment
        calculated_payment = gross_income * contract_data['income_share_percentage']
        
        # Check against cap
        remaining_cap = contract_data['payment_cap'] - contract_data['total_payments_made']
        actual_payment = min(calculated_payment, remaining_cap)
        
        # Create payment record
        payment = ISAPayment(
            contract_id=contract_id,
            user_id=contract_data['user_id'],
            income_month=income_month,
            gross_income=gross_income,
            income_share_percentage=contract_data['income_share_percentage'],
            calculated_payment=calculated_payment,
            actual_payment=actual_payment,
            status='pending',
            due_date=datetime.now() + timedelta(days=7),
        )
        
        db.store_product('isa_payment', payment.id, payment.to_dict())
        
        # Schedule collection
        if actual_payment > 0:
            collection_service.schedule_collection(
                user_id=contract_data['user_id'],
                product_type=self.product_type,
                product_id=contract_id,
                amount=actual_payment,
                due_date=payment.due_date,
                method=CollectionMethod.SALARY_DEDUCTION,
            )
        
        # Update contract totals
        contract_data['total_payments_made'] += actual_payment
        contract_data['payments_count'] += 1
        contract_data['last_payment_date'] = datetime.now().isoformat()
        
        # Check if capped out
        if contract_data['total_payments_made'] >= contract_data['payment_cap']:
            contract_data['status'] = ISAStatus.CAPPED_OUT.value
        
        # Check if duration complete
        if contract_data.get('repayment_end_date'):
            repayment_end = datetime.fromisoformat(contract_data['repayment_end_date'])
            if datetime.now() >= repayment_end:
                contract_data['status'] = ISAStatus.COMPLETED.value
        
        contract_data['updated_at'] = datetime.now().isoformat()
        db.update_product(self.product_type, contract_id, contract_data)
        
        return payment
    
    def confirm_payment(self, payment_id: str) -> Dict[str, Any]:
        """Confirm that a payment was collected successfully"""
        payment_data = db.get_product('isa_payment', payment_id)
        if not payment_data:
            return {'success': False, 'error': 'Payment not found'}
        
        payment_data['status'] = 'completed'
        payment_data['paid_date'] = datetime.now().isoformat()
        
        db.update_product('isa_payment', payment_id, payment_data)
        
        # Update credit score
        credit_identity_service.update_from_upi_data(
            payment_data['user_id'],
            [{'amount': payment_data['actual_payment'], 'type': 'debit', 
              'timestamp': datetime.now().isoformat()}]
        )
        
        return {
            'success': True,
            'payment_id': payment_id,
            'amount': payment_data['actual_payment'],
        }
    
    def get_contract_summary(self, contract_id: str) -> Dict[str, Any]:
        """Get summary of ISA contract status"""
        contract_data = db.get_product(self.product_type, contract_id)
        if not contract_data:
            return {'error': 'Contract not found'}
        
        remaining = contract_data['payment_cap'] - contract_data['total_payments_made']
        progress = (contract_data['total_payments_made'] / contract_data['payment_cap']) * 100
        
        return {
            'contract_id': contract_id,
            'status': contract_data['status'],
            'funded_amount': contract_data['funded_amount'],
            'total_paid': contract_data['total_payments_made'],
            'remaining_to_cap': remaining,
            'progress_percentage': round(progress, 1),
            'payments_count': contract_data['payments_count'],
            'income_share_percentage': contract_data['income_share_percentage'] * 100,
            'minimum_threshold': contract_data['minimum_income_threshold'],
        }
    
    def get_user_contracts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all ISA contracts for a user"""
        return db.get_user_products(self.product_type, user_id)
    
    def simulate_repayment_schedule(
        self,
        funded_amount: float,
        expected_annual_income: float,
        income_share: float = 0.15,
    ) -> Dict[str, Any]:
        """
        Simulate repayment schedule for prospective students
        Helps them understand what they'll pay
        """
        monthly_income = expected_annual_income / 12
        monthly_payment = monthly_income * income_share
        payment_cap = funded_amount * self.default_cap_multiplier
        
        months_to_cap = payment_cap / monthly_payment if monthly_payment > 0 else float('inf')
        months_to_cap = min(months_to_cap, self.default_duration)
        
        total_payments = min(monthly_payment * self.default_duration, payment_cap)
        
        return {
            'funded_amount': funded_amount,
            'expected_annual_income': expected_annual_income,
            'income_share_percentage': income_share * 100,
            'monthly_payment': round(monthly_payment, 2),
            'payment_cap': payment_cap,
            'estimated_months_to_complete': round(months_to_cap, 1),
            'total_payments': round(total_payments, 2),
            'effective_cost_multiple': round(total_payments / funded_amount, 2),
            'below_threshold_months_free': expected_annual_income < self.default_threshold,
        }


# Global product instance
isa_product = IncomeShareAgreementProduct()
