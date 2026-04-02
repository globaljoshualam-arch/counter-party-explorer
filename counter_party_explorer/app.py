"""Main Streamlit application entry point for Counter-Party Lead Explorer."""

import streamlit as st
import pandas as pd
import json
import pathlib
import sys

# Page config must be first
st.set_page_config(
    page_title="Counter-Party Lead Explorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"  # Always start with sidebar visible
)

# Fix Python path for Streamlit Cloud - add repo root to allow package imports
repo_root = pathlib.Path(__file__).parent.parent.resolve()
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Now imports will work
from counter_party_explorer.ui.styles import GLOBAL_CSS
from counter_party_explorer.ui.dashboard import render_dashboard
from counter_party_explorer.ui.lead_detail import render_lead_detail
from counter_party_explorer.ui.clients_dashboard import render_clients_dashboard
from counter_party_explorer.ui.client_detail import render_client_detail


def get_data_dir():
    """Find the data directory robustly - works on both local and Streamlit Cloud."""
    # data/ in repo root (sibling to counter_party_explorer/)
    repo_data = repo_root / "data"
    if repo_data.exists():
        return repo_data

    # Fallback: Check Streamlit Cloud path
    cloud_path = pathlib.Path("/mount/src/counter-party-explorer/data")
    if cloud_path.exists():
        return cloud_path

    return repo_data


DATA_DIR = get_data_dir()


@st.cache_data
def load_data():
    """Load pre-processed leads data."""
    csv_path = DATA_DIR / "leads_processed.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df['client_details'] = df['client_details'].apply(json.loads)
        df['currencies'] = df['currencies'].apply(json.loads)
        return df
    return pd.DataFrame()


def check_password():
    """Simple password protection."""
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    try:
        correct_password = st.secrets["auth"]["password"]
    except Exception:
        # No password configured, allow access
        return True

    # Apply styling to login page too
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    st.markdown("# Counter-Party Lead Explorer")
    st.markdown("Please enter the password to continue.")

    password = st.text_input("Password", type="password", label_visibility="collapsed")
    if st.button("Login", type="primary"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False


# Main app
if not check_password():
    st.stop()

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = "dashboard"
if "selected_lead" not in st.session_state:
    st.session_state.selected_lead = None
if "selected_client" not in st.session_state:
    st.session_state.selected_client = None

# Load data
with st.spinner("Loading leads data..."):
    df = load_data()

if len(df) == 0:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.error("No data found. Please ensure data/leads_processed.csv exists.")
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")

    # Determine which button should appear "active"
    current_view = st.session_state.view

    if st.button("🎯 Top Leads", use_container_width=True,
                 type="primary" if current_view in ["dashboard", "detail"] else "secondary"):
        st.session_state.view = "dashboard"
        st.session_state.selected_lead = None
        st.session_state.selected_client = None
        # Clear cached clients data to refresh
        if "clients_df" in st.session_state:
            del st.session_state.clients_df
        st.rerun()

    if st.button("👥 Top Clients", use_container_width=True,
                 type="primary" if current_view in ["clients", "client_detail"] else "secondary"):
        st.session_state.view = "clients"
        st.session_state.selected_lead = None
        st.session_state.selected_client = None
        st.rerun()

    st.divider()

    # Data info
    st.caption(f"**{len(df):,}** leads loaded")

    # Unique clients count
    unique_clients = set()
    for details in df['client_details']:
        if isinstance(details, list):
            for c in details:
                if c.get('client_id'):
                    unique_clients.add(c['client_id'])
    st.caption(f"**{len(unique_clients):,}** unique clients")

# Route to appropriate view
if st.session_state.view == "detail" and st.session_state.selected_lead:
    render_lead_detail(st.session_state.selected_lead, df)
elif st.session_state.view == "client_detail" and st.session_state.selected_client:
    render_client_detail(st.session_state.selected_client)
elif st.session_state.view == "clients":
    render_clients_dashboard(df)
else:
    render_dashboard(df)
