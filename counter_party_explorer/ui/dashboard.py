"""Main dashboard view with filters and lead table."""

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


def render_dashboard(df: pd.DataFrame):
    """Main dashboard with stats, filters, and lead table."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(render_logo(), unsafe_allow_html=True)

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Header
    st.markdown("# Top Leads")

    # Stats cards using columns
    col1, col2, col3, col4 = st.columns(4)

    total_leads = len(df)
    high_potential = len(df[df["score"] >= 80])
    network_volume = df["total_volume_usd"].sum()
    multi_client = len(df[df["client_count"] > 1])

    with col1:
        st.metric("Total Leads", f"{total_leads:,}", help="Unique counterparties")
    with col2:
        st.metric("High Potential", f"{high_potential:,}", help="Score 80+")
    with col3:
        st.metric("Network Volume", format_volume(network_volume), help="Monthly transactions")
    with col4:
        st.metric("Multi-Client", f"{multi_client:,}", help="2+ client connections")

    st.divider()

    # Filters row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        search = st.text_input("🔍 Search", placeholder="Company name...", label_visibility="collapsed")

    with col2:
        # Get all unique currencies from the currencies lists
        all_currencies = set()
        for curr_list in df["currencies"]:
            if isinstance(curr_list, list):
                all_currencies.update(curr_list)
        currency_options = ["All Currencies"] + sorted(list(all_currencies))
        currency_filter = st.selectbox("Currency", currency_options, label_visibility="collapsed")

    with col3:
        type_filter = st.selectbox("Type", ["All Types", "Receives", "Pays", "Both"], label_visibility="collapsed")

    with col4:
        score_filter = st.selectbox("Score", ["All Scores", "80+", "60-79", "<60"], label_visibility="collapsed")

    # Apply filters
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["company_name"].str.contains(search, case=False, na=False)
        ]

    if currency_filter != "All Currencies":
        filtered_df = filtered_df[filtered_df["currencies"].apply(lambda x: currency_filter in x if isinstance(x, list) else False)]

    if type_filter == "Receives":
        filtered_df = filtered_df[filtered_df["receives"] == True]
    elif type_filter == "Pays":
        filtered_df = filtered_df[filtered_df["pays"] == True]
    elif type_filter == "Both":
        filtered_df = filtered_df[(filtered_df["receives"] == True) & (filtered_df["pays"] == True)]

    if score_filter == "80+":
        filtered_df = filtered_df[filtered_df["score"] >= 80]
    elif score_filter == "60-79":
        filtered_df = filtered_df[(filtered_df["score"] >= 60) & (filtered_df["score"] < 80)]
    elif score_filter == "<60":
        filtered_df = filtered_df[filtered_df["score"] < 60]

    # Pagination
    items_per_page = 15
    total_pages = max(1, (len(filtered_df) - 1) // items_per_page + 1)

    if st.session_state.current_page > total_pages:
        st.session_state.current_page = 1

    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]

    # Results count
    st.caption(f"Showing {len(filtered_df):,} leads")

    if len(page_df) == 0:
        st.info("No leads found matching your filters.")
        return

    # Render each lead as a card/row
    for idx, row in page_df.iterrows():
        score = int(row.get("score", 0))
        company_name = row.get("company_name", "Unknown")
        country = row.get("country")
        if not country or not isinstance(country, str):
            country = "—"
        flag = get_flag(country) if country != "—" else ""
        receives = row.get("receives", False)
        pays = row.get("pays", False)
        volume = row.get("total_volume_usd", 0)
        txn_count = row.get("total_transactions", 0)
        client_count = row.get("client_count", 0)
        currencies = row.get("currencies", [])
        if isinstance(currencies, str):
            currencies = [currencies] if currencies else []

        # Score color
        if score >= 80:
            score_color = "🟢"
        elif score >= 60:
            score_color = "🟡"
        else:
            score_color = "⚪"

        # Type indicator
        type_str = ""
        if receives and pays:
            type_str = "↔️ Both"
        elif receives:
            type_str = "📥 Receives"
        elif pays:
            type_str = "📤 Pays"

        # Currency display
        currency_str = ", ".join(currencies[:3])
        if len(currencies) > 3:
            currency_str += f" +{len(currencies) - 3}"

        # Create row with columns
        cols = st.columns([0.8, 3, 1.2, 1, 1.2, 0.8, 1.5, 1])

        with cols[0]:
            st.markdown(f"**{score_color} {score}**")
        with cols[1]:
            st.markdown(f"**{company_name}**")
        with cols[2]:
            st.markdown(f"{flag} {country}")
        with cols[3]:
            st.markdown(type_str)
        with cols[4]:
            st.markdown(f"**{format_volume(volume)}**")
        with cols[5]:
            st.markdown(f"{client_count} clients")
        with cols[6]:
            st.markdown(f"`{currency_str}`" if currency_str else "—")
        with cols[7]:
            if st.button("View →", key=f"view_{idx}"):
                st.session_state.view = "detail"
                st.session_state.selected_lead = row.to_dict()
                st.rerun()

        st.divider()

    # Pagination controls
    if total_pages > 1:
        col1, col2, col3 = st.columns([2, 1, 2])

        with col1:
            if st.session_state.current_page > 1:
                if st.button("← Previous"):
                    st.session_state.current_page -= 1
                    st.rerun()

        with col2:
            st.caption(f"Page {st.session_state.current_page} of {total_pages}")

        with col3:
            if st.session_state.current_page < total_pages:
                if st.button("Next →"):
                    st.session_state.current_page += 1
                    st.rerun()
