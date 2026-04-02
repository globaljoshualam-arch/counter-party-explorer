"""Top Clients dashboard - client-centric view of counterparty opportunities."""

import streamlit as st
import pandas as pd

from counter_party_explorer.ui.styles import GLOBAL_CSS, get_flag, render_logo


def format_volume(amount: float) -> str:
    """Format volume as $1.2M, $500K, etc."""
    if pd.isna(amount) or not amount:
        return "$0"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:.0f}"


def build_clients_data(leads_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform lead-centric data to client-centric data.

    Each row becomes a client with their associated counterparty leads.
    """
    client_records = []

    for _, lead_row in leads_df.iterrows():
        client_details = lead_row.get("client_details", [])
        if not client_details:
            continue

        for client in client_details:
            client_records.append({
                "client_id": client.get("client_id"),
                "client_name": client.get("client_name", "Unknown"),
                "bd_manager": client.get("bd_manager"),
                "lead_company": lead_row.get("company_name"),
                "lead_country": lead_row.get("country"),
                "lead_score": lead_row.get("score", 0),
                "volume_usd": client.get("volume_usd", 0),
                "transaction_count": client.get("transaction_count", 0),
                "currencies": lead_row.get("currencies", []),
                "receives": lead_row.get("receives", False),
                "pays": lead_row.get("pays", False),
                "latest_month": lead_row.get("latest_month"),
            })

    if not client_records:
        return pd.DataFrame()

    client_df = pd.DataFrame(client_records)

    # Aggregate by client
    def aggregate_client(group):
        # Get all leads for this client
        leads = []
        all_currencies = set()

        for _, row in group.iterrows():
            leads.append({
                "company_name": row["lead_company"],
                "country": row["lead_country"],
                "score": row["lead_score"],
                "volume_usd": row["volume_usd"],
                "transaction_count": row["transaction_count"],
                "currencies": row["currencies"],
                "receives": row["receives"],
                "pays": row["pays"],
                "latest_month": row["latest_month"],
            })
            if isinstance(row["currencies"], list):
                all_currencies.update(row["currencies"])

        # Sort leads by score descending
        leads = sorted(leads, key=lambda x: x["score"], reverse=True)

        # Count high potential leads (score >= 80)
        high_potential_count = sum(1 for l in leads if l["score"] >= 80)

        # Calculate opportunity score for ranking
        # Weighted: high potential leads count most, then total volume
        total_volume = sum(l["volume_usd"] for l in leads)
        opportunity_score = (high_potential_count * 20) + min(80, total_volume / 100000)

        return pd.Series({
            "client_name": group["client_name"].iloc[0],
            "bd_manager": group["bd_manager"].iloc[0],
            "lead_count": len(leads),
            "high_potential_count": high_potential_count,
            "total_volume_usd": total_volume,
            "currencies": sorted(list(all_currencies)),
            "leads": leads,
            "opportunity_score": opportunity_score,
        })

    result = client_df.groupby("client_id", group_keys=False).apply(
        aggregate_client, include_groups=False
    ).reset_index()

    # Sort by opportunity score
    result = result.sort_values("opportunity_score", ascending=False).reset_index(drop=True)

    return result


def render_clients_dashboard(leads_df: pd.DataFrame):
    """Main clients dashboard with stats, filters, and client table."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(render_logo(), unsafe_allow_html=True)

    # Build client-centric data
    if "clients_df" not in st.session_state:
        st.session_state.clients_df = build_clients_data(leads_df)

    df = st.session_state.clients_df

    if len(df) == 0:
        st.warning("No client data available.")
        return

    # Initialize pagination
    if "clients_page" not in st.session_state:
        st.session_state.clients_page = 1

    # Header
    st.markdown("# Top Clients")
    st.caption("Airwallex clients with counterparty lead opportunities")

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)

    total_clients = len(df)
    clients_with_high_potential = len(df[df["high_potential_count"] > 0])
    total_leads = df["lead_count"].sum()
    total_volume = df["total_volume_usd"].sum()

    with col1:
        st.metric("Total Clients", f"{total_clients:,}", help="Clients with counterparty activity")
    with col2:
        st.metric("High Opportunity", f"{clients_with_high_potential:,}", help="Clients with 80+ score leads")
    with col3:
        st.metric("Total Leads", f"{total_leads:,}", help="Counterparty connections")
    with col4:
        st.metric("Network Volume", format_volume(total_volume), help="Total transaction volume")

    st.divider()

    # Filters
    col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])

    with col1:
        search = st.text_input("🔍 Search", placeholder="Client name...", label_visibility="collapsed", key="client_search")

    with col2:
        # BD Manager filter
        bd_managers = df["bd_manager"].dropna().unique().tolist()
        bd_options = ["All BD Managers"] + sorted([b for b in bd_managers if b and isinstance(b, str)])
        bd_filter = st.selectbox("BD Manager", bd_options, label_visibility="collapsed", key="bd_filter")

    with col3:
        # Currency filter
        all_currencies = set()
        for curr_list in df["currencies"]:
            if isinstance(curr_list, list):
                all_currencies.update(curr_list)
        currency_options = ["All Currencies"] + sorted(list(all_currencies))
        currency_filter = st.selectbox("Currency", currency_options, label_visibility="collapsed", key="client_currency")

    with col4:
        min_leads = st.selectbox("Min Leads", ["Any", "2+", "5+", "10+"], label_visibility="collapsed", key="min_leads")

    # Apply filters
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["client_name"].str.contains(search, case=False, na=False)
        ]

    if bd_filter != "All BD Managers":
        filtered_df = filtered_df[filtered_df["bd_manager"] == bd_filter]

    if currency_filter != "All Currencies":
        filtered_df = filtered_df[
            filtered_df["currencies"].apply(lambda x: currency_filter in x if isinstance(x, list) else False)
        ]

    if min_leads == "2+":
        filtered_df = filtered_df[filtered_df["lead_count"] >= 2]
    elif min_leads == "5+":
        filtered_df = filtered_df[filtered_df["lead_count"] >= 5]
    elif min_leads == "10+":
        filtered_df = filtered_df[filtered_df["lead_count"] >= 10]

    # Pagination
    items_per_page = 15
    total_pages = max(1, (len(filtered_df) - 1) // items_per_page + 1)

    if st.session_state.clients_page > total_pages:
        st.session_state.clients_page = 1

    start_idx = (st.session_state.clients_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]

    # Results count
    st.caption(f"Showing {len(filtered_df):,} clients")

    if len(page_df) == 0:
        st.info("No clients found matching your filters.")
        return

    # Render each client row
    for idx, row in page_df.iterrows():
        client_name = row.get("client_name", "Unknown")
        bd_manager = row.get("bd_manager") or "—"
        lead_count = row.get("lead_count", 0)
        high_potential = row.get("high_potential_count", 0)
        total_vol = row.get("total_volume_usd", 0)
        currencies = row.get("currencies", [])

        # High potential indicator
        if high_potential >= 5:
            potential_indicator = "🔥"
        elif high_potential >= 2:
            potential_indicator = "🟢"
        elif high_potential >= 1:
            potential_indicator = "🟡"
        else:
            potential_indicator = "⚪"

        currency_str = ", ".join(currencies[:3])
        if len(currencies) > 3:
            currency_str += f" +{len(currencies) - 3}"

        # Create row with columns
        cols = st.columns([0.6, 2.5, 1.5, 1, 1.2, 1.5, 1])

        with cols[0]:
            st.markdown(f"**{potential_indicator} {high_potential}**")
        with cols[1]:
            st.markdown(f"**{client_name}**")
        with cols[2]:
            st.markdown(f"{bd_manager}")
        with cols[3]:
            st.markdown(f"{lead_count} leads")
        with cols[4]:
            st.markdown(f"**{format_volume(total_vol)}**")
        with cols[5]:
            st.markdown(f"`{currency_str}`" if currency_str else "—")
        with cols[6]:
            if st.button("View →", key=f"view_client_{idx}"):
                st.session_state.view = "client_detail"
                st.session_state.selected_client = row.to_dict()
                st.rerun()

        st.divider()

    # Pagination controls
    if total_pages > 1:
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if st.session_state.clients_page > 1:
                if st.button("← Previous", key="clients_prev"):
                    st.session_state.clients_page -= 1
                    st.rerun()

        with col2:
            st.caption(f"Page {st.session_state.clients_page} of {total_pages}")

        with col3:
            if st.session_state.clients_page < total_pages:
                if st.button("Next →", key="clients_next"):
                    st.session_state.clients_page += 1
                    st.rerun()
