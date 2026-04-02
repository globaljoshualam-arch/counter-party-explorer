"""Main dashboard view with filters and pagination."""

import streamlit as st
import pandas as pd

from counter_party_explorer.ui.styles import GLOBAL_CSS, score_badge, type_badges, region_badge, get_flag


def format_volume(amount: float) -> str:
    """Format volume as $1.2M, $500K, etc."""
    if pd.isna(amount) or not amount:
        return "$0"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:.0f}"


def render_dashboard(df: pd.DataFrame):
    """Main dashboard function with filters and pagination."""
    # Apply global CSS
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Top Leads")
    with col2:
        if st.button("📤 Upload Data", type="primary"):
            st.session_state.view = "upload"
            st.rerun()

    # Metrics
    total_leads = len(df)
    high_potential = len(df[df["score"] >= 80])
    network_volume = df["total_volume_usd"].sum()
    multi_client = len(df[df["client_count"] > 1])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", f"{total_leads:,}")
    with col2:
        st.metric("High Potential", f"{high_potential:,}", help="Score 80+")
    with col3:
        st.metric("Network Volume", format_volume(network_volume))
    with col4:
        st.metric("Multi-Client", f"{multi_client:,}", help="2+ client connections")

    st.divider()

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        search = st.text_input("🔍 Search", placeholder="Company name...")

    with col2:
        # Handle null countries
        countries = df["country"].dropna().unique().tolist()
        regions = ["All"] + sorted([c for c in countries if c])
        region_filter = st.selectbox("🌍 Region", regions)

    with col3:
        type_filter = st.selectbox("💱 Type", ["All", "Receives", "Pays", "Both"])

    with col4:
        score_filter = st.selectbox("⭐ Score", ["All", "80+", "60-79", "<60"])

    # Apply filters
    filtered_df = df.copy()

    # Search filter
    if search:
        filtered_df = filtered_df[
            filtered_df["company_name"].str.contains(search, case=False, na=False)
        ]

    # Region filter
    if region_filter != "All":
        filtered_df = filtered_df[filtered_df["country"] == region_filter]

    # Type filter (using boolean receives/pays columns)
    if type_filter == "Receives":
        filtered_df = filtered_df[filtered_df["receives"] == True]
    elif type_filter == "Pays":
        filtered_df = filtered_df[filtered_df["pays"] == True]
    elif type_filter == "Both":
        filtered_df = filtered_df[(filtered_df["receives"] == True) & (filtered_df["pays"] == True)]

    # Score filter
    if score_filter == "80+":
        filtered_df = filtered_df[filtered_df["score"] >= 80]
    elif score_filter == "60-79":
        filtered_df = filtered_df[(filtered_df["score"] >= 60) & (filtered_df["score"] < 80)]
    elif score_filter == "<60":
        filtered_df = filtered_df[filtered_df["score"] < 60]

    # Pagination
    items_per_page = 20
    total_pages = max(1, (len(filtered_df) - 1) // items_per_page + 1)

    # Ensure current page is valid
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = 1

    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]

    st.caption(f"Showing {len(filtered_df):,} leads")

    # Leads table
    if len(page_df) == 0:
        st.info("No leads found matching your filters.")
    else:
        for idx, row in page_df.iterrows():
            with st.container():
                cols = st.columns([0.8, 2.5, 1.5, 1.2, 1.2, 0.8, 1.2, 0.6])

                # Score
                with cols[0]:
                    score = row["score"]
                    if score >= 80:
                        color = "#22C55E"
                    elif score >= 60:
                        color = "#F59E0B"
                    else:
                        color = "#404040"
                    st.markdown(f'<div style="background:{color};color:white;padding:8px;border-radius:8px;text-align:center;font-family:monospace;font-weight:600;">{score}</div>', unsafe_allow_html=True)

                # Company
                with cols[1]:
                    st.markdown(f"**{row['company_name']}**")

                # Region
                with cols[2]:
                    country = row.get("country") or "Unknown"
                    flag = get_flag(country)
                    st.markdown(f'<span style="background:rgba(255,107,64,0.1);color:#FF8A66;padding:4px 10px;border-radius:6px;">{flag} {country}</span>', unsafe_allow_html=True)

                # Type
                with cols[3]:
                    receives = row.get("receives", False)
                    pays = row.get("pays", False)
                    types = []
                    if receives:
                        types.append('<span style="color:#4ADE80;">Recv</span>')
                    if pays:
                        types.append('<span style="color:#60A5FA;">Pay</span>')
                    st.markdown(" / ".join(types) if types else "—", unsafe_allow_html=True)

                # Volume
                with cols[4]:
                    st.markdown(f'<span style="font-family:monospace;">{format_volume(row["total_volume_usd"])}</span>', unsafe_allow_html=True)

                # Clients
                with cols[5]:
                    st.markdown(f'<span style="font-family:monospace;">{row["client_count"]}</span>', unsafe_allow_html=True)

                # Currencies
                with cols[6]:
                    currencies = row.get("currencies", [])
                    if isinstance(currencies, list) and currencies:
                        display = ", ".join(currencies[:3])
                        if len(currencies) > 3:
                            display += f" +{len(currencies) - 3}"
                        st.markdown(f'<span style="font-family:monospace;font-size:12px;">{display}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown("—")

                # View button
                with cols[7]:
                    if st.button("👁️", key=f"view_{idx}"):
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
            st.markdown(
                f'<div style="text-align: center; padding: 8px;">'
                f'Page {st.session_state.current_page} of {total_pages}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col3:
            if st.session_state.current_page < total_pages:
                if st.button("Next →"):
                    st.session_state.current_page += 1
                    st.rerun()
