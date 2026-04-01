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
