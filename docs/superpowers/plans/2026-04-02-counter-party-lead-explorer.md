# Counter-Party Lead Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit app for sales reps to identify high-potential counterparty leads from transaction data.

**Architecture:** Single-page Streamlit app with sidebar navigation. Data processing layer handles CSV upload, filtering, deduplication, and scoring. UI layer renders dashboard table and lead detail views. All state managed via Streamlit session_state.

**Tech Stack:** Python 3.11+, Streamlit, pandas, pytest

**Spec:** `docs/superpowers/specs/2026-04-02-counter-party-lead-explorer-design.md`

---

## File Structure

```
counter_party_explorer/
├── app.py                      # Main Streamlit entry point, routing
├── data/
│   ├── __init__.py
│   ├── loader.py               # CSV parsing and validation
│   ├── filter.py               # Filter out existing customers
│   ├── deduplicator.py         # Normalize names, merge duplicates
│   ├── scorer.py               # Composite scoring algorithm
│   └── processor.py            # Pipeline orchestrator
├── ui/
│   ├── __init__.py
│   ├── styles.py               # Airwallex CSS constants
│   ├── components.py           # Reusable UI components (badges, cards)
│   ├── dashboard.py            # Top Leads table view
│   ├── lead_detail.py          # Single lead detail view
│   └── upload.py               # CSV upload interface
├── tests/
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_filter.py
│   ├── test_deduplicator.py
│   ├── test_scorer.py
│   ├── test_processor.py
│   └── fixtures/
│       ├── sample_payment.csv
│       └── sample_remitter.csv
├── requirements.txt
└── README.md
```

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `counter_party_explorer/__init__.py`
- Create: `counter_party_explorer/data/__init__.py`
- Create: `counter_party_explorer/ui/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```txt
streamlit>=1.32.0
pandas>=2.2.0
pytest>=8.0.0
pytest-cov>=4.1.0
```

- [ ] **Step 2: Create package structure**

```bash
mkdir -p counter_party_explorer/data counter_party_explorer/ui tests/fixtures
touch counter_party_explorer/__init__.py
touch counter_party_explorer/data/__init__.py
touch counter_party_explorer/ui/__init__.py
touch tests/__init__.py
```

- [ ] **Step 3: Create virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt counter_party_explorer tests
git commit -m "chore: initialize project structure

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Test Fixtures

**Files:**
- Create: `tests/fixtures/sample_payment.csv`
- Create: `tests/fixtures/sample_remitter.csv`

- [ ] **Step 1: Create sample payment fixture**

```csv
payer_account_id,payer_business_name,payer_client_name,bd_manager,payer_total_volume,payer_total_payments,receiver_name,receiver_customer_status,receiver_entity_type,receiver_country,payment_ccy,payment_month,monthly_payment_count,monthly_payment_amount,monthly_payer_amount
acc-001,Client Alpha,Client Alpha,David Tou,50000000,100,Acme Trading Ltd,potential lead,COMPANY,Hong Kong,USD,2026-03-01T00:00:00.000Z,10,500000,500000
acc-001,Client Alpha,Client Alpha,David Tou,50000000,100,Acme Trading Ltd,potential lead,COMPANY,Hong Kong,USD,2026-02-01T00:00:00.000Z,8,400000,400000
acc-002,Client Beta,Client Beta,Vicky Chan,30000000,80,Acme Trading Ltd,potential lead,COMPANY,Hong Kong,HKD,2026-03-01T00:00:00.000Z,5,2000000,250000
acc-001,Client Alpha,Client Alpha,David Tou,50000000,100,Existing Corp,existing customer,COMPANY,Singapore,USD,2026-03-01T00:00:00.000Z,3,100000,100000
acc-003,Client Gamma,Client Gamma,Sarah Lee,20000000,50,Pacific Inc,potential lead,COMPANY,Japan,JPY,2026-03-01T00:00:00.000Z,15,50000000,350000
```

- [ ] **Step 2: Create sample remitter fixture**

```csv
awx_id,client_name,bd_manager,client_go_live_date,priority_score,remitter_account_name,customer_status,ccy,deposit_month,deposit_count,monthly_deposit_amount,monthly_deposit_usd
awx-001,Client Alpha,David Tou,2023-01-15,90,Acme Trading Ltd,potential lead,USD,2026-03-01T00:00:00.000Z,12,600000,600000
awx-001,Client Alpha,David Tou,2023-01-15,90,Acme Trading Ltd,potential lead,USD,2026-02-01T00:00:00.000Z,10,500000,500000
awx-002,Client Beta,Vicky Chan,2023-06-01,85,Delta Supplies,potential lead,HKD,2026-03-01T00:00:00.000Z,8,1500000,190000
awx-003,Client Gamma,Sarah Lee,2024-01-01,70,Existing Corp,existing customer,SGD,2026-03-01T00:00:00.000Z,5,200000,150000
```

- [ ] **Step 3: Commit**

```bash
git add tests/fixtures/
git commit -m "test: add CSV fixtures for unit tests

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: CSV Loader

**Files:**
- Create: `tests/test_loader.py`
- Create: `counter_party_explorer/data/loader.py`

- [ ] **Step 1: Write failing tests for loader**

```python
# tests/test_loader.py
import pytest
import pandas as pd
from pathlib import Path
from counter_party_explorer.data.loader import load_payment_csv, load_remitter_csv, validate_payment_schema, validate_remitter_schema

FIXTURES = Path(__file__).parent / "fixtures"


class TestPaymentLoader:
    def test_load_payment_csv_returns_dataframe(self):
        df = load_payment_csv(FIXTURES / "sample_payment.csv")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5

    def test_load_payment_csv_parses_dates(self):
        df = load_payment_csv(FIXTURES / "sample_payment.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["payment_month"])

    def test_validate_payment_schema_passes_valid(self):
        df = load_payment_csv(FIXTURES / "sample_payment.csv")
        assert validate_payment_schema(df) is True

    def test_validate_payment_schema_fails_missing_column(self):
        df = pd.DataFrame({"wrong_column": [1, 2, 3]})
        assert validate_payment_schema(df) is False


class TestRemitterLoader:
    def test_load_remitter_csv_returns_dataframe(self):
        df = load_remitter_csv(FIXTURES / "sample_remitter.csv")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4

    def test_load_remitter_csv_parses_dates(self):
        df = load_remitter_csv(FIXTURES / "sample_remitter.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["deposit_month"])

    def test_validate_remitter_schema_passes_valid(self):
        df = load_remitter_csv(FIXTURES / "sample_remitter.csv")
        assert validate_remitter_schema(df) is True
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_loader.py -v
```
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement loader**

```python
# counter_party_explorer/data/loader.py
import pandas as pd
from pathlib import Path
from typing import Union

PAYMENT_REQUIRED_COLUMNS = [
    "payer_account_id",
    "payer_business_name",
    "bd_manager",
    "receiver_name",
    "receiver_customer_status",
    "receiver_country",
    "payment_ccy",
    "payment_month",
    "monthly_payment_count",
    "monthly_payment_amount",
]

REMITTER_REQUIRED_COLUMNS = [
    "awx_id",
    "client_name",
    "bd_manager",
    "remitter_account_name",
    "customer_status",
    "ccy",
    "deposit_month",
    "deposit_count",
    "monthly_deposit_usd",
]


def load_payment_csv(path: Union[str, Path]) -> pd.DataFrame:
    """Load payment CSV and parse dates."""
    df = pd.read_csv(path)
    df["payment_month"] = pd.to_datetime(df["payment_month"])
    return df


def load_remitter_csv(path: Union[str, Path]) -> pd.DataFrame:
    """Load remitter CSV and parse dates."""
    df = pd.read_csv(path)
    df["deposit_month"] = pd.to_datetime(df["deposit_month"])
    return df


def validate_payment_schema(df: pd.DataFrame) -> bool:
    """Check that all required payment columns exist."""
    return all(col in df.columns for col in PAYMENT_REQUIRED_COLUMNS)


def validate_remitter_schema(df: pd.DataFrame) -> bool:
    """Check that all required remitter columns exist."""
    return all(col in df.columns for col in REMITTER_REQUIRED_COLUMNS)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_loader.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add counter_party_explorer/data/loader.py tests/test_loader.py
git commit -m "feat: add CSV loader with schema validation

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Lead Filter

**Files:**
- Create: `tests/test_filter.py`
- Create: `counter_party_explorer/data/filter.py`

- [ ] **Step 1: Write failing tests for filter**

```python
# tests/test_filter.py
import pytest
import pandas as pd
from pathlib import Path
from counter_party_explorer.data.loader import load_payment_csv, load_remitter_csv
from counter_party_explorer.data.filter import filter_potential_leads_payment, filter_potential_leads_remitter

FIXTURES = Path(__file__).parent / "fixtures"


class TestPaymentFilter:
    def test_filters_out_existing_customers(self):
        df = load_payment_csv(FIXTURES / "sample_payment.csv")
        filtered = filter_potential_leads_payment(df)
        assert "existing customer" not in filtered["receiver_customer_status"].values

    def test_keeps_potential_leads(self):
        df = load_payment_csv(FIXTURES / "sample_payment.csv")
        filtered = filter_potential_leads_payment(df)
        assert len(filtered) == 4  # 5 rows - 1 existing customer

    def test_filters_out_likely_existing(self):
        df = pd.DataFrame({
            "receiver_name": ["A", "B", "C"],
            "receiver_customer_status": ["potential lead", "likely existing customer", "existing customer"],
        })
        filtered = filter_potential_leads_payment(df)
        assert len(filtered) == 1
        assert filtered.iloc[0]["receiver_name"] == "A"


class TestRemitterFilter:
    def test_filters_out_existing_customers(self):
        df = load_remitter_csv(FIXTURES / "sample_remitter.csv")
        filtered = filter_potential_leads_remitter(df)
        assert "existing customer" not in filtered["customer_status"].values

    def test_keeps_potential_leads(self):
        df = load_remitter_csv(FIXTURES / "sample_remitter.csv")
        filtered = filter_potential_leads_remitter(df)
        assert len(filtered) == 3  # 4 rows - 1 existing customer
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_filter.py -v
```
Expected: FAIL with "cannot import name"

- [ ] **Step 3: Implement filter**

```python
# counter_party_explorer/data/filter.py
import pandas as pd

POTENTIAL_LEAD_STATUS = "potential lead"


def filter_potential_leads_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Filter payment data to only include potential leads."""
    return df[df["receiver_customer_status"] == POTENTIAL_LEAD_STATUS].copy()


def filter_potential_leads_remitter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter remitter data to only include potential leads."""
    return df[df["customer_status"] == POTENTIAL_LEAD_STATUS].copy()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_filter.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add counter_party_explorer/data/filter.py tests/test_filter.py
git commit -m "feat: add lead filter to exclude existing customers

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Name Deduplicator

**Files:**
- Create: `tests/test_deduplicator.py`
- Create: `counter_party_explorer/data/deduplicator.py`

- [ ] **Step 1: Write failing tests for deduplicator**

```python
# tests/test_deduplicator.py
import pytest
import pandas as pd
from counter_party_explorer.data.deduplicator import (
    normalize_company_name,
    deduplicate_leads,
)


class TestNormalizeCompanyName:
    def test_lowercase(self):
        assert normalize_company_name("ACME Corp") == "acme corp"

    def test_strips_common_suffixes(self):
        assert normalize_company_name("Acme Ltd") == "acme"
        assert normalize_company_name("Acme Limited") == "acme"
        assert normalize_company_name("Acme Inc") == "acme"
        assert normalize_company_name("Acme Inc.") == "acme"
        assert normalize_company_name("Acme Co.") == "acme"

    def test_strips_punctuation(self):
        assert normalize_company_name("Acme, Inc.") == "acme"

    def test_strips_whitespace(self):
        assert normalize_company_name("  Acme  Corp  ") == "acme corp"


class TestDeduplicateLeads:
    def test_merges_same_company_different_months(self):
        df = pd.DataFrame({
            "company_name": ["Acme Ltd", "Acme Ltd"],
            "normalized_name": ["acme", "acme"],
            "volume_usd": [100000, 150000],
            "transaction_count": [5, 8],
            "month": pd.to_datetime(["2026-02-01", "2026-03-01"]),
            "client_id": ["c1", "c1"],
            "currencies": [["USD"], ["USD"]],
            "source": ["payment", "payment"],
        })
        result = deduplicate_leads(df)
        assert len(result) == 1
        assert result.iloc[0]["total_volume_usd"] == 250000
        assert result.iloc[0]["total_transactions"] == 13

    def test_counts_unique_clients(self):
        df = pd.DataFrame({
            "company_name": ["Acme Ltd", "Acme Ltd", "Acme Ltd"],
            "normalized_name": ["acme", "acme", "acme"],
            "volume_usd": [100000, 150000, 200000],
            "transaction_count": [5, 8, 10],
            "month": pd.to_datetime(["2026-03-01", "2026-03-01", "2026-03-01"]),
            "client_id": ["c1", "c2", "c1"],
            "currencies": [["USD"], ["HKD"], ["USD"]],
            "source": ["payment", "payment", "remitter"],
        })
        result = deduplicate_leads(df)
        assert len(result) == 1
        assert result.iloc[0]["client_count"] == 2

    def test_unions_currencies(self):
        df = pd.DataFrame({
            "company_name": ["Acme", "Acme"],
            "normalized_name": ["acme", "acme"],
            "volume_usd": [100000, 150000],
            "transaction_count": [5, 8],
            "month": pd.to_datetime(["2026-03-01", "2026-03-01"]),
            "client_id": ["c1", "c2"],
            "currencies": [["USD", "HKD"], ["EUR"]],
            "source": ["payment", "payment"],
        })
        result = deduplicate_leads(df)
        assert set(result.iloc[0]["currencies"]) == {"USD", "HKD", "EUR"}

    def test_tracks_both_sources(self):
        df = pd.DataFrame({
            "company_name": ["Acme", "Acme"],
            "normalized_name": ["acme", "acme"],
            "volume_usd": [100000, 150000],
            "transaction_count": [5, 8],
            "month": pd.to_datetime(["2026-03-01", "2026-03-01"]),
            "client_id": ["c1", "c2"],
            "currencies": [["USD"], ["USD"]],
            "source": ["payment", "remitter"],
        })
        result = deduplicate_leads(df)
        assert result.iloc[0]["receives"] is True
        assert result.iloc[0]["pays"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_deduplicator.py -v
```
Expected: FAIL with "cannot import name"

- [ ] **Step 3: Implement deduplicator**

```python
# counter_party_explorer/data/deduplicator.py
import pandas as pd
import re
from typing import List, Set

SUFFIXES_TO_REMOVE = [
    r"\s+limited$",
    r"\s+ltd\.?$",
    r"\s+inc\.?$",
    r"\s+incorporated$",
    r"\s+corp\.?$",
    r"\s+corporation$",
    r"\s+co\.?$",
    r"\s+company$",
    r"\s+llc\.?$",
    r"\s+plc\.?$",
    r"\s+gmbh$",
    r"\s+pty\.?$",
]


def normalize_company_name(name: str) -> str:
    """Normalize company name for deduplication."""
    if not isinstance(name, str):
        return ""
    
    # Lowercase
    normalized = name.lower().strip()
    
    # Remove punctuation except spaces
    normalized = re.sub(r"[^\w\s]", "", normalized)
    
    # Remove common suffixes
    for suffix in SUFFIXES_TO_REMOVE:
        normalized = re.sub(suffix, "", normalized, flags=re.IGNORECASE)
    
    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()
    
    return normalized


def deduplicate_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deduplicate leads by normalized company name.
    
    Aggregates:
    - total_volume_usd: sum of all volume
    - total_transactions: sum of all transaction counts
    - client_count: count of unique client_ids
    - currencies: union of all currencies
    - receives: True if any source is 'remitter'
    - pays: True if any source is 'payment'
    - latest_month: most recent transaction month
    """
    
    def aggregate_group(group: pd.DataFrame) -> pd.Series:
        # Union all currencies
        all_currencies: Set[str] = set()
        for curr_list in group["currencies"]:
            if isinstance(curr_list, list):
                all_currencies.update(curr_list)
        
        return pd.Series({
            "company_name": group["company_name"].iloc[0],
            "normalized_name": group["normalized_name"].iloc[0],
            "total_volume_usd": group["volume_usd"].sum(),
            "total_transactions": group["transaction_count"].sum(),
            "client_count": group["client_id"].nunique(),
            "currencies": sorted(list(all_currencies)),
            "receives": "remitter" in group["source"].values,
            "pays": "payment" in group["source"].values,
            "latest_month": group["month"].max(),
        })
    
    result = df.groupby("normalized_name").apply(aggregate_group, include_groups=False).reset_index(drop=True)
    return result
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_deduplicator.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add counter_party_explorer/data/deduplicator.py tests/test_deduplicator.py
git commit -m "feat: add company name normalization and deduplication

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Lead Scorer

**Files:**
- Create: `tests/test_scorer.py`
- Create: `counter_party_explorer/data/scorer.py`

- [ ] **Step 1: Write failing tests for scorer**

```python
# tests/test_scorer.py
import pytest
import pandas as pd
from counter_party_explorer.data.scorer import (
    calculate_volume_score,
    calculate_frequency_score,
    calculate_recency_score,
    calculate_network_score,
    calculate_composite_score,
)


class TestVolumeScore:
    def test_highest_volume_gets_100(self):
        volumes = pd.Series([1000, 5000, 10000])
        scores = calculate_volume_score(volumes)
        assert scores.iloc[2] == 100

    def test_lowest_volume_gets_low_score(self):
        volumes = pd.Series([1000, 5000, 10000])
        scores = calculate_volume_score(volumes)
        assert scores.iloc[0] < 50


class TestFrequencyScore:
    def test_highest_frequency_gets_100(self):
        counts = pd.Series([5, 20, 50])
        scores = calculate_frequency_score(counts)
        assert scores.iloc[2] == 100


class TestRecencyScore:
    def test_current_month_gets_100(self):
        current = pd.Timestamp("2026-03-01")
        months = pd.Series([pd.Timestamp("2026-03-01")])
        scores = calculate_recency_score(months, current)
        assert scores.iloc[0] == 100

    def test_old_month_gets_lower_score(self):
        current = pd.Timestamp("2026-03-01")
        months = pd.Series([pd.Timestamp("2025-12-01")])
        scores = calculate_recency_score(months, current)
        assert scores.iloc[0] == 70  # 3 months * 10 = 30 deducted


class TestNetworkScore:
    def test_five_clients_gets_100(self):
        counts = pd.Series([5])
        scores = calculate_network_score(counts)
        assert scores.iloc[0] == 100

    def test_more_than_five_capped_at_100(self):
        counts = pd.Series([10])
        scores = calculate_network_score(counts)
        assert scores.iloc[0] == 100

    def test_one_client_gets_20(self):
        counts = pd.Series([1])
        scores = calculate_network_score(counts)
        assert scores.iloc[0] == 20


class TestCompositeScore:
    def test_composite_calculation(self):
        df = pd.DataFrame({
            "total_volume_usd": [1000000],
            "total_transactions": [50],
            "latest_month": [pd.Timestamp("2026-03-01")],
            "client_count": [5],
            "receives": [True],
            "pays": [True],
        })
        current = pd.Timestamp("2026-03-01")
        result = calculate_composite_score(df, current)
        # With all 100s: 100*0.35 + 100*0.20 + 100*0.15 + 100*0.30 = 100, +10 bonus = 100 (capped)
        assert result.iloc[0]["score"] == 100

    def test_both_receives_and_pays_gets_bonus(self):
        df = pd.DataFrame({
            "total_volume_usd": [500000, 500000],
            "total_transactions": [25, 25],
            "latest_month": [pd.Timestamp("2026-03-01"), pd.Timestamp("2026-03-01")],
            "client_count": [2, 2],
            "receives": [True, True],
            "pays": [True, False],
        })
        current = pd.Timestamp("2026-03-01")
        result = calculate_composite_score(df, current)
        # First has both, second only receives
        assert result.iloc[0]["score"] > result.iloc[1]["score"]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_scorer.py -v
```
Expected: FAIL with "cannot import name"

- [ ] **Step 3: Implement scorer**

```python
# counter_party_explorer/data/scorer.py
import pandas as pd
import numpy as np

# Weights for composite score
WEIGHT_VOLUME = 0.35
WEIGHT_FREQUENCY = 0.20
WEIGHT_RECENCY = 0.15
WEIGHT_NETWORK = 0.30

# Bonus for appearing in both datasets
BOTH_SOURCES_BONUS = 10

# Network score: 20 points per client, capped at 5 clients
POINTS_PER_CLIENT = 20
MAX_CLIENTS_FOR_SCORE = 5

# Recency: 10 points deducted per month old
RECENCY_PENALTY_PER_MONTH = 10


def calculate_volume_score(volumes: pd.Series) -> pd.Series:
    """Calculate percentile-based volume score (0-100)."""
    return volumes.rank(pct=True) * 100


def calculate_frequency_score(counts: pd.Series) -> pd.Series:
    """Calculate percentile-based frequency score (0-100)."""
    return counts.rank(pct=True) * 100


def calculate_recency_score(months: pd.Series, current_month: pd.Timestamp) -> pd.Series:
    """
    Calculate recency score.
    100 for current month, -10 for each month old.
    """
    months_diff = ((current_month.year - months.dt.year) * 12 + 
                   (current_month.month - months.dt.month))
    scores = 100 - (months_diff * RECENCY_PENALTY_PER_MONTH)
    return scores.clip(lower=0)


def calculate_network_score(client_counts: pd.Series) -> pd.Series:
    """
    Calculate network score based on client count.
    20 points per client, capped at 5 clients (100 points).
    """
    scores = client_counts.clip(upper=MAX_CLIENTS_FOR_SCORE) * POINTS_PER_CLIENT
    return scores


def calculate_composite_score(df: pd.DataFrame, current_month: pd.Timestamp) -> pd.DataFrame:
    """
    Calculate composite score for all leads.
    
    Formula:
    score = (volume * 0.35) + (frequency * 0.20) + (recency * 0.15) + (network * 0.30)
    + 10 bonus if both receives and pays
    """
    result = df.copy()
    
    volume_score = calculate_volume_score(df["total_volume_usd"])
    frequency_score = calculate_frequency_score(df["total_transactions"])
    recency_score = calculate_recency_score(df["latest_month"], current_month)
    network_score = calculate_network_score(df["client_count"])
    
    composite = (
        volume_score * WEIGHT_VOLUME +
        frequency_score * WEIGHT_FREQUENCY +
        recency_score * WEIGHT_RECENCY +
        network_score * WEIGHT_NETWORK
    )
    
    # Bonus for both receives and pays
    both_sources = df["receives"] & df["pays"]
    composite = composite + (both_sources * BOTH_SOURCES_BONUS)
    
    # Cap at 100
    result["score"] = composite.clip(upper=100).round().astype(int)
    
    return result
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_scorer.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add counter_party_explorer/data/scorer.py tests/test_scorer.py
git commit -m "feat: add composite lead scoring algorithm

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: Data Processor Pipeline

**Files:**
- Create: `tests/test_processor.py`
- Create: `counter_party_explorer/data/processor.py`

- [ ] **Step 1: Write failing tests for processor**

```python
# tests/test_processor.py
import pytest
import pandas as pd
from pathlib import Path
from counter_party_explorer.data.processor import process_data

FIXTURES = Path(__file__).parent / "fixtures"


class TestProcessor:
    def test_process_returns_dataframe(self):
        result = process_data(
            payment_path=FIXTURES / "sample_payment.csv",
            remitter_path=FIXTURES / "sample_remitter.csv",
        )
        assert isinstance(result, pd.DataFrame)

    def test_filters_out_existing_customers(self):
        result = process_data(
            payment_path=FIXTURES / "sample_payment.csv",
            remitter_path=FIXTURES / "sample_remitter.csv",
        )
        # "Existing Corp" should not appear
        assert "existing corp" not in result["normalized_name"].values

    def test_deduplicates_across_sources(self):
        result = process_data(
            payment_path=FIXTURES / "sample_payment.csv",
            remitter_path=FIXTURES / "sample_remitter.csv",
        )
        # "Acme Trading Ltd" appears in both files, should be merged
        acme_rows = result[result["normalized_name"] == "acme trading"]
        assert len(acme_rows) == 1

    def test_has_required_columns(self):
        result = process_data(
            payment_path=FIXTURES / "sample_payment.csv",
            remitter_path=FIXTURES / "sample_remitter.csv",
        )
        required = ["company_name", "score", "total_volume_usd", "client_count", "receives", "pays"]
        for col in required:
            assert col in result.columns

    def test_sorted_by_score_descending(self):
        result = process_data(
            payment_path=FIXTURES / "sample_payment.csv",
            remitter_path=FIXTURES / "sample_remitter.csv",
        )
        scores = result["score"].tolist()
        assert scores == sorted(scores, reverse=True)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_processor.py -v
```
Expected: FAIL with "cannot import name"

- [ ] **Step 3: Implement processor**

```python
# counter_party_explorer/data/processor.py
import pandas as pd
from pathlib import Path
from typing import Union, Optional

from .loader import load_payment_csv, load_remitter_csv, validate_payment_schema, validate_remitter_schema
from .filter import filter_potential_leads_payment, filter_potential_leads_remitter
from .deduplicator import normalize_company_name, deduplicate_leads
from .scorer import calculate_composite_score

# Static FX rates to USD (approximate, for scoring purposes)
FX_RATES = {
    "USD": 1.0,
    "HKD": 0.128,
    "CNY": 0.14,
    "JPY": 0.0067,
    "EUR": 1.08,
    "GBP": 1.26,
    "AUD": 0.65,
    "SGD": 0.74,
    "CAD": 0.74,
    "CHF": 1.12,
    "NZD": 0.60,
    "KRW": 0.00075,
    "INR": 0.012,
    "IDR": 0.000063,
    "THB": 0.028,
    "MYR": 0.21,
    "PHP": 0.018,
    "VND": 0.00004,
    "SEK": 0.095,
    "NOK": 0.092,
    "DKK": 0.145,
}


def _convert_to_usd(amount: float, currency: str) -> float:
    """Convert amount to USD using static FX rates."""
    rate = FX_RATES.get(currency, 1.0)
    return amount * rate


def _prepare_payment_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform payment data into common schema."""
    result = pd.DataFrame({
        "company_name": df["receiver_name"],
        "normalized_name": df["receiver_name"].apply(normalize_company_name),
        "country": df["receiver_country"],
        "volume_usd": df.apply(
            lambda r: _convert_to_usd(r["monthly_payment_amount"], r["payment_ccy"]), axis=1
        ),
        "transaction_count": df["monthly_payment_count"],
        "month": df["payment_month"],
        "client_id": df["payer_account_id"],
        "client_name": df["payer_business_name"],
        "bd_manager": df["bd_manager"],
        "currencies": df["payment_ccy"].apply(lambda x: [x] if pd.notna(x) else []),
        "source": "payment",
    })
    return result


def _prepare_remitter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform remitter data into common schema."""
    result = pd.DataFrame({
        "company_name": df["remitter_account_name"],
        "normalized_name": df["remitter_account_name"].apply(normalize_company_name),
        "country": None,  # Not available in remitter data
        "volume_usd": df["monthly_deposit_usd"],
        "transaction_count": df["deposit_count"],
        "month": df["deposit_month"],
        "client_id": df["awx_id"],
        "client_name": df["client_name"],
        "bd_manager": df["bd_manager"],
        "currencies": df["ccy"].apply(lambda x: [x] if pd.notna(x) else []),
        "source": "remitter",
    })
    return result


def process_data(
    payment_path: Optional[Union[str, Path]] = None,
    remitter_path: Optional[Union[str, Path]] = None,
    payment_df: Optional[pd.DataFrame] = None,
    remitter_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Process raw CSV data into scored, deduplicated leads.
    
    Args:
        payment_path: Path to payment CSV
        remitter_path: Path to remitter CSV
        payment_df: Pre-loaded payment DataFrame (alternative to path)
        remitter_df: Pre-loaded remitter DataFrame (alternative to path)
    
    Returns:
        DataFrame with scored, deduplicated leads sorted by score descending.
    """
    combined_dfs = []
    
    # Process payment data
    if payment_path is not None:
        payment_df = load_payment_csv(payment_path)
    if payment_df is not None and validate_payment_schema(payment_df):
        filtered = filter_potential_leads_payment(payment_df)
        prepared = _prepare_payment_data(filtered)
        combined_dfs.append(prepared)
    
    # Process remitter data
    if remitter_path is not None:
        remitter_df = load_remitter_csv(remitter_path)
    if remitter_df is not None and validate_remitter_schema(remitter_df):
        filtered = filter_potential_leads_remitter(remitter_df)
        prepared = _prepare_remitter_data(filtered)
        combined_dfs.append(prepared)
    
    if not combined_dfs:
        return pd.DataFrame()
    
    # Combine all data
    combined = pd.concat(combined_dfs, ignore_index=True)
    
    # Filter out empty normalized names
    combined = combined[combined["normalized_name"].str.len() > 0]
    
    # Deduplicate
    deduplicated = deduplicate_leads(combined)
    
    # Get current month for recency scoring
    current_month = combined["month"].max()
    
    # Score
    scored = calculate_composite_score(deduplicated, current_month)
    
    # Sort by score descending
    scored = scored.sort_values("score", ascending=False).reset_index(drop=True)
    
    return scored
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_processor.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add counter_party_explorer/data/processor.py tests/test_processor.py
git commit -m "feat: add data processing pipeline

Orchestrates loading, filtering, deduplication, and scoring.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: UI Styles

**Files:**
- Create: `counter_party_explorer/ui/styles.py`

- [ ] **Step 1: Create Airwallex CSS styles**

```python
# counter_party_explorer/ui/styles.py
"""Airwallex design system styles for Streamlit."""

# Color palette
COLORS = {
    "orange_500": "#FF6B40",
    "orange_600": "#F54D1F",
    "orange_100": "#FFEBE5",
    "success_500": "#22C55E",
    "warning_500": "#F59E0B",
    "error_500": "#EF4444",
    "gray_50": "#FAFAFA",
    "gray_100": "#F5F5F5",
    "gray_200": "#E5E5E5",
    "gray_400": "#A3A3A3",
    "gray_500": "#737373",
    "gray_600": "#525252",
    "gray_700": "#404040",
    "gray_800": "#262626",
    "gray_900": "#171717",
    "gray_950": "#0A0A0A",
}

# Country flags
FLAGS = {
    "Hong Kong": "🇭🇰",
    "China": "🇨🇳",
    "Japan": "🇯🇵",
    "Singapore": "🇸🇬",
    "Australia": "🇦🇺",
    "United Kingdom": "🇬🇧",
    "Germany": "🇩🇪",
    "France": "🇫🇷",
    "Canada": "🇨🇦",
    "United States": "🇺🇸",
    "South Korea": "🇰🇷",
    "India": "🇮🇳",
    "Indonesia": "🇮🇩",
    "Thailand": "🇹🇭",
    "Malaysia": "🇲🇾",
    "Philippines": "🇵🇭",
    "Vietnam": "🇻🇳",
    "Sweden": "🇸🇪",
    "Netherlands": "🇳🇱",
    "New Zealand": "🇳🇿",
}


def get_flag(country: str) -> str:
    """Get flag emoji for country, default to globe."""
    if not country or country == "null":
        return "🌍"
    return FLAGS.get(country, "🌍")


# Global CSS for dark theme
GLOBAL_CSS = """
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Dark theme */
    .stApp {
        background-color: #0A0A0A;
    }
    
    /* Typography */
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FAFAFA !important;
        font-weight: 700 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 12px;
        padding: 16px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #737373 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #FAFAFA !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FF6B40;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 150ms;
    }
    
    .stButton > button:hover {
        background-color: #F54D1F;
        box-shadow: 0 10px 40px -10px rgba(255, 107, 64, 0.4);
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: #262626;
        border: 1px solid #404040;
        color: #D4D4D4;
    }
    
    /* Data tables */
    .stDataFrame {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 12px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 1px solid #262626;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #171717;
        border: 1px solid #404040;
        border-radius: 10px;
        color: #FAFAFA;
        padding: 14px 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B40;
        box-shadow: 0 0 0 3px rgba(255, 107, 64, 0.15);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #171717;
        border: 1px solid #404040;
        border-radius: 10px;
    }
    
    /* Cards */
    .metric-card {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 14px;
        padding: 20px;
    }
    
    /* Score badges */
    .score-high {
        background-color: #22C55E;
        color: white;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    
    .score-medium {
        background-color: #F59E0B;
        color: #171717;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    
    .score-low {
        background-color: #404040;
        color: #D4D4D4;
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    
    /* Type badges */
    .tag-receives {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .tag-pays {
        background-color: rgba(43, 127, 255, 0.15);
        color: #60A5FA;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* Region badge */
    .region-badge {
        background-color: rgba(255, 107, 64, 0.1);
        color: #FF8A66;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 500;
    }
</style>
"""


def score_badge(score: int) -> str:
    """Generate HTML for score badge."""
    if score >= 80:
        cls = "score-high"
    elif score >= 60:
        cls = "score-medium"
    else:
        cls = "score-low"
    return f'<span class="{cls}">{score}</span>'


def type_badges(receives: bool, pays: bool) -> str:
    """Generate HTML for type badges."""
    badges = []
    if receives:
        badges.append('<span class="tag-receives">Recv</span>')
    if pays:
        badges.append('<span class="tag-pays">Pay</span>')
    return " ".join(badges)


def region_badge(country: str) -> str:
    """Generate HTML for region badge."""
    flag = get_flag(country)
    return f'<span class="region-badge">{flag} {country or "Unknown"}</span>'
```

- [ ] **Step 2: Commit**

```bash
git add counter_party_explorer/ui/styles.py
git commit -m "feat: add Airwallex design system styles

Dark theme with orange accents, monospace for numbers.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 9: Dashboard View

**Files:**
- Create: `counter_party_explorer/ui/dashboard.py`

- [ ] **Step 1: Implement dashboard**

```python
# counter_party_explorer/ui/dashboard.py
import streamlit as st
import pandas as pd
from .styles import GLOBAL_CSS, score_badge, type_badges, region_badge, get_flag


def format_volume(amount: float) -> str:
    """Format volume as human-readable string."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:.0f}"


def render_dashboard(df: pd.DataFrame):
    """Render the main leads dashboard."""
    
    # Apply global styles
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Top Leads")
    with col2:
        if st.button("↑ Upload Data", type="primary"):
            st.session_state.view = "upload"
            st.rerun()
    
    # Stats row
    total_leads = len(df)
    high_potential = len(df[df["score"] >= 80])
    total_volume = df["total_volume_usd"].sum()
    multi_client = len(df[df["client_count"] >= 2])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Leads", f"{total_leads:,}")
    c2.metric("High Potential", f"{high_potential:,}", help="Score 80+")
    c3.metric("Network Volume", format_volume(total_volume))
    c4.metric("Multi-Client", f"{multi_client:,}", help="2+ client connections")
    
    st.divider()
    
    # Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search company", placeholder="Search company name...")
    
    with col2:
        # Get unique countries
        countries = ["All"] + sorted(df["country"].dropna().unique().tolist()) if "country" in df.columns else ["All"]
        region_filter = st.selectbox("Region", countries)
    
    with col3:
        type_filter = st.selectbox("Type", ["All", "Receives", "Pays", "Both"])
    
    with col4:
        score_filter = st.selectbox("Score", ["All", "80+", "60-79", "<60"])
    
    # Apply filters
    filtered = df.copy()
    
    if search:
        filtered = filtered[filtered["company_name"].str.contains(search, case=False, na=False)]
    
    if region_filter != "All" and "country" in filtered.columns:
        filtered = filtered[filtered["country"] == region_filter]
    
    if type_filter == "Receives":
        filtered = filtered[filtered["receives"] == True]
    elif type_filter == "Pays":
        filtered = filtered[filtered["pays"] == True]
    elif type_filter == "Both":
        filtered = filtered[(filtered["receives"] == True) & (filtered["pays"] == True)]
    
    if score_filter == "80+":
        filtered = filtered[filtered["score"] >= 80]
    elif score_filter == "60-79":
        filtered = filtered[(filtered["score"] >= 60) & (filtered["score"] < 80)]
    elif score_filter == "<60":
        filtered = filtered[filtered["score"] < 60]
    
    # Results count
    st.caption(f"Showing {len(filtered):,} leads")
    
    # Table
    if len(filtered) == 0:
        st.info("No leads match your filters.")
        return
    
    # Pagination
    page_size = 20
    total_pages = (len(filtered) - 1) // page_size + 1
    
    if "page" not in st.session_state:
        st.session_state.page = 0
    
    start_idx = st.session_state.page * page_size
    end_idx = start_idx + page_size
    page_data = filtered.iloc[start_idx:end_idx]
    
    # Render table
    for idx, row in page_data.iterrows():
        with st.container():
            cols = st.columns([0.8, 2.5, 1.5, 1.2, 1, 1.2, 0.8, 0.8])
            
            # Score
            with cols[0]:
                score_class = "high" if row["score"] >= 80 else "medium" if row["score"] >= 60 else "low"
                st.markdown(f'<div class="score-{score_class}" style="text-align:center;padding:8px;border-radius:8px;font-family:monospace;font-weight:600;">{row["score"]}</div>', unsafe_allow_html=True)
            
            # Company
            with cols[1]:
                st.markdown(f"**{row['company_name']}**")
            
            # Region
            with cols[2]:
                country = row.get("country", "")
                flag = get_flag(country) if country else "🌍"
                st.markdown(f"{flag} {country or 'Unknown'}")
            
            # Type
            with cols[3]:
                types = []
                if row.get("receives"):
                    types.append("Recv")
                if row.get("pays"):
                    types.append("Pay")
                st.markdown(" / ".join(types) if types else "-")
            
            # Volume
            with cols[4]:
                st.markdown(f"`{format_volume(row['total_volume_usd'])}`")
            
            # Clients
            with cols[5]:
                st.markdown(f"{row['client_count']} clients")
            
            # Currencies
            with cols[6]:
                currencies = row.get("currencies", [])
                if currencies:
                    st.markdown(", ".join(currencies[:3]))
            
            # View button
            with cols[7]:
                if st.button("View", key=f"view_{idx}"):
                    st.session_state.selected_lead = row.to_dict()
                    st.session_state.view = "detail"
                    st.rerun()
            
            st.divider()
    
    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pcols = st.columns(5)
        with pcols[0]:
            if st.button("←", disabled=st.session_state.page == 0):
                st.session_state.page -= 1
                st.rerun()
        with pcols[2]:
            st.markdown(f"Page {st.session_state.page + 1} of {total_pages}")
        with pcols[4]:
            if st.button("→", disabled=st.session_state.page >= total_pages - 1):
                st.session_state.page += 1
                st.rerun()
```

- [ ] **Step 2: Commit**

```bash
git add counter_party_explorer/ui/dashboard.py
git commit -m "feat: add dashboard view with filters and pagination

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 10: Lead Detail View

**Files:**
- Create: `counter_party_explorer/ui/lead_detail.py`

- [ ] **Step 1: Implement lead detail view**

```python
# counter_party_explorer/ui/lead_detail.py
import streamlit as st
import pandas as pd
from .styles import GLOBAL_CSS, get_flag


def format_volume(amount: float) -> str:
    """Format volume as human-readable string."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:.0f}"


def render_lead_detail(lead: dict, all_data: pd.DataFrame = None):
    """Render the lead detail view."""
    
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Top Leads"):
        st.session_state.view = "dashboard"
        st.rerun()
    
    st.divider()
    
    # Header
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Score badge
        score = lead.get("score", 0)
        score_color = "#22C55E" if score >= 80 else "#F59E0B" if score >= 60 else "#404040"
        st.markdown(f"""
        <div style="background:{score_color};color:white;padding:20px;border-radius:16px;text-align:center;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:32px;font-weight:700;">{score}</div>
            <div style="font-size:12px;text-transform:uppercase;opacity:0.8;">Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title(lead.get("company_name", "Unknown Company"))
        
        # Meta info
        country = lead.get("country", "")
        flag = get_flag(country)
        
        tags = []
        if lead.get("receives"):
            tags.append("Receives")
        if lead.get("pays"):
            tags.append("Pays")
        
        st.markdown(f"""
        <div style="display:flex;gap:16px;align-items:center;margin-top:8px;">
            <span style="background:rgba(255,107,64,0.1);color:#FF8A66;padding:6px 14px;border-radius:8px;font-weight:600;">{flag} {country or 'Unknown'}</span>
            <span style="color:#A3A3A3;">{' & '.join(tags) if tags else ''}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Volume", format_volume(lead.get("total_volume_usd", 0)), help="Monthly average")
    c2.metric("Transactions", f"{lead.get('total_transactions', 0):,}", help="Per month")
    c3.metric("Client Network", f"{lead.get('client_count', 0)}", help="Airwallex clients")
    
    # Trend placeholder (would need historical data)
    c4.metric("Currencies", ", ".join(lead.get("currencies", [])[:3]))
    
    st.divider()
    
    # Two column layout
    left, right = st.columns([2, 1])
    
    with left:
        # Pitch Points
        st.subheader("💡 Pitch Points")
        
        client_count = lead.get("client_count", 0)
        if client_count >= 2:
            st.success(f"**Strong network connection:** Already transacting with {client_count} of our clients. With Airwallex Pay, settlements would be T+1 instead of T+3.")
        
        currencies = lead.get("currencies", [])
        if len(currencies) >= 2:
            st.info(f"**Multi-currency opportunity:** Active in {', '.join(currencies)} corridors. Could benefit from competitive FX rates and local collection accounts.")
        
        if lead.get("receives") and lead.get("pays"):
            st.warning("**Dual flow:** Both receives from and pays to our clients — strong candidate for full Airwallex suite.")
        
        st.divider()
        
        # Would show client connections here if we had the detail data
        st.subheader("📋 Client Connections")
        st.caption("Your clients who transact with this company")
        st.info("Client connection details would be shown here with the full transaction data.")
    
    with right:
        # Actions
        st.subheader("Actions")
        
        if st.button("📧 Draft Outreach Email", type="primary", use_container_width=True):
            st.info("Email drafting would integrate here")
        
        if st.button("📋 Copy Pitch Points", use_container_width=True):
            pitch = f"""
Lead: {lead.get('company_name')}
Score: {lead.get('score')}
Volume: {format_volume(lead.get('total_volume_usd', 0))}
Client connections: {lead.get('client_count', 0)}
Currencies: {', '.join(lead.get('currencies', []))}
            """
            st.code(pitch)
        
        if st.button("🔍 Search Web for Info", use_container_width=True):
            company = lead.get("company_name", "")
            st.markdown(f"[Search Google](https://www.google.com/search?q={company.replace(' ', '+')})")
        
        st.divider()
        
        # Quick stats
        st.caption("QUICK STATS")
        st.markdown(f"**Lead Score:** {lead.get('score', 0)} / 100")
        st.markdown(f"**Data Freshness:** {lead.get('latest_month', 'N/A')}")
```

- [ ] **Step 2: Commit**

```bash
git add counter_party_explorer/ui/lead_detail.py
git commit -m "feat: add lead detail view with pitch points

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 11: Upload View

**Files:**
- Create: `counter_party_explorer/ui/upload.py`

- [ ] **Step 1: Implement upload view**

```python
# counter_party_explorer/ui/upload.py
import streamlit as st
import pandas as pd
from ..data.processor import process_data
from ..data.loader import validate_payment_schema, validate_remitter_schema
from .styles import GLOBAL_CSS


def render_upload():
    """Render the CSV upload view."""
    
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    
    # Back button (if data exists)
    if "leads_df" in st.session_state and len(st.session_state.leads_df) > 0:
        if st.button("← Back to Dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()
        st.divider()
    
    st.title("Upload Data")
    st.caption("Upload your monthly Payment and Remitter CSV files to refresh leads data.")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Payment Data")
        st.caption("Trade_Lead_Gen_from_Payment.csv")
        payment_file = st.file_uploader(
            "Upload Payment CSV",
            type=["csv"],
            key="payment_upload",
            help="Money leaving clients to suppliers/vendors"
        )
        
        if payment_file:
            try:
                payment_df = pd.read_csv(payment_file)
                if validate_payment_schema(payment_df):
                    st.success(f"✓ Valid payment file ({len(payment_df):,} rows)")
                    st.session_state.payment_df = payment_df
                else:
                    st.error("Invalid schema. Missing required columns.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    with col2:
        st.subheader("Remitter Data")
        st.caption("Trade_Lead_Gen_from_Remitter.csv")
        remitter_file = st.file_uploader(
            "Upload Remitter CSV",
            type=["csv"],
            key="remitter_upload",
            help="Money entering clients from buyers"
        )
        
        if remitter_file:
            try:
                remitter_df = pd.read_csv(remitter_file)
                if validate_remitter_schema(remitter_df):
                    st.success(f"✓ Valid remitter file ({len(remitter_df):,} rows)")
                    st.session_state.remitter_df = remitter_df
                else:
                    st.error("Invalid schema. Missing required columns.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    st.divider()
    
    # Process button
    has_payment = "payment_df" in st.session_state
    has_remitter = "remitter_df" in st.session_state
    
    if has_payment or has_remitter:
        if st.button("🚀 Process Data", type="primary", use_container_width=True):
            with st.spinner("Processing data..."):
                try:
                    leads_df = process_data(
                        payment_df=st.session_state.get("payment_df"),
                        remitter_df=st.session_state.get("remitter_df"),
                    )
                    
                    st.session_state.leads_df = leads_df
                    
                    st.success(f"✓ Processed {len(leads_df):,} unique leads")
                    
                    # Show summary
                    high_potential = len(leads_df[leads_df["score"] >= 80])
                    st.info(f"**{high_potential:,}** high-potential leads (score 80+)")
                    
                    if st.button("View Dashboard →", type="primary"):
                        st.session_state.view = "dashboard"
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error processing data: {e}")
    else:
        st.info("Upload at least one CSV file to continue.")
```

- [ ] **Step 2: Commit**

```bash
git add counter_party_explorer/ui/upload.py
git commit -m "feat: add CSV upload view with validation

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 12: Main App Entry Point

**Files:**
- Create: `counter_party_explorer/app.py`

- [ ] **Step 1: Implement main app with routing**

```python
# counter_party_explorer/app.py
import streamlit as st
import pandas as pd

from ui.dashboard import render_dashboard
from ui.lead_detail import render_lead_detail
from ui.upload import render_upload
from ui.styles import GLOBAL_CSS

# Page config
st.set_page_config(
    page_title="Counter-Party Lead Explorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = "upload"

if "leads_df" not in st.session_state:
    st.session_state.leads_df = pd.DataFrame()

if "selected_lead" not in st.session_state:
    st.session_state.selected_lead = None


def main():
    """Main app routing."""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;padding:16px 0;">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#FF6B40,#FF8A66);border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;color:white;">CP</div>
            <span style="font-weight:600;font-size:16px;">Lead Explorer</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        if st.button("◉ Top Leads", use_container_width=True, 
                     type="primary" if st.session_state.view == "dashboard" else "secondary"):
            st.session_state.view = "dashboard"
            st.rerun()
        
        if st.button("↑ Upload Data", use_container_width=True,
                     type="primary" if st.session_state.view == "upload" else "secondary"):
            st.session_state.view = "upload"
            st.rerun()
        
        st.divider()
        
        # Data status
        if "leads_df" in st.session_state and len(st.session_state.leads_df) > 0:
            st.caption("DATA STATUS")
            st.markdown(f"**{len(st.session_state.leads_df):,}** leads loaded")
    
    # Main content routing
    if st.session_state.view == "upload":
        render_upload()
    
    elif st.session_state.view == "detail" and st.session_state.selected_lead:
        render_lead_detail(st.session_state.selected_lead, st.session_state.leads_df)
    
    elif st.session_state.view == "dashboard":
        if len(st.session_state.leads_df) > 0:
            render_dashboard(st.session_state.leads_df)
        else:
            st.warning("No data loaded. Please upload CSV files first.")
            if st.button("Go to Upload"):
                st.session_state.view = "upload"
                st.rerun()
    
    else:
        render_upload()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add counter_party_explorer/app.py
git commit -m "feat: add main app entry point with routing

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 13: Integration Test

**Files:**
- Run full app test

- [ ] **Step 1: Run all unit tests**

```bash
pytest tests/ -v --cov=counter_party_explorer
```
Expected: All PASS with coverage report

- [ ] **Step 2: Manual smoke test**

```bash
cd counter_party_explorer
streamlit run app.py
```

Test checklist:
- [ ] Upload page loads
- [ ] Can upload Payment CSV
- [ ] Can upload Remitter CSV  
- [ ] Process button works
- [ ] Dashboard shows leads
- [ ] Filters work (search, region, type, score)
- [ ] Pagination works
- [ ] Click lead opens detail view
- [ ] Back button returns to dashboard

- [ ] **Step 3: Commit any fixes**

```bash
git add -A
git commit -m "fix: integration test fixes

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 14: Documentation

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README**

```markdown
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

## Scoring Algorithm

Composite score (0–100) based on:
- Volume (35%): Transaction amount in USD
- Frequency (20%): Number of transactions
- Recency (15%): How recent the last transaction
- Network (30%): Number of Airwallex clients they transact with

+10 bonus for leads that both receive from AND pay to our clients.

## Tech Stack

- Python 3.11+
- Streamlit
- pandas
- pytest

## Development

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=counter_party_explorer
```
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with setup and usage instructions

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

**Total Tasks:** 14
**Estimated Time:** 2-3 hours

**Key Deliverables:**
1. Data processing pipeline (loader, filter, deduplicator, scorer)
2. Streamlit UI (dashboard, detail, upload views)
3. Airwallex-branded styling
4. Test suite with fixtures
5. Documentation

**Run Order:** Tasks are sequential — each builds on the previous.
