"""
FastAPI Application - India FinTech Platform API

This API provides access to missing financial products for India:
- Earned Wage Access (EWA)
- Income Share Agreements (ISA)
- Parametric Insurance
- Credit Identity Service
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

import sys
sys.path.insert(0, '/workspace/india_fintech_platform')

from core.models import User, KYCStatus, EmploymentType
from core.database import db
from core.config import config
from services.credit_identity import credit_identity_service
from services.income_verification import income_verification_service
from services.collection import collection_service
from products.earned_wage_access import ewa_product
from products.income_share_agreement import isa_product
from products.parametric_insurance import parametric_insurance_product, InsuranceType


# FastAPI app
app = FastAPI(
    title="India FinTech Platform",
    description="Building missing financial products for 1.4 billion Indians",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=2)
    phone: str = Field(..., pattern=r'^\d{10}$')
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    state: Optional[str] = None
    employment_type: Optional[str] = "unemployed"
    monthly_income: Optional[float] = 0


class UpdateKYCRequest(BaseModel):
    aadhaar_last_4: str = Field(..., pattern=r'^\d{4}$')
    pan: Optional[str] = Field(None, pattern=r'^[A-Z]{5}\d{4}[A-Z]$')


class EWARequestModel(BaseModel):
    amount: float = Field(..., gt=0, le=25000)
    upi_vpa: Optional[str] = None
    express_disbursal: bool = False


class ISAApplicationRequest(BaseModel):
    education_provider_id: str
    education_provider_name: str
    program_name: str
    program_duration_months: int = Field(..., ge=1, le=48)
    education_cost: float = Field(..., gt=0, le=1000000)
    funded_amount: Optional[float] = None


class InsurancePolicyRequest(BaseModel):
    insurance_type: str
    coverage_amount: float = Field(..., gt=0, le=500000)
    coverage_location: str
    state: str
    duration_months: int = Field(12, ge=1, le=36)
    payout_upi: Optional[str] = None


class WeatherEventRequest(BaseModel):
    location: str
    parameter: str
    value: float


# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# User Management
@app.post("/users", tags=["Users"])
async def create_user(request: CreateUserRequest):
    """Create a new user account"""
    # Check if phone already exists
    existing = db.get_user_by_phone(request.phone)
    if existing:
        raise HTTPException(400, "Phone number already registered")
    
    user = User(
        name=request.name,
        phone=request.phone,
        email=request.email,
        date_of_birth=request.date_of_birth,
        state=request.state,
        employment_type=EmploymentType(request.employment_type) if request.employment_type else EmploymentType.UNEMPLOYED,
        monthly_income=request.monthly_income or 0,
    )
    
    db.create_user(user)
    
    # Create initial credit profile
    credit_identity_service.create_profile(user)
    
    return {"user_id": user.id, "message": "User created successfully"}


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: str):
    """Get user details"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user.to_dict()


@app.post("/users/{user_id}/kyc", tags=["Users"])
async def verify_kyc(user_id: str, request: UpdateKYCRequest):
    """Verify user KYC (simplified for demo)"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    # In production: verify with UIDAI, DigiLocker
    user.aadhaar_hash = f"xxxx-xxxx-{request.aadhaar_last_4}"
    user.pan = request.pan
    user.kyc_status = KYCStatus.VERIFIED
    user.kyc_verified_at = datetime.now()
    
    db.update_user(user)
    
    return {"message": "KYC verified", "status": user.kyc_status.value}


# Credit Identity
@app.get("/credit/{user_id}", tags=["Credit Identity"])
async def get_credit_profile(user_id: str):
    """Get user's credit profile"""
    profile = credit_identity_service.get_or_create_profile(user_id)
    if not profile:
        raise HTTPException(404, "User not found")
    return profile.to_dict()


@app.post("/credit/{user_id}/update-upi", tags=["Credit Identity"])
async def update_credit_from_upi(user_id: str, transactions: List[Dict[str, Any]]):
    """Update credit score from UPI transaction history"""
    try:
        profile = credit_identity_service.update_from_upi_data(user_id, transactions)
        return profile.to_dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/credit/{user_id}/decision", tags=["Credit Identity"])
async def get_credit_decision(user_id: str, product_type: str, amount: float):
    """Get credit decision for a product application"""
    decision = credit_identity_service.get_credit_decision(user_id, product_type, amount)
    return decision


# Earned Wage Access
@app.get("/ewa/{user_id}/eligibility", tags=["Earned Wage Access"])
async def check_ewa_eligibility(user_id: str):
    """Check if user is eligible for earned wage access"""
    return ewa_product.check_eligibility(user_id)


@app.post("/ewa/{user_id}/request", tags=["Earned Wage Access"])
async def request_ewa(user_id: str, request: EWARequestModel):
    """Request an earned wage advance"""
    ewa_request = ewa_product.request_advance(
        user_id=user_id,
        amount=request.amount,
        upi_vpa=request.upi_vpa,
        express_disbursal=request.express_disbursal,
    )
    return ewa_request.to_dict()


@app.post("/ewa/{request_id}/disburse", tags=["Earned Wage Access"])
async def disburse_ewa(request_id: str):
    """Disburse approved EWA to user"""
    result = ewa_product.disburse_advance(request_id)
    if not result.get('success'):
        raise HTTPException(400, result.get('error'))
    return result


@app.get("/ewa/{user_id}/history", tags=["Earned Wage Access"])
async def get_ewa_history(user_id: str):
    """Get user's EWA history"""
    return {
        'history': ewa_product.get_user_ewa_history(user_id),
        'stats': ewa_product.get_ewa_stats(user_id),
    }


# Income Share Agreements
@app.get("/isa/{user_id}/eligibility", tags=["Income Share Agreement"])
async def check_isa_eligibility(user_id: str, program_cost: float):
    """Check if user is eligible for ISA"""
    return isa_product.check_eligibility(user_id, program_cost)


@app.post("/isa/{user_id}/apply", tags=["Income Share Agreement"])
async def create_isa(user_id: str, request: ISAApplicationRequest):
    """Apply for an Income Share Agreement"""
    try:
        contract = isa_product.create_contract(
            user_id=user_id,
            education_provider_id=request.education_provider_id,
            education_provider_name=request.education_provider_name,
            program_name=request.program_name,
            program_duration_months=request.program_duration_months,
            education_cost=request.education_cost,
            funded_amount=request.funded_amount,
        )
        return contract.to_dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/isa/{contract_id}/activate", tags=["Income Share Agreement"])
async def activate_isa(contract_id: str, program_start_date: str):
    """Activate ISA when student enrolls"""
    start_date = datetime.fromisoformat(program_start_date)
    result = isa_product.activate_contract(contract_id, start_date)
    if not result.get('success'):
        raise HTTPException(400, result.get('error'))
    return result


@app.post("/isa/{contract_id}/income-event", tags=["Income Share Agreement"])
async def process_isa_income(contract_id: str, income_month: str, gross_income: float):
    """Process income event for ISA payment calculation"""
    try:
        payment = isa_product.process_income_event(contract_id, income_month, gross_income)
        return payment.to_dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/isa/{contract_id}/summary", tags=["Income Share Agreement"])
async def get_isa_summary(contract_id: str):
    """Get ISA contract summary"""
    return isa_product.get_contract_summary(contract_id)


@app.get("/isa/{user_id}/contracts", tags=["Income Share Agreement"])
async def get_user_isas(user_id: str):
    """Get all ISA contracts for a user"""
    return isa_product.get_user_contracts(user_id)


@app.get("/isa/simulate", tags=["Income Share Agreement"])
async def simulate_isa_repayment(
    funded_amount: float, 
    expected_annual_income: float,
    income_share: float = 0.15
):
    """Simulate ISA repayment schedule"""
    return isa_product.simulate_repayment_schedule(
        funded_amount, expected_annual_income, income_share
    )


# Parametric Insurance
@app.get("/insurance/products", tags=["Parametric Insurance"])
async def get_insurance_products(state: str):
    """Get available insurance products for a state"""
    return parametric_insurance_product.get_available_products(state)


@app.get("/insurance/quote", tags=["Parametric Insurance"])
async def get_insurance_quote(
    insurance_type: str,
    coverage_amount: float,
    duration_months: int = 12
):
    """Get insurance premium quote"""
    try:
        ins_type = InsuranceType(insurance_type)
        return parametric_insurance_product.calculate_premium(
            ins_type, coverage_amount, duration_months
        )
    except ValueError:
        raise HTTPException(400, f"Invalid insurance type: {insurance_type}")


@app.post("/insurance/{user_id}/purchase", tags=["Parametric Insurance"])
async def purchase_insurance(user_id: str, request: InsurancePolicyRequest):
    """Purchase insurance policy"""
    try:
        ins_type = InsuranceType(request.insurance_type)
        policy = parametric_insurance_product.create_policy(
            user_id=user_id,
            insurance_type=ins_type,
            coverage_amount=request.coverage_amount,
            coverage_location=request.coverage_location,
            state=request.state,
            duration_months=request.duration_months,
            payout_upi=request.payout_upi,
        )
        return policy.to_dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/insurance/{policy_id}/activate", tags=["Parametric Insurance"])
async def activate_insurance(policy_id: str):
    """Activate insurance after premium payment"""
    result = parametric_insurance_product.activate_policy(policy_id)
    if not result.get('success'):
        raise HTTPException(400, result.get('error'))
    return result


@app.get("/insurance/{policy_id}/status", tags=["Parametric Insurance"])
async def get_insurance_status(policy_id: str):
    """Get insurance policy status"""
    status = parametric_insurance_product.get_policy_status(policy_id)
    if 'error' in status:
        raise HTTPException(404, status['error'])
    return status


@app.get("/insurance/{user_id}/policies", tags=["Parametric Insurance"])
async def get_user_policies(user_id: str):
    """Get all insurance policies for a user"""
    return parametric_insurance_product.get_user_policies(user_id)


@app.post("/insurance/simulate-weather", tags=["Parametric Insurance"])
async def simulate_weather(request: WeatherEventRequest):
    """Simulate weather event to trigger policies (demo only)"""
    results = parametric_insurance_product.simulate_weather_event(
        request.location, request.parameter, request.value
    )
    return {
        'event': {
            'location': request.location,
            'parameter': request.parameter,
            'value': request.value,
        },
        'triggered_policies': len(results),
        'payouts': results,
    }


# Platform Stats
@app.get("/stats", tags=["Platform"])
async def get_platform_stats():
    """Get platform statistics"""
    return db.get_stats()


# Run with: uvicorn api.main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
