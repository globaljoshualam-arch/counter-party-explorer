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
