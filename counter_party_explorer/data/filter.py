import pandas as pd

POTENTIAL_LEAD_STATUS = "potential lead"


def filter_potential_leads_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Filter payment data to only include potential leads."""
    return df[df["receiver_customer_status"] == POTENTIAL_LEAD_STATUS].copy()


def filter_potential_leads_remitter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter remitter data to only include potential leads."""
    return df[df["customer_status"] == POTENTIAL_LEAD_STATUS].copy()
