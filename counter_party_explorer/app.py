"""Main Streamlit application entry point for Counter-Party Lead Explorer."""

import streamlit as st
import pandas as pd
import json
import os

# Page config must be first
st.set_page_config(
    page_title="Counter-Party Lead Explorer",
    page_icon="🎯",
    layout="wide"
)

# Find data directory - works on both local and Streamlit Cloud
# On Cloud, the repo is mounted at /mount/src/counter-party-explorer/
def get_data_dir():
    """Find the data directory robustly."""
    # Try relative to this file first
    import pathlib
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

# Simple password check
def check_password():
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    try:
        correct_password = st.secrets["auth"]["password"]
    except Exception:
        # No password configured, allow access
        return True

    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False

# Main app
if not check_password():
    st.stop()

st.title("Counter-Party Lead Explorer")

# Debug info (can remove later)
st.caption(f"Data dir: {DATA_DIR}")

# Load data
with st.spinner("Loading data..."):
    df = load_data()

if len(df) == 0:
    st.error(f"No data found. Looked in: {DATA_DIR / 'leads_processed.csv'}")
    st.stop()

st.success(f"Loaded {len(df):,} leads")

# Filters
col1, col2 = st.columns(2)
with col1:
    search = st.text_input("Search company")
with col2:
    min_score = st.slider("Min Score", 0, 100, 0)

# Filter data
filtered = df.copy()
if search:
    filtered = filtered[filtered['company_name'].str.contains(search, case=False, na=False)]
if min_score > 0:
    filtered = filtered[filtered['score'] >= min_score]

st.write(f"Showing {len(filtered):,} leads")

# Display table
st.dataframe(
    filtered[['company_name', 'country', 'score', 'total_volume_usd', 'client_count']].head(50),
    use_container_width=True
)
