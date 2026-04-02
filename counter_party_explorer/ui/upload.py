"""Upload view for CSV file uploads with validation."""

import streamlit as st
import pandas as pd

from counter_party_explorer.data.processor import process_data
from counter_party_explorer.data.loader import validate_payment_schema, validate_remitter_schema
from counter_party_explorer.ui.styles import GLOBAL_CSS


def render_upload():
    """Render the upload view with file uploaders and validation."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Back to dashboard button if data exists
    if "leads_df" in st.session_state and len(st.session_state.leads_df) > 0:
        if st.button("← Back to Dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()

    # Title
    st.markdown('''
    <h1 style="color: #FAFAFA; font-size: 28px; font-weight: 700; margin-bottom: 8px;">Upload Data</h1>
    <p style="color: #737373; font-size: 15px; margin-bottom: 32px;">Upload your Payment and Remitter CSV files to identify potential leads</p>
    ''', unsafe_allow_html=True)

    # Two columns for file uploads
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div style="background: #171717; border: 1px solid #262626; border-radius: 14px; padding: 24px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 40px; height: 40px; background: rgba(43, 127, 255, 0.15); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">💸</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #F5F5F5;">Payment Data</div>
                    <div style="font-size: 13px; color: #737373;">Money leaving clients (to suppliers)</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        payment_file = st.file_uploader(
            "Trade_Lead_Gen_from_Payment.csv",
            type=["csv"],
            key="payment_uploader",
            label_visibility="collapsed"
        )

        if payment_file is not None:
            try:
                payment_df = pd.read_csv(payment_file)
                if validate_payment_schema(payment_df):
                    st.session_state.payment_df = payment_df
                    st.markdown(f'''
                    <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 14px; margin-top: 12px;">
                        <div style="color: #4ADE80; font-weight: 600;">✓ Valid payment file</div>
                        <div style="color: #737373; font-size: 13px; margin-top: 4px;">{len(payment_df):,} rows loaded</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("✗ Invalid schema - missing required columns")
                    st.session_state.payment_df = None
            except Exception as e:
                st.error(f"✗ Error reading file: {str(e)}")
                st.session_state.payment_df = None

    with col2:
        st.markdown('''
        <div style="background: #171717; border: 1px solid #262626; border-radius: 14px; padding: 24px; height: 100%;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 40px; height: 40px; background: rgba(34, 197, 94, 0.15); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">💰</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #F5F5F5;">Remitter Data</div>
                    <div style="font-size: 13px; color: #737373;">Money entering clients (from buyers)</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        remitter_file = st.file_uploader(
            "Trade_Lead_Gen_from_Remitter.csv",
            type=["csv"],
            key="remitter_uploader",
            label_visibility="collapsed"
        )

        if remitter_file is not None:
            try:
                remitter_df = pd.read_csv(remitter_file)
                if validate_remitter_schema(remitter_df):
                    st.session_state.remitter_df = remitter_df
                    st.markdown(f'''
                    <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 14px; margin-top: 12px;">
                        <div style="color: #4ADE80; font-weight: 600;">✓ Valid remitter file</div>
                        <div style="color: #737373; font-size: 13px; margin-top: 4px;">{len(remitter_df):,} rows loaded</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.error("✗ Invalid schema - missing required columns")
                    st.session_state.remitter_df = None
            except Exception as e:
                st.error(f"✗ Error reading file: {str(e)}")
                st.session_state.remitter_df = None

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    # Check if at least one file is uploaded
    has_payment = "payment_df" in st.session_state and st.session_state.payment_df is not None
    has_remitter = "remitter_df" in st.session_state and st.session_state.remitter_df is not None

    if has_payment or has_remitter:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process Data & Find Leads", type="primary", use_container_width=True):
                with st.spinner("Processing data..."):
                    try:
                        leads_df = process_data(
                            payment_df=st.session_state.get("payment_df"),
                            remitter_df=st.session_state.get("remitter_df"),
                        )
                        st.session_state.leads_df = leads_df

                        high_potential = len(leads_df[leads_df["score"] >= 80])

                        st.markdown(f'''
                        <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 14px; padding: 24px; text-align: center; margin-top: 24px;">
                            <div style="font-size: 48px; margin-bottom: 12px;">🎯</div>
                            <div style="font-size: 20px; font-weight: 600; color: #4ADE80; margin-bottom: 8px;">Processing Complete!</div>
                            <div style="color: #D4D4D4;">Found <strong style="color: #FAFAFA;">{len(leads_df):,}</strong> unique leads</div>
                            <div style="color: #FF8A66; margin-top: 4px;">{high_potential:,} high-potential (score 80+)</div>
                        </div>
                        ''', unsafe_allow_html=True)

                        st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

                        if st.button("View Dashboard →", type="primary", use_container_width=True):
                            st.session_state.view = "dashboard"
                            st.rerun()

                    except Exception as e:
                        st.error(f"✗ Processing error: {str(e)}")
    else:
        st.markdown('''
        <div style="background: #171717; border: 2px dashed #404040; border-radius: 14px; padding: 48px; text-align: center; margin-top: 16px;">
            <div style="font-size: 36px; margin-bottom: 12px;">📁</div>
            <div style="color: #A3A3A3; font-size: 15px;">Upload at least one CSV file to continue</div>
        </div>
        ''', unsafe_allow_html=True)
