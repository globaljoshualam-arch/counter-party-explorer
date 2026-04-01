import pandas as pd

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
