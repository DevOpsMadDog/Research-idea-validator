# 🇮🇳 India FinTech Platform

## Missing Financial Products for 1.4 Billion Indians

This platform implements the key financial products identified as critically missing in India, based on the AI Agent Debate analysis.

---

## 🎯 The Problem

| Gap | India Reality | Developed Markets |
|-----|--------------|-------------------|
| Credit Access | 300M adults unbanked | 95%+ coverage |
| Retirement Savings | 93% without pensions | Mandatory coverage |
| Insurance | 600M underinsured | High penetration |
| Education Finance | 9.2% default rate | ISAs, IBR available |
| Gig Worker Benefits | Zero protection | Growing coverage |

---

## 💡 Products Built

### 1. 💰 Earned Wage Access (EWA)
Access wages you've already earned but haven't been paid yet.

**Key Features:**
- NOT a loan - your own money
- 1% flat fee (vs 400% APR from moneylenders)
- Instant UPI disbursement
- Auto-repayment on payday
- Builds credit history

**For:** Daily wage workers, gig workers, salaried employees

### 2. 📚 Income Share Agreements (ISA)
Pay for education as a percentage of future income.

**Key Features:**
- $0 upfront
- Pay 15% of income after getting a job
- Only pay if earning above ₹3 LPA
- Capped at 2x education cost
- Aligns school incentives with student success

**For:** Students wanting skill education, coding bootcamps

### 3. 🌾 Parametric Insurance
Automatic payouts based on weather/sensor data - no claims paperwork.

**Key Features:**
- Instant trigger (rainfall deficit, flood level, etc.)
- No claims process
- Payout via UPI in minutes
- Verifiable, transparent, trustworthy

**For:** Farmers, property owners, gig workers

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                    │
│   EWA  │  ISA  │  Parametric Insurance  │  Future...   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                       │
│  Credit Identity │ Income Verification │ Collection     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    CORE LAYER                           │
│         Models │ Database │ Configuration               │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
cd india_fintech_platform
pip install -r requirements.txt
```

### Run Demo

```bash
python demo/run_demo.py
```

This runs an interactive demo showcasing all three products.

### Run API Server

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API documentation: http://localhost:8000/docs

---

## 📡 API Endpoints

### Users
- `POST /users` - Create user
- `GET /users/{user_id}` - Get user details
- `POST /users/{user_id}/kyc` - Verify KYC

### Credit Identity
- `GET /credit/{user_id}` - Get credit profile
- `POST /credit/{user_id}/update-upi` - Update from UPI data
- `GET /credit/{user_id}/decision` - Get credit decision

### Earned Wage Access
- `GET /ewa/{user_id}/eligibility` - Check eligibility
- `POST /ewa/{user_id}/request` - Request advance
- `POST /ewa/{request_id}/disburse` - Disburse funds
- `GET /ewa/{user_id}/history` - View history

### Income Share Agreements
- `GET /isa/{user_id}/eligibility` - Check eligibility
- `POST /isa/{user_id}/apply` - Apply for ISA
- `POST /isa/{contract_id}/activate` - Activate contract
- `POST /isa/{contract_id}/income-event` - Process income
- `GET /isa/simulate` - Simulate repayment

### Parametric Insurance
- `GET /insurance/products` - List products
- `GET /insurance/quote` - Get quote
- `POST /insurance/{user_id}/purchase` - Purchase policy
- `POST /insurance/{policy_id}/activate` - Activate policy
- `POST /insurance/simulate-weather` - Simulate trigger

---

## 🧠 AI Agent Debate Summary

This platform was designed based on an intense debate between 6 AI agents:

| Agent | Perspective | Key Contribution |
|-------|-------------|------------------|
| DISRUPTOR | Fintech founder | Speed and ambition |
| BANKER | Traditional finance | Risk awareness |
| REGULATOR | Policy expert | Consumer protection |
| ECONOMIST | Macro view | Prioritization framework |
| CONSUMER | 800M underbanked | Dignity and accessibility |
| TECHNOLOGIST | Infrastructure | Platform thinking |

**Winner:** Agent CONSUMER - for keeping focus on human dignity.

**True Verdict:** The synthesis of all perspectives, held in productive tension.

---

## 📊 Impact Metrics (Target)

| Metric | Year 1 | Year 3 | Year 5 |
|--------|--------|--------|--------|
| EWA Users | 5M | 25M | 100M |
| ISA Students | 10K | 100K | 1M |
| Insurance Policies | 1M | 10M | 50M |
| Credit Profiles | 10M | 50M | 200M |

---

## 🔒 Regulatory Considerations

This is a prototype. Production deployment requires:

1. **EWA:** RBI guidelines compliance, lending license or partnership
2. **ISA:** Regulatory sandbox participation, legal structure clarity
3. **Insurance:** IRDAI approval, parametric product registration
4. **Credit:** Account Aggregator license, data privacy compliance

---

## 🤝 Contributing

See AI_AGENT_DEBATE_MISSING_FINANCIAL_PRODUCTS_INDIA.md for the full debate analysis.

---

## 📜 License

MIT License - Build for India, build for all.

---

*"Financial innovation is not about products. It is about POSSIBILITY."*
*— Judge SAGACITY*
