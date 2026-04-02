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
    if "leads_df" in st.session_state and len(st.session_state.leads_df) > 0:
        if st.button("← Back to Dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()

    # Title and caption
    st.title("Upload Data")
    st.caption("Upload your Payment and Remitter CSV files to identify potential leads")

    st.divider()

    # Two columns for file uploads
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💸 Payment Data")
        st.caption("Trade_Lead_Gen_from_Payment.csv")
        st.caption("Money leaving clients (to suppliers)")
        payment_file = st.file_uploader(
            "Upload Payment CSV",
            type=["csv"],
            key="payment_uploader",
            label_visibility="collapsed"
        )

        if payment_file is not None:
            try:
                payment_df = pd.read_csv(payment_file)
                if validate_payment_schema(payment_df):
                    st.session_state.payment_df = payment_df
                    st.success(f"✓ Valid payment file ({len(payment_df):,} rows)")
                else:
                    st.error("✗ Invalid schema - missing required columns")
                    st.session_state.payment_df = None
            except Exception as e:
                st.error(f"✗ Error reading file: {str(e)}")
                st.session_state.payment_df = None

    with col2:
        st.subheader("💰 Remitter Data")
        st.caption("Trade_Lead_Gen_from_Remitter.csv")
        st.caption("Money entering clients (from buyers)")
        remitter_file = st.file_uploader(
            "Upload Remitter CSV",
            type=["csv"],
            key="remitter_uploader",
            label_visibility="collapsed"
        )

        if remitter_file is not None:
            try:
                remitter_df = pd.read_csv(remitter_file)
                if validate_remitter_schema(remitter_df):
                    st.session_state.remitter_df = remitter_df
                    st.success(f"✓ Valid remitter file ({len(remitter_df):,} rows)")
                else:
                    st.error("✗ Invalid schema - missing required columns")
                    st.session_state.remitter_df = None
            except Exception as e:
                st.error(f"✗ Error reading file: {str(e)}")
                st.session_state.remitter_df = None

    st.divider()

    # Check if at least one file is uploaded
    has_payment = "payment_df" in st.session_state and st.session_state.payment_df is not None
    has_remitter = "remitter_df" in st.session_state and st.session_state.remitter_df is not None

    if has_payment or has_remitter:
        if st.button("🚀 Process Data", type="primary", use_container_width=True):
            with st.spinner("Processing data..."):
                try:
                    leads_df = process_data(
                        payment_df=st.session_state.get("payment_df"),
                        remitter_df=st.session_state.get("remitter_df"),
                    )
                    st.session_state.leads_df = leads_df

                    high_potential = len(leads_df[leads_df["score"] >= 80])
                    st.success(f"✓ Processed {len(leads_df):,} unique leads ({high_potential:,} high-potential)")

                    if st.button("View Dashboard →", type="primary"):
                        st.session_state.view = "dashboard"
                        st.rerun()

                except Exception as e:
                    st.error(f"✗ Processing error: {str(e)}")
    else:
        st.info("📁 Upload at least one CSV file to continue.")
