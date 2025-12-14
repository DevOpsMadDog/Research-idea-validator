"""
Configuration for India FinTech Platform
"""

from dataclasses import dataclass, field
from typing import Optional
import os


@dataclass
class Config:
    """Platform configuration"""
    
    # Database
    database_url: str = "sqlite:///india_fintech.db"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True
    
    # Credit Scoring
    min_credit_score: int = 300
    max_credit_score: int = 900
    default_credit_score: int = 550
    
    # Earned Wage Access (EWA)
    ewa_max_advance_percentage: float = 0.50  # 50% of earned wages
    ewa_processing_fee_percentage: float = 0.01  # 1% fee
    ewa_max_amount: float = 25000.0  # ₹25,000 max
    
    # Income Share Agreement (ISA)
    isa_income_share_percentage: float = 0.15  # 15% of income
    isa_payment_duration_months: int = 48  # 4 years
    isa_minimum_income_threshold: float = 300000.0  # ₹3 LPA minimum
    isa_cap_multiplier: float = 2.0  # Max 2x education cost
    
    # Parametric Insurance
    parametric_min_premium: float = 100.0  # ₹100 minimum
    parametric_max_coverage: float = 500000.0  # ₹5 lakh max
    
    # Regulatory
    kyc_verification_required: bool = True
    aadhaar_verification_enabled: bool = True
    pan_verification_enabled: bool = True
    
    # Risk Management
    max_exposure_per_user: float = 500000.0  # ₹5 lakh
    default_risk_buffer: float = 0.20  # 20% buffer
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        return cls(
            database_url=os.getenv('DATABASE_URL', cls.database_url),
            api_host=os.getenv('API_HOST', cls.api_host),
            api_port=int(os.getenv('API_PORT', cls.api_port)),
            api_debug=os.getenv('API_DEBUG', 'true').lower() == 'true',
        )


# Global config instance
config = Config()
