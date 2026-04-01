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
