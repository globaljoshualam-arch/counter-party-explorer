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
