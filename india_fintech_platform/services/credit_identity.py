"""
Universal Credit Identity Service
The foundational layer for all financial products

This service creates credit scores for the unbanked using alternative data:
- UPI transaction history
- Telecom/recharge patterns
- Utility bill payments
- Rental payments
- Employment verification
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import random
import math

from core.models import User, CreditProfile, Transaction, EmploymentType
from core.database import db
from core.config import config


@dataclass
class DataSource:
    """Represents a data source for credit scoring"""
    name: str
    weight: float
    confidence: float
    data: Dict[str, Any]


class CreditIdentityService:
    """
    Universal Credit Identity Service
    
    Creates credit scores for anyone with a smartphone, using:
    1. UPI transaction history
    2. Bank account aggregator data
    3. Telecom usage patterns
    4. Utility payment history
    5. Employment verification
    
    This is the 'missing infrastructure' identified in the AI debate.
    """
    
    def __init__(self):
        self.min_score = config.min_credit_score
        self.max_score = config.max_credit_score
        self.default_score = config.default_credit_score
    
    def create_profile(self, user: User) -> CreditProfile:
        """Create initial credit profile for a user"""
        profile = CreditProfile(
            user_id=user.id,
            composite_score=self.default_score,
            data_sources=[],
            confidence_level=0.1,  # Low confidence initially
        )
        
        # If user has income info, adjust baseline
        if user.monthly_income > 0:
            profile = self._adjust_for_income(profile, user.monthly_income)
        
        db.create_credit_profile(profile)
        return profile
    
    def get_or_create_profile(self, user_id: str) -> Optional[CreditProfile]:
        """Get existing profile or create new one"""
        profile = db.get_credit_profile(user_id)
        if profile:
            return profile
        
        user = db.get_user(user_id)
        if user:
            return self.create_profile(user)
        return None
    
    def update_from_upi_data(
        self, 
        user_id: str, 
        transactions: List[Dict[str, Any]]
    ) -> CreditProfile:
        """
        Update credit profile from UPI transaction history
        
        Key signals:
        - Transaction frequency (more = better)
        - Transaction consistency (regular patterns = better)
        - Average transaction size
        - Merchant diversity
        - Incoming vs outgoing ratio
        """
        profile = self.get_or_create_profile(user_id)
        if not profile:
            raise ValueError(f"User {user_id} not found")
        
        # Analyze transactions
        analysis = self._analyze_upi_transactions(transactions)
        
        # Update scores
        profile.upi_transaction_count_30d = analysis['count_30d']
        profile.upi_transaction_value_30d = analysis['value_30d']
        profile.income_regularity_index = analysis['regularity_index']
        
        # Adjust credit score components
        profile.payment_history_score = self._calculate_payment_score(analysis)
        profile.income_stability_score = self._calculate_stability_score(analysis)
        
        # Update composite score
        profile.composite_score = self._calculate_composite_score(profile)
        
        # Update metadata
        if 'upi' not in profile.data_sources:
            profile.data_sources.append('upi')
        profile.confidence_level = min(0.9, profile.confidence_level + 0.2)
        profile.last_updated = datetime.now()
        
        db.update_credit_profile(profile)
        return profile
    
    def update_from_bank_aggregator(
        self, 
        user_id: str, 
        account_data: Dict[str, Any]
    ) -> CreditProfile:
        """
        Update credit profile from Account Aggregator data
        
        Key signals:
        - Average monthly balance
        - Balance volatility
        - Salary credits (regularity)
        - Loan EMIs (existing obligations)
        - Overdraft usage
        """
        profile = self.get_or_create_profile(user_id)
        if not profile:
            raise ValueError(f"User {user_id} not found")
        
        # Extract signals
        profile.average_balance = account_data.get('average_balance', 0)
        
        # Calculate credit utilization
        credit_limit = account_data.get('credit_limit', 0)
        credit_used = account_data.get('credit_used', 0)
        if credit_limit > 0:
            utilization = credit_used / credit_limit
            profile.credit_utilization_score = self._score_from_utilization(utilization)
        
        # Existing obligations
        profile.existing_loan_count = account_data.get('loan_count', 0)
        profile.total_outstanding = account_data.get('total_outstanding', 0)
        
        # Debt to income
        monthly_income = account_data.get('monthly_income', 0)
        monthly_obligations = account_data.get('monthly_obligations', 0)
        if monthly_income > 0:
            profile.debt_to_income_ratio = monthly_obligations / monthly_income
        
        # Update composite
        profile.composite_score = self._calculate_composite_score(profile)
        
        # Update metadata
        if 'account_aggregator' not in profile.data_sources:
            profile.data_sources.append('account_aggregator')
        profile.confidence_level = min(0.95, profile.confidence_level + 0.3)
        profile.last_updated = datetime.now()
        
        db.update_credit_profile(profile)
        return profile
    
    def update_from_telecom(
        self, 
        user_id: str, 
        telecom_data: Dict[str, Any]
    ) -> CreditProfile:
        """
        Update from telecom recharge patterns
        
        Signals:
        - Recharge frequency and consistency
        - Plan type (prepaid vs postpaid)
        - Average recharge amount
        - Data usage patterns
        """
        profile = self.get_or_create_profile(user_id)
        if not profile:
            raise ValueError(f"User {user_id} not found")
        
        # Telecom contributes to stability score
        recharge_regularity = telecom_data.get('regularity_index', 0.5)
        plan_type = telecom_data.get('plan_type', 'prepaid')
        tenure_months = telecom_data.get('tenure_months', 0)
        
        # Postpaid indicates better creditworthiness
        telecom_score = 500
        if plan_type == 'postpaid':
            telecom_score += 100
        telecom_score += int(recharge_regularity * 100)
        telecom_score += min(100, tenure_months * 2)
        
        # Blend with existing score
        profile.income_stability_score = (
            profile.income_stability_score * 0.7 + 
            telecom_score * 0.3
        )
        
        # Update composite
        profile.composite_score = self._calculate_composite_score(profile)
        
        # Update metadata
        if 'telecom' not in profile.data_sources:
            profile.data_sources.append('telecom')
        profile.confidence_level = min(0.9, profile.confidence_level + 0.1)
        profile.last_updated = datetime.now()
        
        db.update_credit_profile(profile)
        return profile
    
    def get_credit_decision(
        self, 
        user_id: str, 
        product_type: str, 
        amount: float
    ) -> Dict[str, Any]:
        """
        Get credit decision for a specific product and amount
        
        Returns:
        - approved: bool
        - max_amount: float (if different from requested)
        - interest_rate: float (risk-based pricing)
        - reasons: List[str]
        - confidence: float
        """
        profile = self.get_or_create_profile(user_id)
        if not profile:
            return {
                'approved': False,
                'reasons': ['User not found'],
                'confidence': 0.0,
            }
        
        user = db.get_user(user_id)
        
        # Base decision on score
        min_score_required = self._get_min_score_for_product(product_type)
        
        result = {
            'approved': False,
            'requested_amount': amount,
            'max_amount': 0,
            'interest_rate': 0,
            'reasons': [],
            'confidence': profile.confidence_level,
            'credit_score': profile.composite_score,
        }
        
        # Check score
        if profile.composite_score < min_score_required:
            result['reasons'].append(
                f'Credit score {profile.composite_score} below minimum {min_score_required}'
            )
            return result
        
        # Check debt-to-income
        if profile.debt_to_income_ratio > 0.5:
            result['reasons'].append('Debt-to-income ratio too high')
            return result
        
        # Check recent defaults
        if profile.recent_defaults > 0:
            result['reasons'].append('Recent defaults on record')
            return result
        
        # Approved - calculate terms
        result['approved'] = True
        
        # Risk-based max amount
        score_factor = (profile.composite_score - self.min_score) / (self.max_score - self.min_score)
        max_amount = self._get_max_amount_for_product(product_type, user, profile)
        result['max_amount'] = min(amount, max_amount)
        
        # Risk-based pricing
        base_rate = self._get_base_rate_for_product(product_type)
        risk_premium = (1 - score_factor) * 0.12  # Up to 12% risk premium
        result['interest_rate'] = base_rate + risk_premium
        
        result['reasons'].append('Credit approved based on credit profile')
        
        return result
    
    # Private helper methods
    
    def _analyze_upi_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze UPI transactions for credit signals"""
        if not transactions:
            return {
                'count_30d': 0,
                'value_30d': 0,
                'regularity_index': 0,
                'merchant_diversity': 0,
                'incoming_ratio': 0.5,
            }
        
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        
        recent_txns = [
            t for t in transactions 
            if datetime.fromisoformat(t.get('timestamp', now.isoformat())) > thirty_days_ago
        ]
        
        count_30d = len(recent_txns)
        value_30d = sum(t.get('amount', 0) for t in recent_txns)
        
        # Regularity: how evenly distributed are transactions?
        if count_30d > 0:
            days_with_txn = len(set(
                datetime.fromisoformat(t.get('timestamp', now.isoformat())).date() 
                for t in recent_txns
            ))
            regularity_index = min(1.0, days_with_txn / 20)  # 20 days = perfect
        else:
            regularity_index = 0
        
        # Merchant diversity
        merchants = set(t.get('merchant', '') for t in recent_txns if t.get('merchant'))
        merchant_diversity = min(1.0, len(merchants) / 10)  # 10 unique = perfect
        
        # Incoming vs outgoing
        incoming = sum(t.get('amount', 0) for t in recent_txns if t.get('type') == 'credit')
        total = value_30d if value_30d > 0 else 1
        incoming_ratio = incoming / total
        
        return {
            'count_30d': count_30d,
            'value_30d': value_30d,
            'regularity_index': regularity_index,
            'merchant_diversity': merchant_diversity,
            'incoming_ratio': incoming_ratio,
        }
    
    def _calculate_payment_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate payment history score from transaction analysis"""
        base_score = 500
        
        # Transaction frequency boost
        count = analysis.get('count_30d', 0)
        base_score += min(150, count * 3)  # Up to 150 points
        
        # Regularity boost
        regularity = analysis.get('regularity_index', 0)
        base_score += int(regularity * 100)  # Up to 100 points
        
        # Merchant diversity boost
        diversity = analysis.get('merchant_diversity', 0)
        base_score += int(diversity * 50)  # Up to 50 points
        
        return min(self.max_score, max(self.min_score, base_score))
    
    def _calculate_stability_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate income stability score"""
        base_score = 500
        
        # Value-based boost
        value = analysis.get('value_30d', 0)
        if value > 50000:
            base_score += 100
        elif value > 20000:
            base_score += 50
        elif value > 5000:
            base_score += 25
        
        # Incoming ratio (more incoming = income, not just spending)
        incoming_ratio = analysis.get('incoming_ratio', 0.5)
        base_score += int(incoming_ratio * 100)
        
        # Regularity
        regularity = analysis.get('regularity_index', 0)
        base_score += int(regularity * 100)
        
        return min(self.max_score, max(self.min_score, base_score))
    
    def _calculate_composite_score(self, profile: CreditProfile) -> int:
        """Calculate weighted composite score"""
        weights = {
            'payment_history': 0.35,
            'credit_utilization': 0.30,
            'income_stability': 0.25,
            'debt_to_income': 0.10,
        }
        
        # Debt-to-income score (inverse - lower is better)
        dti_score = max(self.min_score, self.max_score - int(profile.debt_to_income_ratio * 600))
        
        composite = (
            profile.payment_history_score * weights['payment_history'] +
            profile.credit_utilization_score * weights['credit_utilization'] +
            profile.income_stability_score * weights['income_stability'] +
            dti_score * weights['debt_to_income']
        )
        
        return min(self.max_score, max(self.min_score, int(composite)))
    
    def _score_from_utilization(self, utilization: float) -> int:
        """Convert credit utilization to score component"""
        # Optimal utilization is 10-30%
        if utilization < 0.1:
            return 700  # Too low, not using credit
        elif utilization < 0.3:
            return 800  # Optimal
        elif utilization < 0.5:
            return 650
        elif utilization < 0.75:
            return 500
        else:
            return 400  # Over-utilized
    
    def _adjust_for_income(self, profile: CreditProfile, monthly_income: float) -> CreditProfile:
        """Adjust score based on income level"""
        income_boost = 0
        
        if monthly_income > 100000:  # > ₹1 LPM
            income_boost = 100
        elif monthly_income > 50000:
            income_boost = 75
        elif monthly_income > 25000:
            income_boost = 50
        elif monthly_income > 10000:
            income_boost = 25
        
        profile.income_stability_score += income_boost
        return profile
    
    def _get_min_score_for_product(self, product_type: str) -> int:
        """Minimum credit score required for each product type"""
        requirements = {
            'ewa': 400,  # Lower barrier for earned wage access
            'isa': 500,  # Medium for income share agreements
            'micro_investment': 350,  # Very low for investments
            'parametric_insurance': 300,  # No credit requirement
            'personal_loan': 650,  # Higher for traditional loans
            'credit_card': 700,  # Highest for credit cards
        }
        return requirements.get(product_type, 550)
    
    def _get_max_amount_for_product(
        self, 
        product_type: str, 
        user: User, 
        profile: CreditProfile
    ) -> float:
        """Calculate maximum amount based on product and risk"""
        # Base limits
        base_limits = {
            'ewa': min(25000, user.monthly_income * 0.5),  # 50% of monthly income
            'isa': 500000,  # ₹5L for education
            'micro_investment': 100000,  # ₹1L
            'parametric_insurance': 500000,  # ₹5L coverage
            'personal_loan': 300000,  # ₹3L
        }
        
        base = base_limits.get(product_type, 50000)
        
        # Adjust by score
        score_factor = (profile.composite_score - self.min_score) / (self.max_score - self.min_score)
        
        return base * (0.5 + 0.5 * score_factor)
    
    def _get_base_rate_for_product(self, product_type: str) -> float:
        """Base interest rate for each product"""
        rates = {
            'ewa': 0.01,  # 1% flat fee
            'isa': 0.15,  # 15% income share
            'personal_loan': 0.14,  # 14% APR base
            'credit_card': 0.36,  # 36% APR
        }
        return rates.get(product_type, 0.18)


# Global service instance
credit_identity_service = CreditIdentityService()
