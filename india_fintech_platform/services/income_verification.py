"""
Income Verification Service
Verifies and estimates income from multiple data sources
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

from core.models import User, EmploymentType
from core.database import db


class VerificationStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    ESTIMATED = "estimated"
    FAILED = "failed"


@dataclass
class IncomeVerification:
    user_id: str
    status: VerificationStatus
    verified_amount: float
    confidence: float
    sources: List[str]
    verification_date: datetime
    valid_until: datetime
    details: Dict[str, Any]


class IncomeVerificationService:
    """
    Verifies income through multiple channels:
    1. Bank account aggregator (salary credits)
    2. Employer verification (API/letter)
    3. GST returns (self-employed)
    4. UPI pattern analysis (estimation)
    5. Self-declaration with risk adjustment
    """
    
    def __init__(self):
        self._verifications: Dict[str, IncomeVerification] = {}
    
    def verify_from_bank_account(
        self, 
        user_id: str, 
        account_data: Dict[str, Any]
    ) -> IncomeVerification:
        """
        Verify income from bank account data
        Most reliable method - directly observes salary credits
        """
        transactions = account_data.get('transactions', [])
        
        # Find salary-like credits (regular, similar amounts, monthly)
        salary_credits = self._identify_salary_credits(transactions)
        
        if salary_credits:
            avg_salary = sum(s['amount'] for s in salary_credits) / len(salary_credits)
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.VERIFIED,
                verified_amount=avg_salary,
                confidence=0.95,
                sources=['bank_account_aggregator'],
                verification_date=datetime.now(),
                valid_until=datetime.now() + timedelta(days=90),
                details={
                    'method': 'salary_credit_analysis',
                    'samples': len(salary_credits),
                    'employer_name': salary_credits[0].get('sender', 'Unknown'),
                }
            )
        else:
            # Estimate from total credits
            total_credits = sum(
                t['amount'] for t in transactions 
                if t.get('type') == 'credit'
            )
            months = max(1, account_data.get('months_of_data', 3))
            estimated_monthly = total_credits / months
            
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.ESTIMATED,
                verified_amount=estimated_monthly,
                confidence=0.6,
                sources=['bank_account_aggregator'],
                verification_date=datetime.now(),
                valid_until=datetime.now() + timedelta(days=30),
                details={
                    'method': 'total_credit_estimation',
                    'total_credits': total_credits,
                    'months': months,
                }
            )
        
        self._verifications[user_id] = verification
        return verification
    
    def verify_from_employer(
        self, 
        user_id: str, 
        employer_data: Dict[str, Any]
    ) -> IncomeVerification:
        """
        Verify income through employer confirmation
        Requires employer API integration or document verification
        """
        salary = employer_data.get('monthly_salary', 0)
        employer_name = employer_data.get('employer_name', '')
        employment_start = employer_data.get('start_date')
        
        if salary > 0 and employer_name:
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.VERIFIED,
                verified_amount=salary,
                confidence=0.98,
                sources=['employer_verification'],
                verification_date=datetime.now(),
                valid_until=datetime.now() + timedelta(days=180),
                details={
                    'method': 'employer_api',
                    'employer_name': employer_name,
                    'employment_start': employment_start,
                    'designation': employer_data.get('designation', ''),
                }
            )
        else:
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.FAILED,
                verified_amount=0,
                confidence=0,
                sources=['employer_verification'],
                verification_date=datetime.now(),
                valid_until=datetime.now(),
                details={'error': 'Insufficient employer data'}
            )
        
        self._verifications[user_id] = verification
        return verification
    
    def verify_from_gst(
        self, 
        user_id: str, 
        gst_data: Dict[str, Any]
    ) -> IncomeVerification:
        """
        Verify income from GST returns
        For self-employed individuals and businesses
        """
        annual_turnover = gst_data.get('annual_turnover', 0)
        gst_number = gst_data.get('gstin', '')
        
        if annual_turnover > 0 and gst_number:
            # Estimate monthly income (assuming 30% margin for services)
            estimated_monthly = (annual_turnover * 0.3) / 12
            
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.VERIFIED,
                verified_amount=estimated_monthly,
                confidence=0.85,
                sources=['gst_returns'],
                verification_date=datetime.now(),
                valid_until=datetime.now() + timedelta(days=365),
                details={
                    'method': 'gst_analysis',
                    'gstin': gst_number,
                    'annual_turnover': annual_turnover,
                    'margin_assumed': 0.3,
                }
            )
        else:
            verification = IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.FAILED,
                verified_amount=0,
                confidence=0,
                sources=['gst_returns'],
                verification_date=datetime.now(),
                valid_until=datetime.now(),
                details={'error': 'No GST data available'}
            )
        
        self._verifications[user_id] = verification
        return verification
    
    def estimate_from_upi_pattern(
        self, 
        user_id: str, 
        upi_data: Dict[str, Any]
    ) -> IncomeVerification:
        """
        Estimate income from UPI transaction patterns
        Lower confidence but works for gig workers/daily wage
        """
        transactions = upi_data.get('transactions', [])
        
        # Separate incoming and outgoing
        incoming = [t for t in transactions if t.get('type') == 'credit']
        
        if not incoming:
            return IncomeVerification(
                user_id=user_id,
                status=VerificationStatus.FAILED,
                verified_amount=0,
                confidence=0,
                sources=['upi_pattern'],
                verification_date=datetime.now(),
                valid_until=datetime.now(),
                details={'error': 'No incoming transactions found'}
            )
        
        # Calculate average monthly incoming
        months = upi_data.get('months_of_data', 1)
        total_incoming = sum(t['amount'] for t in incoming)
        avg_monthly = total_incoming / max(1, months)
        
        # Analyze patterns for confidence
        regularity = self._calculate_income_regularity(incoming)
        
        verification = IncomeVerification(
            user_id=user_id,
            status=VerificationStatus.ESTIMATED,
            verified_amount=avg_monthly,
            confidence=0.4 + (regularity * 0.3),  # 40-70% confidence
            sources=['upi_pattern'],
            verification_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=15),
            details={
                'method': 'upi_pattern_analysis',
                'total_incoming': total_incoming,
                'months': months,
                'regularity_index': regularity,
                'transaction_count': len(incoming),
            }
        )
        
        self._verifications[user_id] = verification
        return verification
    
    def verify_for_gig_worker(
        self, 
        user_id: str, 
        platform_data: List[Dict[str, Any]]
    ) -> IncomeVerification:
        """
        Verify income for gig workers from platform data
        Aggregates across multiple platforms (Swiggy, Uber, etc.)
        """
        total_earnings = 0
        platforms = []
        
        for platform in platform_data:
            earnings = platform.get('monthly_earnings', 0)
            total_earnings += earnings
            platforms.append(platform.get('platform_name', 'Unknown'))
        
        verification = IncomeVerification(
            user_id=user_id,
            status=VerificationStatus.VERIFIED if platforms else VerificationStatus.FAILED,
            verified_amount=total_earnings,
            confidence=0.9 if len(platforms) > 0 else 0,
            sources=['gig_platform'] + platforms,
            verification_date=datetime.now(),
            valid_until=datetime.now() + timedelta(days=30),
            details={
                'method': 'gig_platform_aggregation',
                'platforms': platforms,
                'breakdown': {p.get('platform_name'): p.get('monthly_earnings') for p in platform_data}
            }
        )
        
        self._verifications[user_id] = verification
        return verification
    
    def get_verification(self, user_id: str) -> Optional[IncomeVerification]:
        """Get current income verification for user"""
        return self._verifications.get(user_id)
    
    def is_verification_valid(self, user_id: str) -> bool:
        """Check if existing verification is still valid"""
        verification = self._verifications.get(user_id)
        if not verification:
            return False
        return verification.valid_until > datetime.now()
    
    # Private helper methods
    
    def _identify_salary_credits(
        self, 
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify salary-like credit patterns"""
        credits = [t for t in transactions if t.get('type') == 'credit']
        
        if len(credits) < 3:
            return []
        
        # Group by approximate amount (within 10% variance)
        amount_groups: Dict[int, List[Dict]] = {}
        for credit in credits:
            amount = credit.get('amount', 0)
            bucket = round(amount, -3)  # Round to nearest 1000
            if bucket not in amount_groups:
                amount_groups[bucket] = []
            amount_groups[bucket].append(credit)
        
        # Find groups with regular monthly pattern
        salary_candidates = []
        for bucket, group in amount_groups.items():
            if len(group) >= 3 and bucket > 10000:  # At least 3 months, > ₹10K
                # Check if roughly monthly
                dates = sorted([
                    datetime.fromisoformat(t.get('timestamp', datetime.now().isoformat()))
                    for t in group
                ])
                
                # Average gap between credits
                if len(dates) > 1:
                    gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                    avg_gap = sum(gaps) / len(gaps)
                    
                    if 25 <= avg_gap <= 35:  # Monthly pattern
                        salary_candidates.extend(group)
        
        return salary_candidates
    
    def _calculate_income_regularity(
        self, 
        transactions: List[Dict[str, Any]]
    ) -> float:
        """Calculate how regular income transactions are (0-1)"""
        if len(transactions) < 2:
            return 0.0
        
        dates = sorted([
            datetime.fromisoformat(t.get('timestamp', datetime.now().isoformat()))
            for t in transactions
        ])
        
        # Calculate coefficient of variation of gaps
        gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        
        if not gaps:
            return 0.0
        
        avg_gap = sum(gaps) / len(gaps)
        variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)
        std_dev = variance ** 0.5
        
        # Lower CV = more regular
        cv = std_dev / avg_gap if avg_gap > 0 else float('inf')
        
        # Convert to 0-1 score (CV of 0 = perfect, CV of 1+ = irregular)
        regularity = max(0, 1 - cv)
        
        return regularity


# Global service instance
income_verification_service = IncomeVerificationService()
