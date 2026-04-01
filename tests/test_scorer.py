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
