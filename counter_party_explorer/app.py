"""Main Streamlit application entry point for Counter-Party Lead Explorer."""

import streamlit as st
import pandas as pd
import json
import pathlib

# Page config must be first
st.set_page_config(
    page_title="Counter-Party Lead Explorer",
    page_icon="🎯",
    layout="wide"
)

# Import UI components
from counter_party_explorer.ui.styles import GLOBAL_CSS
from counter_party_explorer.ui.dashboard import render_dashboard
from counter_party_explorer.ui.lead_detail import render_lead_detail


def get_data_dir():
    """Find the data directory robustly - works on both local and Streamlit Cloud."""
    current_file = pathlib.Path(__file__).resolve()

    # Option 1: data/ in repo root (sibling to counter_party_explorer/)
    repo_data = current_file.parent.parent / "data"
    if repo_data.exists():
        return repo_data

    # Option 2: Check if we're on Streamlit Cloud
    cloud_path = pathlib.Path("/mount/src/counter-party-explorer/data")
    if cloud_path.exists():
        return cloud_path

    # Option 3: Current working directory
    cwd_data = pathlib.Path.cwd() / "data"
    if cwd_data.exists():
        return cwd_data

    return repo_data  # Return default even if not found


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

# Load data
with st.spinner("Loading leads data..."):
    df = load_data()

if len(df) == 0:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.error(f"No data found. Please ensure data/leads_processed.csv exists.")
    st.stop()

# Route to appropriate view
if st.session_state.view == "detail" and st.session_state.selected_lead:
    render_lead_detail(st.session_state.selected_lead, df)
else:
    render_dashboard(df)
