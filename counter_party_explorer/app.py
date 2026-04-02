"""Main Streamlit application entry point for Counter-Party Lead Explorer."""

import streamlit as st
import pandas as pd

from ui.dashboard import render_dashboard
from ui.lead_detail import render_lead_detail
from ui.upload import render_upload
from ui.styles import GLOBAL_CSS


def main():
    """Main application function with routing and navigation."""
    # Page configuration
    st.set_page_config(
        page_title="Counter-Party Lead Explorer",
        page_icon="🎯",
        layout="wide"
    )

    # Apply global styles
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Initialize session state
    if "view" not in st.session_state:
        st.session_state.view = "upload"
    if "leads_df" not in st.session_state:
        st.session_state.leads_df = pd.DataFrame()
    if "selected_lead" not in st.session_state:
        st.session_state.selected_lead = None

    # Sidebar navigation
    with st.sidebar:
        st.title("🎯 Lead Explorer")
        st.divider()

        # Navigation buttons
        if st.button("◉ Top Leads", use_container_width=True):
            st.session_state.view = "dashboard"
            st.rerun()

        if st.button("↑ Upload Data", use_container_width=True):
            st.session_state.view = "upload"
            st.rerun()

        st.divider()

        # Data status
        st.subheader("Data Status")
        lead_count = len(st.session_state.leads_df)
        if lead_count > 0:
            st.success(f"✓ {lead_count} leads loaded")
        else:
            st.info("No data loaded")

    # Main content routing
    if st.session_state.view == "upload":
        render_upload()
    elif st.session_state.view == "detail" and st.session_state.selected_lead is not None:
        render_lead_detail(st.session_state.selected_lead, st.session_state.leads_df)
    elif st.session_state.view == "dashboard":
        if len(st.session_state.leads_df) > 0:
            render_dashboard(st.session_state.leads_df)
        else:
            st.warning("⚠️ No data loaded. Please upload data first.")
            if st.button("Go to Upload"):
                st.session_state.view = "upload"
                st.rerun()


if __name__ == "__main__":
    main()
