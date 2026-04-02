# Counter-Party Lead Explorer

A Streamlit app for Airwallex sales reps to identify high-potential counterparty leads from transaction data.

## Features

- **Top Leads Dashboard**: Ranked list of potential leads with composite scoring
- **Search & Filter**: Find leads by company name, region, type, or score
- **Lead Detail View**: Full context including pitch points, client connections, and actions
- **CSV Upload**: Monthly data refresh via simple upload interface

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
cd counter_party_explorer
streamlit run app.py
```

## Data Files

Upload two CSV files:

1. **Trade_Lead_Gen_from_Payment.csv** — Money leaving clients (payments to suppliers)
2. **Trade_Lead_Gen_from_Remitter.csv** — Money entering clients (deposits from buyers)

### Required Columns

**Payment CSV:**
- payer_account_id, payer_business_name, bd_manager
- receiver_name, receiver_customer_status, receiver_country
- payment_ccy, payment_month, monthly_payment_count, monthly_payment_amount

**Remitter CSV:**
- awx_id, client_name, bd_manager
- remitter_account_name, customer_status
- ccy, deposit_month, deposit_count, monthly_deposit_usd

## Scoring Algorithm

Composite score (0–100) based on:

| Component | Weight | Description |
|-----------|--------|-------------|
| Volume | 35% | Transaction amount in USD |
| Frequency | 20% | Number of transactions |
| Recency | 15% | How recent the last transaction |
| Network | 30% | Number of Airwallex clients they transact with |

**+10 bonus** for leads that both receive from AND pay to our clients.

## Lead Filtering

Only **potential leads** are shown. Existing Airwallex clients are automatically filtered out based on `receiver_customer_status` and `customer_status` columns.

## Tech Stack

- Python 3.11+
- Streamlit
- pandas
- pytest

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=counter_party_explorer
```

## Project Structure

```
counter_party_explorer/
├── app.py                  # Main Streamlit entry point
├── data/
│   ├── loader.py           # CSV parsing and validation
│   ├── filter.py           # Filter out existing customers
│   ├── deduplicator.py     # Normalize names, merge duplicates
│   ├── scorer.py           # Composite scoring algorithm
│   └── processor.py        # Pipeline orchestrator
├── ui/
│   ├── styles.py           # Airwallex CSS
│   ├── dashboard.py        # Top Leads table view
│   ├── lead_detail.py      # Lead detail view
│   └── upload.py           # CSV upload interface
└── tests/
    ├── fixtures/           # Sample CSV files
    ├── test_loader.py
    ├── test_filter.py
    ├── test_deduplicator.py
    ├── test_scorer.py
    └── test_processor.py
```
