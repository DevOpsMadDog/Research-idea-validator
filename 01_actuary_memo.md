# ACTUARY / INSURANCE & REINSURANCE MEMO
**Role:** Insurance Actuary and Reinsurance Advisor  
**Date:** December 16, 2025

---

## 1. INSURABLE vs NON-INSURABLE CREATOR RISKS

### ❌ NON-INSURABLE (High Correlation / Moral Hazard / Unverifiable)

| Risk | Reason for Rejection |
|------|---------------------|
| General revenue volatility | Endogenous to creator behavior; no external peril |
| Algorithm changes (platform-wide) | 100% correlation across all creators; systemic |
| "Views down" or engagement drops | Caused by content quality (moral hazard); subjective |
| Loss of popularity / audience fatigue | Behavioral; creator-controlled |
| Competitive pressure | Market force, not insurable peril |
| Content strategy failure | Moral hazard + subjective |

### ✅ CONDITIONALLY INSURABLE (Narrow, Parametric, Externally Verifiable)

| Risk | Insurability Logic |
|------|-------------------|
| **Platform account suspension/termination** | Binary event; externally verifiable via API; creator has limited control IF they comply with ToS |
| **Major platform outage** | Objectively measurable (API status, news); low correlation with creator behavior |
| **Copyright strike (false/disputed)** | Verifiable via platform logs; can gate on creator compliance history |
| **Payment processing failure** | Platform-level issue; verifiable via public status pages |
| **Catastrophic equipment failure** | Physical peril (fire, theft); traditional insurance territory |

**Critical constraint:** Only risks that are:
1. Externally triggered (not creator-caused)
2. Objectively verifiable via third-party data
3. Low correlation with creator behavior
4. Capped in frequency and severity

---

## 2. PARAMETRIC COVERAGE TRIGGERS (Defensible & Verifiable)

### Coverage Option A: Platform Access Disruption
**Trigger:** Creator's verified channel becomes inaccessible for uploads/monetization for ≥7 consecutive days

**Verification:** YouTube API status checks + screenshot evidence + appeal documentation

**Payout:** Fixed daily benefit of ₹5,000/day (max 30 days = ₹150,000)

**Exclusions:**
- Strikes for actual ToS violations (verified by our pre-screening)
- Manual monetization disablement by creator
- Regional restrictions (not global suspension)
- Voluntary account changes/migrations

**Eligibility Gating:**
- ≥50K subscribers
- ≥12 months channel history
- Clean compliance record (our risk score ≥70/100)
- No strikes/warnings in past 90 days
- Must pass KYC + content audit

**Deductible:** First 7 days (waiting period)

**Premium:** ₹3,000–5,000/month (varies by risk tier)

---

### Coverage Option B: False Copyright Strike Protection
**Trigger:** YouTube copyright strike issued; creator files counter-claim; strike is retracted within 60 days

**Payout:** ₹25,000 flat (legal/dispute support)

**Exclusions:**
- Actual copyright infringement (verified by our content audit)
- Strikes not counter-claimed within 14 days
- Repeated strikes (>2 in 12 months)

**Eligibility:**
- Must provide proof of original content or licensing
- Pre-approval of high-risk content categories

**Premium:** ₹1,500/month

---

### Coverage Option C: Platform Payment Failure
**Trigger:** YouTube fails to transfer AdSense revenue for ≥30 days due to platform technical issues (not creator account issues)

**Verification:** Public YouTube/AdSense status page confirmation + support ticket trail

**Payout:** 50% of average monthly revenue (max ₹50,000)

**Exclusions:**
- Creator tax/payment info errors
- Account suspension for any reason
- Revenue below ₹10,000/month average

**Premium:** ₹2,000/month

---

### Coverage Option D: Major Equipment Loss
**Trigger:** Fire, theft, or accidental damage to declared equipment (camera, computer, studio gear) valued ≥₹100,000

**Verification:** Police report (theft) OR fire dept. report + purchase receipts

**Payout:** Replacement cost up to ₹300,000

**Traditional property insurance:** Partner with existing insurer; we distribute

**Premium:** ₹1,000–2,000/month

---

### Coverage Option E: Platform Outage Loss
**Trigger:** YouTube platform-wide outage ≥24 consecutive hours (verified by public status + news)

**Payout:** ₹10,000 flat (one-time per year)

**Exclusions:**
- Regional outages
- Creator-side connectivity issues

**Premium:** ₹500/month (optional add-on)

**Correlation Risk:** HIGH — only offer with strict annual aggregate cap

---

## 3. CRITICAL UNDERWRITING CONTROLS

### Eligibility Gating (Must Pass All)
- [ ] ≥50K subscribers OR ≥100K monthly views
- [ ] ≥12 months monetization history
- [ ] Clean ToS compliance record (verified via our audit)
- [ ] Risk score ≥65/100 (our proprietary model)
- [ ] No active strikes, warnings, or disputes
- [ ] Completed KYC (PAN, Aadhaar, bank verification)
- [ ] Content category approved (exclude high-risk: crypto scams, medical advice, adult-adjacent)

### Caps (Per Creator)
- Annual aggregate payout: ₹500,000 max
- Lifetime payout: ₹1,000,000 max
- Claim frequency: Max 2 claims/year

### Deductibles & Waiting Periods
- **Account suspension:** 7-day waiting period
- **Payment failure:** 30-day waiting period
- **Copyright strike:** No deductible (but must counter-claim)

### Exclusions (Hard)
- Creator-caused violations (ToS breach, fraud, harassment)
- Content that violates our acceptable use policy
- Strikes/suspensions during first 60 days of policy
- Mass platform policy changes (affects >10% of creators)
- War, terrorism, govt. shutdown of platforms

---

## 4. CORRELATION RISK MANAGEMENT

### Problem
Platform-wide events (algorithm change, mass strikes, AdSense glitch) trigger simultaneous claims → insolvency

### Controls

**1. Aggregate Annual Cap**
- Total payouts capped at ₹5 crore across all policies
- Individual event cap: ₹50 lakh (e.g., if YouTube goes down)

**2. Trigger Narrowing**
- Only cover "access loss" (can't upload/monetize)
- Exclude "revenue decrease" (too correlated)

**3. Excess-of-Loss Reinsurance**
- Retain first ₹25 lakh of annual losses
- Reinsurer covers ₹25L–₹2 crore layer
- Stop-loss at ₹2 crore (reject claims above)

**4. Geographic Diversification**
- Launch India-only initially (reduces global platform risk correlation)
- If expanding: stagger by region to avoid concentration

**5. Dynamic Underwriting**
- If YouTube changes policies → suspend new sales for 90 days
- Monitor platform health via API + news feeds
- Automatic suspension if >5% of portfolio files claims in 7 days

---

## 5. REINSURANCE & CAPITAL STRATEGY

### Capital Requirements (Year 1)
- Regulatory capital (India): ₹10 crore (if licensed insurer)
- Claims reserve: ₹2 crore
- Operating capital: ₹1 crore
- **Total:** ₹13 crore

**Problem:** No startup has ₹13 crore; reinsurers are skeptical of creator risk

### RECOMMENDED STRUCTURE (Reinsurance-Feasible)

**Option A: MGA (Managing General Agent) Model**
- Partner with licensed Indian insurer (e.g., Bajaj Allianz, ICICI Lombard)
- We design product, underwrite, distribute
- Insurer holds risk + regulatory license
- Reinsurer backstops insurer (traditional treaty)

**We provide:**
- Risk scoring tech (API integration)
- Underwriting criteria + data
- Claims verification automation

**Insurer provides:**
- License + capital + reinsurance relationships
- Balance sheet to hold risk

**Revenue split:** 30–40% commission on premiums

---

**Option B: Parametric "Service Agreement" (Not Insurance)**
- Do NOT call it insurance (regulatory arbitrage)
- Offer "Creator Protection Service" as paid membership
- Payout is "service credit" or "assistance grant" (not insurance claim)
- Fund via reserve pool (not insurance pool)

**Risk:** Regulatory gray zone; could be deemed insurance and shut down

**Safer:** Partner with licensed insurer from Day 1

---

### Reinsurer Appetite (Reality Check)

**Challenges:**
- New risk class (no actuarial tables)
- Platform dependency (single point of failure)
- Moral hazard concerns
- Small premium pool (niche market)

**What reinsurers WILL accept:**
- Equipment loss (traditional property)
- Cyber/tech E&O coverage (if we partner with cyber insurer)

**What reinsurers WON'T accept (yet):**
- Platform suspension risk (too new, too correlated)

**Path forward:**
- Start with traditional equipment coverage (reinsurable)
- Build 2–3 years of claims data on platform suspension
- Approach reinsurers with data + proven loss ratios

---

## 6. FRAUD VECTORS & CONTROLS

### Fraud Scenario 1: Fake Suspension
**Attack:** Creator temporarily disables monetization, claims "suspension"

**Control:**
- API verification (YouTube Studio API shows suspension reason)
- Screenshot + support ticket required
- Cross-check with YouTube support team (if partnership exists)
- Payout only after 7-day waiting period + appeals process

---

### Fraud Scenario 2: Intentional ToS Violation
**Attack:** Creator wants payout → uploads banned content → claims "wrongful suspension"

**Control:**
- Pre-screening: Audit content before policy issuance
- Behavior scoring: Detect anomalies (sudden content shift, risky uploads)
- Exclude suspensions within first 60 days of policy
- Review uploaded content during suspension period (if accessible)

---

### Fraud Scenario 3: Collusion (Mass Claim)
**Attack:** Group of creators coordinate false claims (e.g., fake copyright strikes)

**Control:**
- Network analysis: Detect clusters of simultaneous claims
- Require independent verification (not just creator screenshots)
- Aggregate cap triggers manual review if >3% of portfolio claims

---

### Fraud Scenario 4: Application Fraud
**Attack:** Fake subscriber count, edited screenshots, borrowed credentials

**Control:**
- API-only verification (no manual screenshots accepted)
- OAuth authentication (creator must authorize our app)
- Real-time data pulls (not self-reported)

---

## 7. UNDERWRITING CHECKLIST (Must-Have Controls)

- [ ] API-only verification (no self-reported data)
- [ ] OAuth-based authentication (creator grants read-only access)
- [ ] Pre-policy content audit (manual or AI-assisted)
- [ ] Risk score ≥65/100 (our proprietary model)
- [ ] 60-day waiting period for suspension coverage
- [ ] 7-day deductible on access loss
- [ ] Annual aggregate cap: ₹5 crore (across all policies)
- [ ] Individual annual cap: ₹5 lakh per creator
- [ ] Exclude mass events (>10% of creators affected)
- [ ] Partner with licensed insurer (MGA model)
- [ ] Reinsurance or stop-loss for catastrophic layer
- [ ] Monthly platform health monitoring (auto-suspend sales if risk spikes)
- [ ] Fraud detection: Network analysis + anomaly detection
- [ ] Geographic concentration limits (max 30% from single state)

---

## 8. LOSS RATIO ASSUMPTIONS (Conservative)

**Premium:** ₹3,000/month avg × 1,000 creators = ₹30 lakh/month = ₹3.6 crore/year

**Expected Claims (Year 1):**
- Suspension events: 2% of creators (20 × ₹50K avg payout) = ₹10 lakh
- Copyright strikes: 5% (50 × ₹25K) = ₹12.5 lakh
- Equipment loss: 1% (10 × ₹150K) = ₹15 lakh
- **Total claims:** ₹37.5 lakh

**Loss Ratio:** 37.5 / 360 = **10.4%** ← Extremely low (suspicious)

**Reality check:**
- Likely underestimating claims frequency
- Need 3–5 years of data to model accurately
- Should assume **30–50% loss ratio** for pricing safety

**Recommended premium adjustment:**
- Target 60% loss ratio (conservative)
- Premium should be ₹6,000–8,000/month for full coverage bundle

---

## 9. ACTUARIAL RECOMMENDATION

### ✅ Viable Path
1. Start as **SaaS risk scoring tool** (no insurance) → build data
2. Add **equipment insurance** via partner insurer (traditional, reinsurable)
3. After 12 months: Pilot **parametric platform suspension** (50 creators, waitlist)
4. Collect 24 months of claims data
5. Approach reinsurers with proven loss ratios
6. Scale if loss ratio <60%

### ❌ Do Not Launch
- General "revenue protection" (uninsurable)
- Algorithm change coverage (correlated)
- Standalone parametric product without insurer partnership (regulatory risk)

**Final verdict:** Insurable if scoped narrowly, gated heavily, and partnered with licensed insurer. NOT viable as standalone insurance company (capital + regulatory burden too high).
