import streamlit as st
import pandas as pd
from data_generator import generate_data
from reconciliation import reconcile

st.set_page_config(page_title="Reconciliation Dashboard", layout="wide")

st.title("💳 Payment Reconciliation Dashboard")

st.markdown("Compare Platform Transactions with Bank Settlements and detect mismatches.")

# Generate data
platform_df, bank_df = generate_data()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Platform Data")
    st.dataframe(platform_df, use_container_width=True)

with col2:
    st.subheader("🏦 Bank Data")
    st.dataframe(bank_df, use_container_width=True)

# Run reconciliation
report = reconcile(platform_df, bank_df)

st.divider()

st.header("⚠️ Reconciliation Report")

# Metrics row
m1, m2, m3, m4 = st.columns(4)

m1.metric("Missing in Bank", len(report["missing_in_bank"]))
m2.metric("Duplicates", len(report["duplicates"]))
m3.metric("Invalid Refunds", len(report["invalid_refunds"]))
m4.metric("Amount Mismatches", len(report["amount_mismatch"]))

st.divider()

# Detailed Issues

st.subheader("🔍 Detailed Issues")

# Missing in Bank
if report["missing_in_bank"]:
    st.error(f"Missing in Bank: {report['missing_in_bank']}")

# Missing in Platform
if report["missing_in_platform"]:
    st.warning(f"Missing in Platform: {report['missing_in_platform']}")

# Duplicates
if report["duplicates"]:
    st.error(f"Duplicate Transactions: {report['duplicates']}")

# Invalid Refunds
if report["invalid_refunds"]:
    st.error(f"Invalid Refunds: {report['invalid_refunds']}")

# Amount mismatches
if report["amount_mismatch"]:
    st.warning("Amount Mismatches:")
    mismatch_df = pd.DataFrame(report["amount_mismatch"], columns=["txn_id", "platform_amt", "bank_amt"])
    st.dataframe(mismatch_df)

# Totals
st.divider()
st.subheader("💰 Total Comparison")

colA, colB = st.columns(2)

with colA:
    st.success(f"Platform Total: ₹{report['total_platform']}")

with colB:
    st.info(f"Bank Total: ₹{report['total_bank']}")

# Highlight mismatch
if report["total_platform"] != report["total_bank"]:
    st.error("⚠️ Totals do NOT match! Reconciliation failed.")
else:
    st.success("✅ Totals match! Reconciliation successful.")

# Footer
st.divider()
st.caption("Built for Payment Reconciliation Assignment 🚀")