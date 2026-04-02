"""Lead detail view with pitch points and client connections."""

import streamlit as st
import pandas as pd
from counter_party_explorer.ui.styles import GLOBAL_CSS, get_flag


def format_volume(amount):
    """Format volume amounts consistently."""
    if not amount or pd.isna(amount):
        return "$0"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    else:
        return f"${amount:.0f}"


def render_lead_detail(lead: dict, all_data: pd.DataFrame = None):
    """Render detailed view for a single lead with pitch points."""

    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Top Leads"):
        st.session_state.view = "dashboard"
        st.session_state.selected_lead = None
        st.rerun()

    # Header section
    score = lead.get("score", 0)
    company_name = lead.get("company_name", "Unknown Company")

    # Score badge color based on value
    if score >= 80:
        score_color = "#22C55E"  # green
    elif score >= 60:
        score_color = "#F59E0B"  # amber
    else:
        score_color = "#404040"  # gray

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="
            background: {score_color};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 2rem;
            font-weight: bold;
            font-family: 'JetBrains Mono', monospace;
            min-width: 80px;
            text-align: center;
        ">{score}</div>
        <h1 style="margin: 0; font-size: 2rem; color: #FAFAFA;">{company_name}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Region and type badges
    country = lead.get("country") or "Unknown"
    flag = get_flag(country)
    receives = lead.get("receives", False)
    pays = lead.get("pays", False)

    type_badges = []
    if receives:
        type_badges.append('<span style="background: rgba(34, 197, 94, 0.15); color: #4ADE80; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem; font-weight: 600;">RECEIVES</span>')
    if pays:
        type_badges.append('<span style="background: rgba(43, 127, 255, 0.15); color: #60A5FA; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem; font-weight: 600;">PAYS</span>')

    st.markdown(f"""
    <div style="display: flex; gap: 0.5rem; margin-bottom: 2rem; align-items: center;">
        <span style="background: rgba(255, 107, 64, 0.1); color: #FF8A66; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem; font-weight: 500;">
            {flag} {country}
        </span>
        {' '.join(type_badges)}
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    total_volume = lead.get("total_volume_usd", 0)
    transactions = lead.get("total_transactions", 0)
    client_count = lead.get("client_count", 0)
    currencies = lead.get("currencies", [])
    if isinstance(currencies, str):
        currencies = [currencies]
    currency_list = ", ".join(currencies[:5]) if currencies else "N/A"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Volume", format_volume(total_volume))

    with col2:
        st.metric("Transactions", f"{transactions:,}")

    with col3:
        st.metric("Client Network", f"{client_count}")

    with col4:
        st.metric("Currencies", currency_list)

    st.divider()

    # Two column layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # Pitch Points section
        st.subheader("💡 Pitch Points")

        # Network connection strength
        if client_count >= 2:
            st.success(f"**Strong Network Connection:** Already transacting with {client_count} of your clients. With Airwallex Pay, settlements would be T+1 instead of T+3.")
        elif client_count == 1:
            st.info(f"**Existing Connection:** Currently transacting with 1 of your clients — opportunity to expand relationship.")

        # Multi-currency opportunity
        if len(currencies) >= 2:
            st.info(f"**Multi-Currency Opportunity:** Active in {len(currencies)} currencies ({currency_list}). Could benefit from competitive FX rates and local collection accounts.")

        # Dual flow opportunity
        if receives and pays:
            st.warning("**Dual Flow Opportunity:** Both receives from and pays to your clients — strong candidate for full Airwallex suite.")

        st.divider()

        # Client Connections section
        st.subheader("📋 Client Connections")
        st.caption("Your clients who transact with this company")
        st.info("Client connection details require full transaction data enrichment.")

    with right_col:
        # Actions sidebar
        st.subheader("Actions")

        if st.button("📧 Draft Outreach Email", use_container_width=True, type="primary"):
            st.info("Email drafting feature coming in V2")

        if st.button("📋 Copy Pitch Points", use_container_width=True):
            pitch = f"""
Lead: {company_name}
Score: {score}/100
Volume: {format_volume(total_volume)}
Client connections: {client_count}
Currencies: {currency_list}
Type: {'Receives & Pays' if receives and pays else 'Receives' if receives else 'Pays' if pays else 'N/A'}
            """.strip()
            st.code(pitch)

        if st.button("🔍 Search Web for Info", use_container_width=True):
            search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}"
            st.markdown(f"[Open Google Search]({search_url})")

        st.divider()

        st.caption("QUICK STATS")
        st.markdown(f"**Lead Score:** {score} / 100")
        latest_month = lead.get("latest_month")
        if latest_month:
            st.markdown(f"**Data Freshness:** {str(latest_month)[:10]}")
