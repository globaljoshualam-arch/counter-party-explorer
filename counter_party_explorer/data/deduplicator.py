import pandas as pd
import re
from typing import Set

SUFFIXES_TO_REMOVE = [
    r"\s+limited$",
    r"\s+ltd\.?$",
    r"\s+inc\.?$",
    r"\s+incorporated$",
    r"\s+corporation$",
    r"\s+co\.$",
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

    # Remove common suffixes first (before removing punctuation)
    for suffix in SUFFIXES_TO_REMOVE:
        normalized = re.sub(suffix, "", normalized, flags=re.IGNORECASE)

    # Remove punctuation except spaces
    normalized = re.sub(r"[^\w\s]", "", normalized)

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

        # Get the normalized_name from the group's name (the groupby key)
        normalized_name = group.name if hasattr(group, 'name') else group.index[0]

        # Get first non-null country
        country_values = group["country"].dropna()
        country = country_values.iloc[0] if len(country_values) > 0 else None

        # Aggregate client-level details (name, volume, transaction count)
        client_details = []
        client_agg = group.groupby("client_id").agg({
            "client_name": "first",
            "volume_usd": "sum",
            "transaction_count": "sum",
            "bd_manager": "first",
        }).reset_index()

        for _, client_row in client_agg.iterrows():
            client_details.append({
                "client_id": client_row["client_id"],
                "client_name": client_row["client_name"] if pd.notna(client_row["client_name"]) else "Unknown",
                "volume_usd": float(client_row["volume_usd"]),
                "transaction_count": int(client_row["transaction_count"]),
                "bd_manager": client_row["bd_manager"] if pd.notna(client_row["bd_manager"]) else None,
            })

        # Sort by volume descending
        client_details = sorted(client_details, key=lambda x: x["volume_usd"], reverse=True)

        result = pd.Series({
            "company_name": group["company_name"].iloc[0],
            "normalized_name": normalized_name,
            "country": country,
            "total_volume_usd": group["volume_usd"].sum(),
            "total_transactions": group["transaction_count"].sum(),
            "client_count": group["client_id"].nunique(),
            "client_details": client_details,
            "currencies": sorted(list(all_currencies)),
            "receives": bool("remitter" in group["source"].values),
            "pays": bool("payment" in group["source"].values),
            "latest_month": group["month"].max(),
        })
        # Convert numpy bools to Python bools
        result["receives"] = bool(result["receives"])
        result["pays"] = bool(result["pays"])
        return result

    result = df.groupby("normalized_name", group_keys=False).apply(aggregate_group, include_groups=False).reset_index(drop=True)

    # Convert numpy bools to Python bools for compatibility with identity checks
    result["receives"] = result["receives"].astype(object)
    result["pays"] = result["pays"].astype(object)

    return result
