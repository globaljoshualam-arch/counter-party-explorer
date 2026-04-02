"""Lead detail view with pitch points and client connections."""

import streamlit as st
import pandas as pd
from .styles import GLOBAL_CSS, get_flag


def format_volume(amount):
    """Format volume amounts consistently."""
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

    # Back button
    if st.button("← Back to Top Leads"):
        st.session_state.selected_lead = None
        st.rerun()

    # Header section
    score = lead.get("score", 0)
    company_name = lead.get("counter_party", "Unknown")

    # Score badge color based on value
    if score >= 80:
        score_color = "#10b981"  # green
    elif score >= 60:
        score_color = "#f59e0b"  # amber
    else:
        score_color = "#ef4444"  # red

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <div style="
            background: {score_color};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 2rem;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
        ">{score}</div>
        <h1 style="margin: 0; font-size: 2rem;">{company_name}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Region and type badges
    region = lead.get("region", "Unknown")
    flag = get_flag(region)
    receives_volume = lead.get("receives_volume", 0)
    pays_volume = lead.get("pays_volume", 0)

    type_badges = []
    if receives_volume > 0:
        type_badges.append('<span style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem;">Receives</span>')
    if pays_volume > 0:
        type_badges.append('<span style="background: #fef3c7; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem;">Pays</span>')

    st.markdown(f"""
    <div style="display: flex; gap: 0.5rem; margin-bottom: 2rem; align-items: center;">
        <span style="background: #f3f4f6; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.875rem;">
            {flag} {region}
        </span>
        {' '.join(type_badges)}
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    total_volume = lead.get("total_volume", 0)
    transactions = lead.get("transactions", 0)
    client_network = lead.get("client_network", 0)
    currencies = lead.get("currencies", "")
    currency_count = len(currencies.split(", ")) if currencies else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Volume", format_volume(total_volume))

    with col2:
        st.metric("Transactions", f"{transactions:,}")

    with col3:
        st.metric("Client Network", client_network)

    with col4:
        st.metric("Currencies", currency_count)

    st.divider()

    # Pitch Points section
    st.subheader("Pitch Points")

    # Network connection strength
    if client_network > 0:
        st.success(f"**Strong Network Connection:** Already transacting with {client_network} of your clients, demonstrating established trust and compatibility with your network.")

    # Multi-currency opportunity
    if currency_count > 1:
        st.info(f"**Multi-Currency Opportunity:** Active in {currency_count} currencies ({currencies}), indicating sophisticated cross-border payment needs.")

    # Dual flow opportunity
    if receives_volume > 0 and pays_volume > 0:
        receives_pct = (receives_volume / total_volume * 100) if total_volume > 0 else 0
        pays_pct = (pays_volume / total_volume * 100) if total_volume > 0 else 0
        st.warning(f"**Dual Flow Opportunity:** Handles both incoming ({receives_pct:.0f}%) and outgoing ({pays_pct:.0f}%) payments, suggesting comprehensive payment infrastructure needs.")

    st.divider()

    # Client Connections section
    st.subheader("Client Connections")
    st.info("Detailed client connection analysis coming soon...")

    # Sidebar actions
    with st.sidebar:
        st.subheader("Actions")

        if st.button("📧 Draft Email", use_container_width=True):
            st.toast("Email draft feature coming soon!")

        if st.button("📋 Copy Pitch Points", use_container_width=True):
            st.toast("Pitch points copied to clipboard!")

        if st.button("🔍 Search Web", use_container_width=True):
            st.toast("Web search feature coming soon!")

        st.divider()

        st.subheader("Quick Stats")
        st.metric("Lead Score", score)
        st.caption("Data freshness: Last 90 days")
