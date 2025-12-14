# Multi-Agent Debate System

## Overview
An intense AI agent debate system that analyzes missing financial products in India through multi-perspective discussions.

## System Components

### 1. Debate Engine (`debate_engine.py`)
- Manages debate rounds, scoring, and argument tracking
- Supports multiple debate phases: Opening, Rebuttal, Cross-Examination, Closing
- Tracks agent performance and generates leaderboards
- Exports comprehensive debate transcripts

### 2. Specialized Agents (`agents.py`)
- **Product Visionary**: Innovation-focused, user-centric perspective
- **Market Analyst**: Data-driven market analysis and business viability
- **Risk Manager**: Compliance, risk mitigation, and regulatory concerns
- **Tech Architect**: Technical feasibility and implementation details
- **Judge Agent**: Holistic evaluation and final verdict

### 3. Debate Orchestrator (`orchestrator.py`)
- Coordinates multi-round debates between agents
- Manages debate flow through 5 phases
- Implements automated scoring system
- Generates comprehensive results and recommendations

## Key Features

- **Multi-Phase Debate Structure**:
  - Phase 1: Opening Arguments (agents present initial positions)
  - Phase 2: Rebuttals Round 1 (address opponent arguments)
  - Phase 3: Cross-Examination (direct questioning)
  - Phase 4: Rebuttals Round 2 (intense counter-arguments)
  - Phase 5: Closing Arguments (final positions)

- **Automated Scoring**:
  - Argument Strength (0-10)
  - Evidence Quality (0-10)
  - Logical Coherence (0-10)
  - Real-time leaderboards

- **Comprehensive Output**:
  - Full debate transcripts
  - Judge's detailed evaluation
  - Final product recommendation
  - Implementation roadmap

## Running the Debate

```bash
python orchestrator.py
```

## Output Files

- `debate_results.json`: Summary of results and final recommendation
- `debate_full_transcript.json`: Complete debate transcript with all arguments

## Final Recommendation

After intense debate, the system recommends:

**Product: SAMPOORNA (Federated Financial Dashboard)**

- **Core Value**: Unified financial life management
- **Technology**: Account Aggregator framework
- **Target**: 550M Indians with multiple financial accounts
- **Timeline**: 6-month MVP, 12-month full launch
- **Investment**: ₹10 crore
- **Revenue Potential**: ₹500+ crore by Year 2

## Key Insights from Debate

1. India has 800M underserved citizens in financial services
2. Account Aggregator framework enables low-risk innovation
3. Regulatory compliance is critical for survival
4. Technical feasibility must drive product decisions
5. Unit economics matter more than vision in current market

## Why SAMPOORNA Wins

- ✅ Technically feasible (6-month build time)
- ✅ Regulatory compliant (no license required)
- ✅ Market validated (proven user need)
- ✅ Economically viable (positive unit economics)
- ✅ Scalable (leverage existing infrastructure)

## Architecture

```
Frontend: Flutter (iOS/Android/Web)
Backend: Python FastAPI
Database: PostgreSQL + Redis
Integrations: Account Aggregator API, UPI, CIBIL
Security: AES-256, tokenization, OAuth 2.0
Infrastructure: AWS EKS (Kubernetes)
```

## Business Model

1. **Subscription**: ₹99/month or ₹999/year
2. **Transaction Fees**: 0.3-0.5% on investments
3. **Partner Commissions**: Insurance, loans, tax filing

## Next Steps

See `PROTOTYPE.md` for detailed product specifications and implementation plan.
