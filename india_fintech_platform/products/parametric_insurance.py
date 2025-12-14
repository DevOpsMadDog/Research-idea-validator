"""
Parametric Insurance Product
Automatic payouts based on measurable triggers (weather, satellite, etc.)

This addresses the critical gap for 600 million rural Indians:
- No claims paperwork
- Instant payouts when trigger event occurs
- Eliminates fraud AND bureaucracy
- Works for crop, health, property insurance
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
import random

from core.models import User, Transaction, TransactionStatus
from core.database import db
from core.config import config


class InsuranceType(Enum):
    CROP_RAINFALL = "crop_rainfall"
    CROP_TEMPERATURE = "crop_temperature"
    FLOOD = "flood"
    DROUGHT = "drought"
    HEALTH_HOSPITALIZATION = "health_hospitalization"
    GIG_ACCIDENT = "gig_accident"


class PolicyStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    TRIGGERED = "triggered"
    PAYOUT_PROCESSING = "payout_processing"
    PAYOUT_COMPLETED = "payout_completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class TriggerCondition:
    """Defines when insurance pays out"""
    parameter: str  # rainfall_mm, temperature_c, hospital_days, etc.
    operator: str  # less_than, greater_than, equals
    threshold: float
    measurement_source: str  # imd (India Meteorological), satellite, hospital_api
    measurement_location: Optional[str] = None  # district, pincode, coordinates


@dataclass
class InsurancePolicy:
    """Parametric insurance policy"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    
    # Policy type
    insurance_type: InsuranceType = InsuranceType.CROP_RAINFALL
    
    # Coverage details
    coverage_amount: float = 0.0
    premium: float = 0.0
    premium_paid: bool = False
    
    # Trigger conditions
    trigger_conditions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Location (for weather-based)
    coverage_location: str = ""  # District/pincode
    state: str = ""
    coordinates: Optional[str] = None  # lat,lng
    
    # Policy period
    start_date: datetime = field(default_factory=datetime.now)
    end_date: datetime = field(default_factory=datetime.now)
    
    # Status
    status: PolicyStatus = PolicyStatus.PENDING
    
    # Trigger/payout tracking
    triggered_at: Optional[datetime] = None
    trigger_data: Optional[Dict[str, Any]] = None
    payout_amount: float = 0.0
    payout_date: Optional[datetime] = None
    payout_upi: Optional[str] = None
    payout_bank: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'insurance_type': self.insurance_type.value,
            'coverage_amount': self.coverage_amount,
            'premium': self.premium,
            'premium_paid': self.premium_paid,
            'trigger_conditions': self.trigger_conditions,
            'coverage_location': self.coverage_location,
            'state': self.state,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status.value,
            'payout_amount': self.payout_amount,
            'created_at': self.created_at.isoformat(),
        }


@dataclass
class WeatherData:
    """Weather/environmental data for trigger evaluation"""
    date: datetime
    location: str
    parameter: str
    value: float
    source: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date.isoformat(),
            'location': self.location,
            'parameter': self.parameter,
            'value': self.value,
            'source': self.source,
        }


class ParametricInsuranceProduct:
    """
    Parametric Insurance Product
    
    Revolutionary insurance that:
    1. Pays out automatically based on measurable triggers
    2. No claims process - data triggers payment
    3. Uses satellite, weather, IoT data
    4. Instant payment via UPI when triggered
    5. Transparent, verifiable, trustworthy
    
    Use cases:
    - Crop insurance (rainfall deficit/excess)
    - Flood insurance (water level triggers)
    - Health insurance (hospitalization days)
    - Gig worker accident (verified via platform)
    """
    
    def __init__(self):
        self.min_premium = config.parametric_min_premium
        self.max_coverage = config.parametric_max_coverage
        self.product_type = "parametric_insurance"
        
        # Premium rates by type (percentage of coverage)
        self.premium_rates = {
            InsuranceType.CROP_RAINFALL: 0.05,  # 5%
            InsuranceType.CROP_TEMPERATURE: 0.04,
            InsuranceType.FLOOD: 0.08,
            InsuranceType.DROUGHT: 0.06,
            InsuranceType.HEALTH_HOSPITALIZATION: 0.03,
            InsuranceType.GIG_ACCIDENT: 0.02,
        }
    
    def get_available_products(self, state: str) -> List[Dict[str, Any]]:
        """Get available insurance products for a state"""
        # Different products available in different states
        products = [
            {
                'type': InsuranceType.CROP_RAINFALL.value,
                'name': 'Crop Rainfall Protection',
                'description': 'Automatic payout if rainfall is 20% below normal',
                'premium_rate': self.premium_rates[InsuranceType.CROP_RAINFALL],
                'min_coverage': 10000,
                'max_coverage': 200000,
                'trigger': 'Rainfall deficit > 20% from IMD normal',
                'seasons': ['kharif', 'rabi'],
            },
            {
                'type': InsuranceType.DROUGHT.value,
                'name': 'Drought Protection',
                'description': 'Payout when drought is declared in your district',
                'premium_rate': self.premium_rates[InsuranceType.DROUGHT],
                'min_coverage': 20000,
                'max_coverage': 300000,
                'trigger': 'Official drought declaration by state government',
                'seasons': ['kharif'],
            },
            {
                'type': InsuranceType.FLOOD.value,
                'name': 'Flood Protection',
                'description': 'Automatic payout when river level exceeds danger mark',
                'premium_rate': self.premium_rates[InsuranceType.FLOOD],
                'min_coverage': 25000,
                'max_coverage': 500000,
                'trigger': 'River water level > danger mark (CWC data)',
                'seasons': ['monsoon'],
            },
            {
                'type': InsuranceType.GIG_ACCIDENT.value,
                'name': 'Gig Worker Accident Cover',
                'description': 'Instant payout for accidents during gig work',
                'premium_rate': self.premium_rates[InsuranceType.GIG_ACCIDENT],
                'min_coverage': 50000,
                'max_coverage': 500000,
                'trigger': 'Verified accident during active delivery/ride',
                'availability': 'All cities',
            },
        ]
        
        return products
    
    def calculate_premium(
        self,
        insurance_type: InsuranceType,
        coverage_amount: float,
        duration_months: int = 12,
        location_risk_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate premium for given coverage
        """
        base_rate = self.premium_rates.get(insurance_type, 0.05)
        
        # Adjust for duration
        if duration_months < 12:
            duration_factor = duration_months / 12 * 1.2  # Slight penalty for short term
        else:
            duration_factor = duration_months / 12 * 0.95  # Discount for longer term
        
        # Calculate premium
        premium = coverage_amount * base_rate * duration_factor * location_risk_factor
        
        # Apply minimum
        premium = max(premium, self.min_premium)
        
        # Calculate payout scenarios
        scenarios = self._calculate_payout_scenarios(insurance_type, coverage_amount)
        
        return {
            'coverage_amount': coverage_amount,
            'premium': round(premium, 2),
            'premium_per_month': round(premium / duration_months, 2),
            'duration_months': duration_months,
            'base_rate': base_rate * 100,
            'location_risk_factor': location_risk_factor,
            'payout_scenarios': scenarios,
        }
    
    def create_policy(
        self,
        user_id: str,
        insurance_type: InsuranceType,
        coverage_amount: float,
        coverage_location: str,
        state: str,
        duration_months: int = 12,
        payout_upi: Optional[str] = None,
    ) -> InsurancePolicy:
        """
        Create a new insurance policy
        """
        user = db.get_user(user_id)
        if not user:
            raise ValueError('User not found')
        
        # Validate coverage
        if coverage_amount > self.max_coverage:
            raise ValueError(f'Coverage exceeds maximum of ₹{self.max_coverage}')
        
        # Calculate premium
        pricing = self.calculate_premium(insurance_type, coverage_amount, duration_months)
        
        # Create trigger conditions based on type
        trigger_conditions = self._create_trigger_conditions(insurance_type, coverage_location)
        
        # Create policy
        end_date = datetime.now() + timedelta(days=duration_months * 30)
        
        policy = InsurancePolicy(
            user_id=user_id,
            insurance_type=insurance_type,
            coverage_amount=coverage_amount,
            premium=pricing['premium'],
            trigger_conditions=trigger_conditions,
            coverage_location=coverage_location,
            state=state,
            end_date=end_date,
            payout_upi=payout_upi,
            status=PolicyStatus.PENDING,
        )
        
        db.store_product(self.product_type, policy.id, policy.to_dict())
        
        return policy
    
    def activate_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Activate policy after premium payment
        """
        policy_data = db.get_product(self.product_type, policy_id)
        if not policy_data:
            return {'success': False, 'error': 'Policy not found'}
        
        if policy_data['status'] != PolicyStatus.PENDING.value:
            return {'success': False, 'error': f"Invalid status: {policy_data['status']}"}
        
        # Mark as active
        policy_data['status'] = PolicyStatus.ACTIVE.value
        policy_data['premium_paid'] = True
        policy_data['start_date'] = datetime.now().isoformat()
        
        db.update_product(self.product_type, policy_id, policy_data)
        
        # Record premium transaction
        transaction = Transaction(
            user_id=policy_data['user_id'],
            type='debit',
            amount=policy_data['premium'],
            description=f"Insurance Premium - {policy_data['insurance_type']}",
            status=TransactionStatus.COMPLETED,
        )
        db.create_transaction(transaction)
        
        return {
            'success': True,
            'policy_id': policy_id,
            'coverage': policy_data['coverage_amount'],
            'valid_until': policy_data['end_date'],
            'trigger_conditions': policy_data['trigger_conditions'],
        }
    
    def check_trigger(
        self, 
        policy_id: str, 
        weather_data: WeatherData
    ) -> Dict[str, Any]:
        """
        Check if policy trigger conditions are met
        In production, this would be called by automated data feeds
        """
        policy_data = db.get_product(self.product_type, policy_id)
        if not policy_data:
            return {'triggered': False, 'error': 'Policy not found'}
        
        if policy_data['status'] != PolicyStatus.ACTIVE.value:
            return {'triggered': False, 'error': f"Policy not active: {policy_data['status']}"}
        
        # Check if location matches
        if weather_data.location != policy_data['coverage_location']:
            return {'triggered': False, 'reason': 'Location mismatch'}
        
        # Evaluate trigger conditions
        for condition in policy_data['trigger_conditions']:
            if weather_data.parameter == condition['parameter']:
                is_triggered = self._evaluate_condition(
                    weather_data.value,
                    condition['operator'],
                    condition['threshold']
                )
                
                if is_triggered:
                    return {
                        'triggered': True,
                        'condition': condition,
                        'measured_value': weather_data.value,
                        'threshold': condition['threshold'],
                        'payout_amount': policy_data['coverage_amount'],
                    }
        
        return {'triggered': False, 'reason': 'Conditions not met'}
    
    def process_trigger_event(
        self, 
        policy_id: str,
        trigger_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a verified trigger event and initiate payout
        """
        policy_data = db.get_product(self.product_type, policy_id)
        if not policy_data:
            return {'success': False, 'error': 'Policy not found'}
        
        if policy_data['status'] != PolicyStatus.ACTIVE.value:
            return {'success': False, 'error': f"Policy not active"}
        
        # Update policy status
        policy_data['status'] = PolicyStatus.TRIGGERED.value
        policy_data['triggered_at'] = datetime.now().isoformat()
        policy_data['trigger_data'] = trigger_data
        policy_data['payout_amount'] = policy_data['coverage_amount']
        
        db.update_product(self.product_type, policy_id, policy_data)
        
        # Initiate payout
        return self.process_payout(policy_id)
    
    def process_payout(self, policy_id: str) -> Dict[str, Any]:
        """
        Process payout for triggered policy
        """
        policy_data = db.get_product(self.product_type, policy_id)
        if not policy_data:
            return {'success': False, 'error': 'Policy not found'}
        
        if policy_data['status'] not in [
            PolicyStatus.TRIGGERED.value,
            PolicyStatus.PAYOUT_PROCESSING.value
        ]:
            return {'success': False, 'error': 'Policy not triggered'}
        
        payout_amount = policy_data['payout_amount']
        
        # Simulate instant UPI payout
        policy_data['status'] = PolicyStatus.PAYOUT_PROCESSING.value
        db.update_product(self.product_type, policy_id, policy_data)
        
        # Create payout transaction
        transaction = Transaction(
            user_id=policy_data['user_id'],
            type='credit',
            amount=payout_amount,
            description=f"Insurance Payout - {policy_data['insurance_type']}",
            status=TransactionStatus.COMPLETED,
        )
        db.create_transaction(transaction)
        
        # Update policy as completed
        policy_data['status'] = PolicyStatus.PAYOUT_COMPLETED.value
        policy_data['payout_date'] = datetime.now().isoformat()
        
        db.update_product(self.product_type, policy_id, policy_data)
        
        return {
            'success': True,
            'policy_id': policy_id,
            'payout_amount': payout_amount,
            'payout_date': policy_data['payout_date'],
            'transaction_id': transaction.id,
            'message': f'₹{payout_amount} credited to your account',
        }
    
    def get_user_policies(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all policies for a user"""
        return db.get_user_products(self.product_type, user_id)
    
    def get_policy_status(self, policy_id: str) -> Dict[str, Any]:
        """Get detailed policy status"""
        policy_data = db.get_product(self.product_type, policy_id)
        if not policy_data:
            return {'error': 'Policy not found'}
        
        return {
            'policy_id': policy_id,
            'type': policy_data['insurance_type'],
            'status': policy_data['status'],
            'coverage': policy_data['coverage_amount'],
            'premium_paid': policy_data['premium_paid'],
            'location': policy_data['coverage_location'],
            'valid_from': policy_data.get('start_date'),
            'valid_until': policy_data['end_date'],
            'trigger_conditions': policy_data['trigger_conditions'],
            'payout_amount': policy_data.get('payout_amount', 0),
            'payout_date': policy_data.get('payout_date'),
        }
    
    def simulate_weather_event(
        self, 
        location: str, 
        parameter: str, 
        value: float
    ) -> List[Dict[str, Any]]:
        """
        Simulate a weather event to trigger policies (for demo)
        In production: receives data from IMD, satellites, etc.
        """
        weather_data = WeatherData(
            date=datetime.now(),
            location=location,
            parameter=parameter,
            value=value,
            source='simulation',
        )
        
        # Find all active policies for this location
        all_policies = [
            p for p in db._products.get(self.product_type, {}).values()
            if p.get('coverage_location') == location 
            and p.get('status') == PolicyStatus.ACTIVE.value
        ]
        
        results = []
        for policy in all_policies:
            check = self.check_trigger(policy['id'], weather_data)
            if check.get('triggered'):
                payout = self.process_trigger_event(policy['id'], weather_data.to_dict())
                results.append({
                    'policy_id': policy['id'],
                    'user_id': policy['user_id'],
                    **payout
                })
        
        return results
    
    # Private methods
    
    def _create_trigger_conditions(
        self, 
        insurance_type: InsuranceType, 
        location: str
    ) -> List[Dict[str, Any]]:
        """Create appropriate trigger conditions for insurance type"""
        
        if insurance_type == InsuranceType.CROP_RAINFALL:
            return [{
                'parameter': 'rainfall_deficit_percentage',
                'operator': 'greater_than',
                'threshold': 20,  # 20% deficit triggers payout
                'measurement_source': 'imd',
                'measurement_location': location,
            }]
        
        elif insurance_type == InsuranceType.DROUGHT:
            return [{
                'parameter': 'drought_declaration',
                'operator': 'equals',
                'threshold': 1,  # Binary - declared or not
                'measurement_source': 'state_government',
                'measurement_location': location,
            }]
        
        elif insurance_type == InsuranceType.FLOOD:
            return [{
                'parameter': 'water_level_above_danger',
                'operator': 'greater_than',
                'threshold': 0,  # Any amount above danger mark
                'measurement_source': 'cwc',
                'measurement_location': location,
            }]
        
        elif insurance_type == InsuranceType.GIG_ACCIDENT:
            return [{
                'parameter': 'verified_accident',
                'operator': 'equals',
                'threshold': 1,
                'measurement_source': 'platform_api',
                'measurement_location': location,
            }]
        
        else:
            return []
    
    def _evaluate_condition(
        self, 
        value: float, 
        operator: str, 
        threshold: float
    ) -> bool:
        """Evaluate if trigger condition is met"""
        if operator == 'greater_than':
            return value > threshold
        elif operator == 'less_than':
            return value < threshold
        elif operator == 'equals':
            return value == threshold
        elif operator == 'greater_than_equal':
            return value >= threshold
        elif operator == 'less_than_equal':
            return value <= threshold
        return False
    
    def _calculate_payout_scenarios(
        self, 
        insurance_type: InsuranceType, 
        coverage: float
    ) -> List[Dict[str, Any]]:
        """Calculate example payout scenarios"""
        
        if insurance_type == InsuranceType.CROP_RAINFALL:
            return [
                {'scenario': 'No rainfall deficit', 'payout': 0},
                {'scenario': 'Deficit > 20%', 'payout': coverage},
            ]
        
        elif insurance_type == InsuranceType.FLOOD:
            return [
                {'scenario': 'Water level normal', 'payout': 0},
                {'scenario': 'Water level above danger mark', 'payout': coverage},
            ]
        
        elif insurance_type == InsuranceType.GIG_ACCIDENT:
            return [
                {'scenario': 'No accident', 'payout': 0},
                {'scenario': 'Verified accident during work', 'payout': coverage},
            ]
        
        return [{'scenario': 'Trigger met', 'payout': coverage}]


# Global product instance
parametric_insurance_product = ParametricInsuranceProduct()
