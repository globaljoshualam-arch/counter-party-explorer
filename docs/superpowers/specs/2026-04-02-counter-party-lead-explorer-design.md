# Counter-Party Lead Explorer — Design Spec

## Overview

A Streamlit web app that helps Airwallex sales reps identify high-potential prospects from transaction data. The tool surfaces counterparties (suppliers and buyers) who transact with existing Airwallex clients, scores them by potential, and provides pitch context for outreach.

## Problem

Sales reps lack visibility into who their clients' counterparties are. These counterparties are warm leads — they already transact with Airwallex clients and could benefit from Airwallex Pay (faster settlement, lower fees, no manual bank details).

## Data Sources

Two CSV datasets, uploaded monthly:

| Dataset | Description | Key Fields |
|---------|-------------|------------|
| **Trade_Lead_Gen_from_Payment** | Money leaving clients (payments to suppliers) | payer_account_id, receiver_name, receiver_customer_status, receiver_country, payment_ccy, monthly_payment_amount |
| **Trade_Lead_Gen_from_Remitter** | Money entering clients (deposits from buyers) | awx_id, remitter_account_name, customer_status, ccy, monthly_deposit_usd |

**Scale:**
- ~104 unique payer clients
- ~11,800 unique counterparties (after filtering out existing Airwallex clients)
- ~31 BD managers
- ~64k rows combined (pre-filter)

## Core Features

### 1. Top Leads View (Default)

Ranked list of counterparties sorted by composite score.

**Columns:**
- Score (0–100)
- Company name
- Region (with flag, filterable)
- Type (Receives / Pays / Both)
- Monthly volume
- Client count (network density)
- Currencies
- Trend (% change)

**Filters:**
- Region (dropdown with multi-select)
- Type (All / Receives / Pays / Both)
- Currency
- Score range

**Sorting:** Score (default), Volume, Client count, Trend

### 2. Search

Full-text search on company name. Returns matching leads with same columns as Top Leads.

### 3. Lead Detail View

Displayed when clicking a lead. Contains:

**Header:**
- Score badge (large)
- Company name
- Region with flag
- Type badges

**Key Metrics (4-up grid):**
- Total monthly volume
- Transaction count
- Client network size
- Trend %

**Pitch Points Card:**
Auto-generated talking points based on data:
- Network connection strength ("Already transacting with X clients")
- FX opportunity (currency corridors)
- Growth trajectory

**Client Connections:**
List of Airwallex clients who transact with this lead:
- Client name
- BD manager name
- Volume with this lead
- Transaction frequency
- Direction (Recv/Pay)

**Transaction History:**
Bar chart showing 12-month volume trend.

**Currency Corridors:**
List of currency pairs with volume (FX opportunity).

**Actions Sidebar:**
- Draft Outreach Email (future: AI-assisted)
- Copy Pitch Points
- Search Web for Info
- Quick stats (rank, data freshness)
- Company info (website, industry, size — web enrichment)

### 4. Upload View

Simple CSV upload interface for monthly data refresh. Accepts both Payment and Remitter files.

## Scoring Algorithm

Composite score (0–100) based on:

```
score = (
  volume_score × 0.35 +
  frequency_score × 0.20 +
  recency_score × 0.15 +
  network_score × 0.30
)
```

**Components:**
- **volume_score:** Percentile rank of monthly_payment_amount / monthly_deposit_usd
- **frequency_score:** Percentile rank of transaction count
- **recency_score:** Decay based on months since last transaction (100 if current month, −10 per month)
- **network_score:** Number of Airwallex clients they transact with (capped at 5 = 100)

Leads appearing in BOTH datasets (receives AND pays) get a 10-point bonus (capped at 100).

## Lead Filtering

**Exclude existing Airwallex clients.** Both datasets have a status column:

| Column | Dataset | Values |
|--------|---------|--------|
| `receiver_customer_status` | Payment | potential lead, existing customer, likely existing customer |
| `customer_status` | Remitter | potential lead, existing customer, likely existing customer |

**Filter logic:**
- **Include:** `potential lead` only
- **Exclude:** `existing customer`, `likely existing customer`

This ensures reps only see net-new prospects, not companies already using Airwallex.

## Lead Deduplication

Counterparties may appear multiple times (different months, different clients). Deduplication logic:

1. Normalize company names (lowercase, strip punctuation, common suffix removal)
2. Group by normalized name
3. Aggregate: sum volumes, max recency, union of currencies, count unique clients
4. Single row per unique counterparty

## Data Processing Pipeline

On CSV upload:

1. **Validate schema** — check required columns exist
2. **Parse dates** — convert payment_month/deposit_month to datetime
3. **Normalize amounts** — convert to USD using static FX rates
4. **Merge datasets** — combine Payment and Remitter, flag source
5. **Deduplicate** — group by normalized company name
6. **Score** — calculate composite score
7. **Enrich** — add country flags, format currencies
8. **Store** — save processed DataFrame to session state

## Tech Stack

- **Framework:** Streamlit
- **Data processing:** pandas
- **Styling:** Custom CSS following Airwallex design standard
- **Deployment:** Streamlit Cloud (free tier) or internal server
- **Storage:** In-memory (session state), no database

## UI/UX Specifications

Following Airwallex Design Standard:

**Colors:**
- Primary orange: #FF6B40
- Dark background: #0A0A0A / #171717
- Gray scale: #262626, #404040, #525252, #737373

**Typography:**
- Font: DM Sans (Circular fallback)
- Monospace for numbers: JetBrains Mono
- Body: 15px
- Headers: 28px

**Components:**
- Border radius: 10–14px
- Cards: dark bg (#171717), 1px border (#262626)
- Buttons: 12px radius, orange primary, gray secondary
- Tables: compact rows (14px padding), hover state

**Region display:** Flag emoji + country name, orange-tinted badge

## Access Control

Full visibility — all reps see all leads. No filtering by BD manager.

## Data Refresh

Manual CSV upload on monthly basis. No real-time database connection.

## Out of Scope (V1)

- Real-time data sync
- AI-generated outreach emails
- CRM integration
- User authentication
- Lead status tracking (contacted, converted)
- Web enrichment API calls (manual for now)

## Success Criteria

1. Rep can find a high-potential lead in < 30 seconds
2. Rep can identify which of their clients to ask for an intro
3. Rep has enough context to craft a personalized pitch
4. Data upload takes < 1 minute for full refresh

## Mockups

Visual mockups saved in `.superpowers/brainstorm/`:
- `dashboard-v4.html` — Top Leads view
- `lead-detail.html` — Lead detail view
