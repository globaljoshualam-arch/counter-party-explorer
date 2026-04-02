"""Main dashboard view with filters and pagination."""

import streamlit as st
import pandas as pd

from .styles import GLOBAL_CSS, score_badge, type_badges, region_badge, get_flag


def format_volume(amount: float) -> str:
    """Format volume as $1.2M, $500K, etc."""
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
    if "current_view" not in st.session_state:
        st.session_state.current_view = "dashboard"
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Top Leads")
    with col2:
        if st.button("📤 Upload"):
            st.session_state.current_view = "upload"
            st.rerun()

    # Metrics
    total_leads = len(df)
    high_potential = len(df[df["score"] >= 80])
    network_volume = df["total_volume"].sum()
    multi_client = len(df[df["client_count"] > 1])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", f"{total_leads:,}")
    with col2:
        st.metric("High Potential", f"{high_potential:,}")
    with col3:
        st.metric("Network Volume", format_volume(network_volume))
    with col4:
        st.metric("Multi-Client", f"{multi_client:,}")

    st.markdown("---")

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        search = st.text_input("🔍 Search", placeholder="Company name...")

    with col2:
        regions = ["All"] + sorted(df["country"].unique().tolist())
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

    # Type filter
    if type_filter == "Receives":
        filtered_df = filtered_df[
            (filtered_df["receives_currencies"].notna()) &
            (filtered_df["receives_currencies"] != "") &
            ((filtered_df["pays_currencies"].isna()) | (filtered_df["pays_currencies"] == ""))
        ]
    elif type_filter == "Pays":
        filtered_df = filtered_df[
            (filtered_df["pays_currencies"].notna()) &
            (filtered_df["pays_currencies"] != "") &
            ((filtered_df["receives_currencies"].isna()) | (filtered_df["receives_currencies"] == ""))
        ]
    elif type_filter == "Both":
        filtered_df = filtered_df[
            (filtered_df["receives_currencies"].notna()) &
            (filtered_df["receives_currencies"] != "") &
            (filtered_df["pays_currencies"].notna()) &
            (filtered_df["pays_currencies"] != "")
        ]

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

    st.markdown(f"**Showing {len(filtered_df):,} leads**")
    st.markdown("---")

    # Leads table
    if len(page_df) == 0:
        st.info("No leads found matching your filters.")
    else:
        for idx, row in page_df.iterrows():
            with st.container():
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 2, 1.5, 1.5, 1.5, 1, 1.5, 1])

                with col1:
                    st.markdown(score_badge(row["score"]), unsafe_allow_html=True)

                with col2:
                    st.markdown(f"**{row['company_name']}**")

                with col3:
                    st.markdown(region_badge(row["country"]), unsafe_allow_html=True)

                with col4:
                    receives = row.get("receives_currencies", "") or ""
                    pays = row.get("pays_currencies", "") or ""
                    if receives or pays:
                        st.markdown(type_badges(receives, pays), unsafe_allow_html=True)
                    else:
                        st.markdown("—")

                with col5:
                    st.markdown(f'<span class="mono">{format_volume(row["total_volume"])}</span>', unsafe_allow_html=True)

                with col6:
                    st.markdown(f'<span class="mono">{row["client_count"]}</span>', unsafe_allow_html=True)

                with col7:
                    currencies = row.get("all_currencies", "") or ""
                    if currencies:
                        currency_list = [c.strip() for c in currencies.split(",")]
                        display = ", ".join(currency_list[:3])
                        if len(currency_list) > 3:
                            display += f" +{len(currency_list) - 3}"
                        st.markdown(f'<span class="mono">{display}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown("—")

                with col8:
                    if st.button("👁️", key=f"view_{idx}"):
                        st.session_state.current_view = "detail"
                        st.session_state.selected_company = row["company_name"]
                        st.rerun()

                st.markdown("---")

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
