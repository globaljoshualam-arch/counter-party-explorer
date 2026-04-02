"""Client detail view - shows counterparty leads for a specific Airwallex client."""

import streamlit as st
import pandas as pd

from counter_party_explorer.ui.styles import GLOBAL_CSS, get_flag, render_logo


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


def render_client_detail(client: dict):
    """Render detailed view for a single client with their counterparty leads."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(render_logo(), unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Top Clients"):
        st.session_state.view = "clients"
        st.session_state.selected_client = None
        st.rerun()

    # Extract data
    client_name = client.get("client_name", "Unknown Client")
    bd_manager = client.get("bd_manager") or "Not assigned"
    lead_count = client.get("lead_count", 0)
    high_potential_count = client.get("high_potential_count", 0)
    total_volume = client.get("total_volume_usd", 0)
    currencies = client.get("currencies", [])
    leads = client.get("leads", [])

    # Opportunity indicator
    if high_potential_count >= 5:
        opp_indicator = "🔥"
        opp_label = "Hot Opportunity"
    elif high_potential_count >= 2:
        opp_indicator = "🟢"
        opp_label = "High Opportunity"
    elif high_potential_count >= 1:
        opp_indicator = "🟡"
        opp_label = "Medium Opportunity"
    else:
        opp_indicator = "⚪"
        opp_label = "Low Opportunity"

    # Header
    st.markdown(f"# {client_name}")

    # Info row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### {opp_indicator} {high_potential_count} High-Potential Leads")
        st.caption(opp_label)
    with col2:
        st.markdown(f"### {lead_count} Total Leads")
        st.caption("Counterparty connections")
    with col3:
        st.markdown(f"### {bd_manager}")
        st.caption("BD Manager")

    st.divider()

    # Key Metrics
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Volume", format_volume(total_volume), help="With all counterparties")
    with col2:
        st.metric("Counterparties", f"{lead_count}", help="Unique leads")
    with col3:
        st.metric("High Potential", f"{high_potential_count}", help="Score 80+")
    with col4:
        currency_list = ", ".join(currencies[:5]) if currencies else "N/A"
        st.metric("Currencies", f"{len(currencies)}", help=currency_list)

    st.divider()

    # Two column layout
    left_col, right_col = st.columns([3, 1])

    with left_col:
        # Counterparty Leads section
        st.subheader("🎯 Counterparty Leads")
        st.caption("Potential referral opportunities for this client")

        if leads and len(leads) > 0:
            # Header row
            header_cols = st.columns([2.5, 1, 1, 1.2, 1.5, 1])
            with header_cols[0]:
                st.markdown("**Company**")
            with header_cols[1]:
                st.markdown("**Score**")
            with header_cols[2]:
                st.markdown("**Type**")
            with header_cols[3]:
                st.markdown("**Volume**")
            with header_cols[4]:
                st.markdown("**Currencies**")
            with header_cols[5]:
                st.markdown("**Country**")

            st.divider()

            # Lead rows
            for lead in leads:
                company_name = lead.get("company_name", "Unknown")
                score = int(lead.get("score", 0))
                volume = lead.get("volume_usd", 0)
                receives = lead.get("receives", False)
                pays = lead.get("pays", False)
                lead_currencies = lead.get("currencies", [])
                country = lead.get("country")

                # Score color
                if score >= 80:
                    score_display = f"🟢 {score}"
                elif score >= 60:
                    score_display = f"🟡 {score}"
                else:
                    score_display = f"⚪ {score}"

                # Type
                if receives and pays:
                    type_str = "↔️ Both"
                elif receives:
                    type_str = "📥 Recv"
                elif pays:
                    type_str = "📤 Pay"
                else:
                    type_str = "—"

                # Currency display
                currency_str = ", ".join(lead_currencies[:2])
                if len(lead_currencies) > 2:
                    currency_str += f" +{len(lead_currencies) - 2}"

                # Country with flag
                if country and isinstance(country, str):
                    flag = get_flag(country)
                    country_display = f"{flag} {country}"
                else:
                    country_display = "—"

                lead_cols = st.columns([2.5, 1, 1, 1.2, 1.5, 1])
                with lead_cols[0]:
                    st.markdown(f"**{company_name}**")
                with lead_cols[1]:
                    st.markdown(score_display)
                with lead_cols[2]:
                    st.markdown(type_str)
                with lead_cols[3]:
                    st.markdown(f"**{format_volume(volume)}**")
                with lead_cols[4]:
                    st.markdown(f"`{currency_str}`" if currency_str else "—")
                with lead_cols[5]:
                    st.markdown(country_display)

            st.divider()

            # Summary
            high_score_leads = [l for l in leads if l.get("score", 0) >= 80]
            if high_score_leads:
                st.success(f"**{len(high_score_leads)} high-potential leads** ready for outreach")

        else:
            st.caption("No lead data available")

    with right_col:
        # Actions panel
        st.subheader("⚡ Actions")

        if st.button("📧 Draft Client Email", use_container_width=True, type="primary"):
            st.info("Email drafting feature coming in V2")

        if st.button("📋 Copy Summary", use_container_width=True):
            # Build summary text
            high_leads = [l for l in leads if l.get("score", 0) >= 80]
            lead_names = ", ".join([l.get("company_name", "") for l in high_leads[:5]])

            summary_text = f"""
Client: {client_name}
BD Manager: {bd_manager}
Total Leads: {lead_count}
High-Potential Leads: {high_potential_count}
Total Volume: {format_volume(total_volume)}
Currencies: {', '.join(currencies[:5])}

Top Leads: {lead_names}
            """.strip()
            st.code(summary_text)

        st.divider()

        # Quick stats
        st.caption("**Opportunity Level**")
        opp_pct = min(100, high_potential_count * 20)
        st.progress(opp_pct / 100)
        st.markdown(f"`{high_potential_count} high-potential`")

        st.divider()

        # Currency breakdown
        st.caption("**Active Currencies**")
        if currencies:
            for ccy in currencies[:6]:
                st.markdown(f"• `{ccy}`")
            if len(currencies) > 6:
                st.caption(f"+ {len(currencies) - 6} more")
        else:
            st.caption("No currency data")
