"""Lead detail view with pitch points and metrics."""

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


def render_lead_detail(lead: dict, all_data: pd.DataFrame = None):
    """Render detailed view for a single lead."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(render_logo(), unsafe_allow_html=True)

    # Back button
    if st.button("← Back to Top Leads"):
        st.session_state.view = "dashboard"
        st.session_state.selected_lead = None
        st.rerun()

    # Extract data
    score = int(lead.get("score", 0))
    company_name = lead.get("company_name", "Unknown Company")
    country = lead.get("country")
    if not country or not isinstance(country, str):
        country = "Unknown"
    flag = get_flag(country)
    receives = lead.get("receives", False)
    pays = lead.get("pays", False)
    total_volume = lead.get("total_volume_usd", 0)
    transactions = lead.get("total_transactions", 0)
    client_count = lead.get("client_count", 0)
    currencies = lead.get("currencies", [])
    if isinstance(currencies, str):
        currencies = [currencies] if currencies else []
    currency_list = ", ".join(currencies[:5]) if currencies else "N/A"
    latest_month = lead.get("latest_month")

    # Score indicator
    if score >= 80:
        score_indicator = "🟢"
        score_label = "High Potential"
    elif score >= 60:
        score_indicator = "🟡"
        score_label = "Medium Potential"
    else:
        score_indicator = "⚪"
        score_label = "Low Potential"

    # Header
    st.markdown(f"# {company_name}")

    # Info row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### {score_indicator} Score: {score}/100")
        st.caption(score_label)
    with col2:
        st.markdown(f"### {flag} {country}")
        type_badges = []
        if receives:
            type_badges.append("📥 Receives")
        if pays:
            type_badges.append("📤 Pays")
        st.caption(" | ".join(type_badges) if type_badges else "No payment type")
    with col3:
        st.markdown(f"### {client_count} Clients")
        st.caption("Airwallex connections")

    st.divider()

    # Key Metrics
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Volume", format_volume(total_volume), help="Monthly average")
    with col2:
        st.metric("Transactions", f"{transactions:,}", help="Per month")
    with col3:
        st.metric("Client Network", f"{client_count}", help="Airwallex clients")
    with col4:
        st.metric("Currencies", f"{len(currencies)}", help=currency_list)

    st.divider()

    # Two column layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # Pitch Points
        st.subheader("💡 Pitch Points")
        st.caption("Key talking points for outreach")

        pitch_points = []

        # Network connection pitch
        if client_count >= 2:
            pitch_points.append({
                "icon": "🔗",
                "title": "Strong network connection",
                "text": f"Already transacting with {client_count} of our clients. With Airwallex Pay, settlements would be T+1 instead of T+3."
            })
        elif client_count == 1:
            pitch_points.append({
                "icon": "🔗",
                "title": "Existing connection",
                "text": "Currently transacting with 1 of our clients — opportunity to expand relationship."
            })

        # Multi-currency pitch
        if len(currencies) >= 2:
            pitch_points.append({
                "icon": "💱",
                "title": "Multi-currency opportunity",
                "text": f"Active in {len(currencies)} currencies ({currency_list}). Could benefit from competitive FX rates and local collection accounts."
            })

        # Dual flow pitch
        if receives and pays:
            pitch_points.append({
                "icon": "↔️",
                "title": "Dual flow opportunity",
                "text": "Both receives from and pays to your clients — strong candidate for full Airwallex suite."
            })

        # Volume pitch
        if total_volume >= 500_000:
            pitch_points.append({
                "icon": "📈",
                "title": "High volume trader",
                "text": f"Processing {format_volume(total_volume)}/month through your network. Scale warrants dedicated payment infrastructure."
            })

        if pitch_points:
            for p in pitch_points:
                st.info(f"**{p['icon']} {p['title']}:** {p['text']}")
        else:
            st.caption("No specific pitch points available for this lead.")

        # Associated Clients section
        st.subheader("🏢 Associated Clients")
        st.caption("Airwallex clients transacting with this counterparty")

        client_details = lead.get("client_details", [])
        if client_details and len(client_details) > 0:
            # Header row
            header_cols = st.columns([3, 1.5, 1, 2])
            with header_cols[0]:
                st.markdown("**Client Name**")
            with header_cols[1]:
                st.markdown("**Volume**")
            with header_cols[2]:
                st.markdown("**Txns**")
            with header_cols[3]:
                st.markdown("**BD Manager**")

            st.divider()

            # Client rows
            for client in client_details:
                client_cols = st.columns([3, 1.5, 1, 2])
                with client_cols[0]:
                    st.markdown(f"{client.get('client_name', 'Unknown')}")
                with client_cols[1]:
                    st.markdown(f"**{format_volume(client.get('volume_usd', 0))}**")
                with client_cols[2]:
                    st.markdown(f"{client.get('transaction_count', 0):,}")
                with client_cols[3]:
                    bd = client.get('bd_manager')
                    st.markdown(f"{bd if bd else '—'}")
        else:
            st.caption("No client data available")

        st.divider()

        # Currency Activity - always show section
        st.subheader("💱 Currency Activity")
        st.caption("Active currency corridors")

        if currencies and len(currencies) > 0:
            # Display currencies in a grid
            num_cols = min(6, len(currencies))
            currency_cols = st.columns(num_cols)
            for i, ccy in enumerate(currencies[:6]):
                with currency_cols[i]:
                    st.markdown(f"**`{ccy}`**")

            if len(currencies) > 6:
                st.caption(f"+ {len(currencies) - 6} more currencies")
        else:
            st.caption("No currency data available")

    with right_col:
        # Actions panel
        st.subheader("⚡ Actions")

        if st.button("📧 Draft Outreach Email", use_container_width=True, type="primary"):
            st.info("Email drafting feature coming in V2")

        if st.button("📋 Copy Pitch Points", use_container_width=True):
            pitch_text = f"""
Lead: {company_name}
Score: {score}/100
Volume: {format_volume(total_volume)}
Client connections: {client_count}
Currencies: {currency_list}
Type: {'Receives & Pays' if receives and pays else 'Receives' if receives else 'Pays' if pays else 'N/A'}
            """.strip()
            st.code(pitch_text)

        if st.button("🔍 Search Web for Info", use_container_width=True):
            search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}"
            st.markdown(f"[Open Google Search]({search_url})")

        st.divider()

        # Quick stats
        st.caption("**Lead Score**")
        st.progress(score / 100)
        st.markdown(f"`{score} / 100`")

        st.caption("**Latest Activity**")
        st.markdown(f"`{str(latest_month)[:10] if latest_month else 'N/A'}`")
        st.caption("Last payment received from or paid to our clients")
