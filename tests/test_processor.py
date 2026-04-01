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
