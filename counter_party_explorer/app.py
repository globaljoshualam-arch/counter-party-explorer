"""Main Streamlit application entry point for Counter-Party Lead Explorer."""

import sys
from pathlib import Path

# Add parent directory to path for imports to work
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd

from counter_party_explorer.ui.dashboard import render_dashboard
from counter_party_explorer.ui.lead_detail import render_lead_detail
from counter_party_explorer.ui.upload import render_upload
from counter_party_explorer.ui.styles import GLOBAL_CSS
from counter_party_explorer.data.processor import process_data

# Data file paths
REPO_DATA_DIR = Path(__file__).parent.parent / "data"
PAYMENT_FILENAME = "Trade_Lead_Gen_from_Payment.csv"
REMITTER_FILENAME = "Trade_Lead_Gen_from_Remitter.csv"


def check_password():
    """Returns True if the user has entered the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        entered = st.session_state.get("password", "")
        try:
            correct = st.secrets.get("auth", {}).get("password", "")
        except Exception:
            correct = ""
        if entered == correct:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 60vh;">
            <div style="background: #171717; border: 1px solid #262626; border-radius: 16px; padding: 48px; max-width: 400px; width: 100%; text-align: center;">
                <div style="
                    width: 64px;
                    height: 64px;
                    background: linear-gradient(135deg, #FF6B40, #FF8A66);
                    border-radius: 16px;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 24px;
                    color: white;
                    margin-bottom: 16px;
                ">CP</div>
                <h2 style="color: #FAFAFA; margin: 0 0 8px 0;">Counter-Party Lead Explorer</h2>
                <p style="color: #737373;">Enter password to continue</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Enter password..."
        )
        return False

    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Enter password..."
        )
        st.error("Incorrect password. Please try again.")
        return False

    return True


@st.cache_data(ttl=3600, show_spinner=False)
def load_preloaded_data():
    """Load pre-processed data from CSV file. Cached for 1 hour."""
    import json
    csv_path = REPO_DATA_DIR / "leads_processed.csv"

    try:
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Parse JSON columns back to Python objects
            df['client_details'] = df['client_details'].apply(json.loads)
            df['currencies'] = df['currencies'].apply(json.loads)
            return df
    except Exception as e:
        st.error(f"Error loading data: {e}")

    return pd.DataFrame()


def main():
    """Main application function with routing and navigation."""
    st.set_page_config(
        page_title="Counter-Party Lead Explorer",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Check password (skip if secrets not configured)
    try:
        has_auth = hasattr(st, 'secrets') and "auth" in st.secrets and "password" in st.secrets["auth"]
    except Exception:
        has_auth = False

    if has_auth and not check_password():
        st.stop()

    # Initialize session state
    if "view" not in st.session_state:
        st.session_state.view = "dashboard"
    if "selected_lead" not in st.session_state:
        st.session_state.selected_lead = None

    # Load data with spinner (only on first load)
    if "leads_df" not in st.session_state:
        with st.spinner("Loading leads data... This may take a moment."):
            st.session_state.leads_df = load_preloaded_data()

    # Sidebar
    with st.sidebar:
        st.markdown('''
        <div style="display: flex; align-items: center; gap: 12px; padding: 0 8px; margin-bottom: 36px;">
            <div style="
                width: 36px;
                height: 36px;
                background: linear-gradient(135deg, #FF6B40, #FF8A66);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 15px;
                color: white;
            ">CP</div>
            <span style="font-weight: 600; font-size: 16px; color: #F5F5F5;">Lead Explorer</span>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #737373; padding: 0 12px; margin-bottom: 10px;">Discovery</div>
        ''', unsafe_allow_html=True)

        if st.button("◉ Top Leads", use_container_width=True, key="nav_leads"):
            st.session_state.view = "dashboard"
            st.rerun()

        st.markdown('''
        <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #737373; padding: 0 12px; margin: 20px 0 10px 0;">Data</div>
        ''', unsafe_allow_html=True)

        if st.button("↑ Upload Data", use_container_width=True, key="nav_upload"):
            st.session_state.view = "upload"
            st.rerun()

        if st.button("↻ Refresh Data", use_container_width=True, key="nav_refresh"):
            load_preloaded_data.clear()
            st.session_state.leads_df = load_preloaded_data()
            st.session_state.view = "dashboard"
            st.rerun()

        st.markdown('<div style="height: 1px; background: #262626; margin: 24px 0;"></div>', unsafe_allow_html=True)

        st.markdown('''
        <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #737373; padding: 0 12px; margin-bottom: 10px;">Status</div>
        ''', unsafe_allow_html=True)

        lead_count = len(st.session_state.leads_df)
        if lead_count > 0:
            high_potential = len(st.session_state.leads_df[st.session_state.leads_df["score"] >= 80])
            st.markdown(f'''
            <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 14px; margin: 0 4px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 600; color: #4ADE80;">{lead_count:,}</div>
                <div style="font-size: 13px; color: #737373; margin-top: 2px;">leads loaded</div>
                <div style="font-size: 12px; color: #FF8A66; margin-top: 8px;">{high_potential:,} high potential</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div style="background: #262626; border-radius: 10px; padding: 14px; margin: 0 4px;">
                <div style="font-size: 14px; color: #737373;">No data loaded</div>
                <div style="font-size: 12px; color: #525252; margin-top: 4px;">Upload CSV to start</div>
            </div>
            ''', unsafe_allow_html=True)

    # Main content routing
    if st.session_state.view == "upload":
        render_upload()
    elif st.session_state.view == "detail" and st.session_state.selected_lead is not None:
        render_lead_detail(st.session_state.selected_lead, st.session_state.leads_df)
    elif st.session_state.view == "dashboard":
        if len(st.session_state.leads_df) > 0:
            render_dashboard(st.session_state.leads_df)
        else:
            st.markdown('''
            <div style="text-align: center; padding: 80px 20px;">
                <div style="font-size: 48px; margin-bottom: 16px;">📤</div>
                <h2 style="color: #FAFAFA; margin-bottom: 8px;">No Data Loaded</h2>
                <p style="color: #737373; margin-bottom: 24px;">Upload your Payment and Remitter CSV files to get started.</p>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("Go to Upload", type="primary"):
                st.session_state.view = "upload"
                st.rerun()


if __name__ == "__main__":
    main()
