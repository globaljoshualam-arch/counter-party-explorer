"""Upload view for CSV file uploads with validation."""

import streamlit as st
import pandas as pd

from ..data.processor import process_data
from ..data.loader import validate_payment_schema, validate_remitter_schema
from .styles import GLOBAL_CSS


def render_upload():
    """Render the upload view with file uploaders and validation."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Back to dashboard button if data exists
    if "leads_df" in st.session_state and st.session_state.leads_df is not None:
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    # Title and caption
    st.title("Upload Data")
    st.caption("Upload your payment and remitter CSV files to identify potential leads")

    # Two columns for file uploads
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Payment Data")
        st.caption("Expected: payment_data.csv")
        payment_file = st.file_uploader(
            "Upload Payment CSV",
            type=["csv"],
            key="payment_uploader"
        )

        if payment_file is not None:
            try:
                payment_df = pd.read_csv(payment_file)
                validate_payment_schema(payment_df)
                st.session_state.payment_df = payment_df
                st.success(f"✓ Payment data loaded: {len(payment_df):,} rows")
            except Exception as e:
                st.error(f"✗ Payment data error: {str(e)}")
                st.session_state.payment_df = None

    with col2:
        st.subheader("Remitter Data")
        st.caption("Expected: remitter_data.csv")
        remitter_file = st.file_uploader(
            "Upload Remitter CSV",
            type=["csv"],
            key="remitter_uploader"
        )

        if remitter_file is not None:
            try:
                remitter_df = pd.read_csv(remitter_file)
                validate_remitter_schema(remitter_df)
                st.session_state.remitter_df = remitter_df
                st.success(f"✓ Remitter data loaded: {len(remitter_df):,} rows")
            except Exception as e:
                st.error(f"✗ Remitter data error: {str(e)}")
                st.session_state.remitter_df = None

    # Process data button
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Process Data", disabled=(
        "payment_df" not in st.session_state or
        "remitter_df" not in st.session_state or
        st.session_state.payment_df is None or
        st.session_state.remitter_df is None
    )):
        with st.spinner("Processing data..."):
            try:
                leads_df = process_data(
                    st.session_state.payment_df,
                    st.session_state.remitter_df
                )
                st.session_state.leads_df = leads_df
                st.success(f"✓ Successfully processed data! Found {len(leads_df):,} leads")

                if st.button("Go to Dashboard"):
                    st.session_state.current_page = "dashboard"
                    st.rerun()
            except Exception as e:
                st.error(f"✗ Processing error: {str(e)}")
