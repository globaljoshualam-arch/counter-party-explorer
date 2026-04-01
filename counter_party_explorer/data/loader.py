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
