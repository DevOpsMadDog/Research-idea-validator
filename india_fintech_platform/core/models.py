"""
Core Data Models for India FinTech Platform
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid


class KYCStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class EmploymentType(Enum):
    SALARIED = "salaried"
    SELF_EMPLOYED = "self_employed"
    GIG_WORKER = "gig_worker"
    DAILY_WAGE = "daily_wage"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"


class ProductType(Enum):
    EWA = "earned_wage_access"
    ISA = "income_share_agreement"
    PARAMETRIC_INSURANCE = "parametric_insurance"
    MICRO_INVESTMENT = "micro_investment"
    GIG_BENEFITS = "gig_worker_benefits"


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"


@dataclass
class User:
    """Represents a platform user"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Basic Info
    name: str = ""
    phone: str = ""  # Primary identifier in India
    email: Optional[str] = None
    
    # KYC
    aadhaar_hash: Optional[str] = None  # Hashed Aadhaar for privacy
    pan: Optional[str] = None
    kyc_status: KYCStatus = KYCStatus.PENDING
    kyc_verified_at: Optional[datetime] = None
    
    # Demographics
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    
    # Employment
    employment_type: EmploymentType = EmploymentType.UNEMPLOYED
    employer_name: Optional[str] = None
    monthly_income: float = 0.0
    income_verified: bool = False
    
    # Account
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    # Preferences
    preferred_language: str = "hi"  # Hindi default
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'kyc_status': self.kyc_status.value,
            'employment_type': self.employment_type.value,
            'monthly_income': self.monthly_income,
            'state': self.state,
            'created_at': self.created_at.isoformat(),
        }


@dataclass
class CreditProfile:
    """Universal Credit Identity for a user"""
    user_id: str
    
    # Scores (300-900 range, like CIBIL)
    composite_score: int = 550
    payment_history_score: int = 550
    credit_utilization_score: int = 550
    income_stability_score: int = 550
    
    # Derived from various data sources
    upi_transaction_count_30d: int = 0
    upi_transaction_value_30d: float = 0.0
    average_balance: float = 0.0
    income_regularity_index: float = 0.0  # 0-1, higher is more regular
    
    # Risk Indicators
    existing_loan_count: int = 0
    total_outstanding: float = 0.0
    recent_defaults: int = 0
    debt_to_income_ratio: float = 0.0
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    data_sources: List[str] = field(default_factory=list)
    confidence_level: float = 0.5  # 0-1, how confident we are in the score
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'composite_score': self.composite_score,
            'payment_history_score': self.payment_history_score,
            'credit_utilization_score': self.credit_utilization_score,
            'income_stability_score': self.income_stability_score,
            'debt_to_income_ratio': self.debt_to_income_ratio,
            'confidence_level': self.confidence_level,
            'last_updated': self.last_updated.isoformat(),
        }


@dataclass
class Transaction:
    """Represents a financial transaction"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    
    # Transaction details
    type: str = ""  # credit, debit, transfer
    amount: float = 0.0
    currency: str = "INR"
    
    # Parties
    source_account: Optional[str] = None
    destination_account: Optional[str] = None
    
    # Context
    product_type: Optional[ProductType] = None
    product_id: Optional[str] = None
    description: str = ""
    
    # Status
    status: TransactionStatus = TransactionStatus.PENDING
    
    # Timing
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    # Reference
    upi_ref: Optional[str] = None
    bank_ref: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'amount': self.amount,
            'status': self.status.value,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
        }


@dataclass
class AuditLog:
    """Audit trail for all actions"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
