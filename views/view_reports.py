"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_reports.py
Description: Reports & Data Management View. Handles CSV export, external CSV
             import, instant database backups, demo dataset seeder, and safe reset.
================================================================================
"""

import streamlit as st
import os
import csv
from datetime import datetime
from config import BACKUPS_DIR, COLORS
from modules.data_manager import (
    export_transactions_csv,
    backup_data,
    clear_all_data,
    add_transaction,
    load_transactions,
    load_budget
)
from modules.sample_data import load_sample_dataset, has_sample_dataset, remove_user_sample_dataset
from modules.calc_engine import format_inr, calculate_total_income, calculate_total_expenses


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Reports & Data Management</h1>
        <div class="hero-subtitle">Export your financial ledger, create local backups, import external data, or reset storage.</div>
    </div>
    """, unsafe_allow_html=True)

    transactions = load_transactions()
    budget = load_budget()

    # --- TOP DATA SUMMARY CARD ---
    total_inc = calculate_total_income(transactions)
    total_exp = calculate_total_expenses(transactions)

    st.markdown(f"""
    <div class="content-card">
        <h3 style="margin-top:0; font-size:1.15rem; color:#FFFFFF;">📦 Database Summary & Health</h3>
        <div style="display:flex; gap: 2rem; flex-wrap:wrap; margin-top: 0.75rem;">
            <div>Total Transactions: <strong>{len(transactions)} records</strong></div>
            <div>Cumulative Income: <strong style="color:#10B981;">{format_inr(total_inc)}</strong></div>
            <div>Cumulative Expenses: <strong style="color:#EF4444;">{format_inr(total_exp)}</strong></div>
            <div>Configured Budget Months: <strong>{len(budget)} months</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SECTION 1: SAMPLE DEMO DATA SEEDER ---
    st.subheader("1. Sample / Demo Dataset Management")
    st.caption("Populate your isolated account with a curated, realistic dataset formatted in Indian Rupees (₹) for demonstration and evaluation.")

    demo_count = has_sample_dataset()
    if demo_count > 0:
        st.info(f"💡 **Demo Dataset Active:** You currently have **{demo_count} sample transactions** loaded under your account.")
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            if st.button("🔄 Reload / Replace Demo Dataset", key="btn_reload_demo", type="primary", use_container_width=True):
                res = load_sample_dataset(replace_existing=True)
                st.success(
                    f"✅ Demo data reloaded! Added {res['transactions_loaded']} transactions "
                    f"and set monthly budget to {format_inr(res['total_budget'])}."
                )
                st.rerun()
        with col_d2:
            if st.button("🗑️ Remove Only My Demo Records", key="btn_remove_demo", type="secondary", use_container_width=True):
                res = remove_user_sample_dataset()
                st.success(f"✅ Removed {res['deleted']} sample demo transactions. Genuine transactions preserved.")
                st.rerun()
    else:
        col_d1, _ = st.columns([1, 1])
        with col_d1:
            if st.button("🚀 Load Sample Demo Data (INR ₹)", key="btn_load_demo", type="primary", use_container_width=True):
                res = load_sample_dataset(replace_existing=True)
                st.success(
                    f"✅ Demo data loaded! Added {res['transactions_loaded']} transactions "
                    f"and set monthly budget to {format_inr(res['total_budget'])}."
                )
                st.rerun()

    st.markdown("---")

    # --- SECTION 2: EXPORT & BACKUPS ---
    st.subheader("2. CSV Export & Backup Snapshots")
    c_ex1, c_ex2 = st.columns(2)

    with c_ex1:
        st.write("**Download Complete Transaction Ledger**")
        csv_str = export_transactions_csv()
        st.download_button(
            label="📥 Download Transactions (CSV)",
            data=csv_str,
            file_name=f"spendwise_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with c_ex2:
        st.write("**Create Local Timestamped Backup Snapshot**")
        if st.button("💾 Create Backup Snapshot Now", key="btn_create_backup_reports", use_container_width=True):
            res = backup_data()
            if res.get("success"):
                st.success(f"Snapshot created successfully: `{res['timestamp']}`")
            else:
                st.error(f"Backup failed: {res.get('error')}")

    # List recent backup files
    if os.path.exists(BACKUPS_DIR):
        backup_files = sorted(os.listdir(BACKUPS_DIR), reverse=True)
        if backup_files:
            with st.expander(f"📦 Stored Backup Files ({len(backup_files)} files found)", expanded=False):
                for b in backup_files[:8]:
                    st.text(f"• {b}")

    st.markdown("---")

    # --- SECTION 3: IMPORT EXTERNAL TRANSACTIONS ---
    st.subheader("3. Import External CSV Transactions")
    st.caption("Upload a standard CSV file with headers: date, type, category, amount, payment_mode, description")

    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded is not None:
        try:
            content = uploaded.getvalue().decode("utf-8").splitlines()
            reader = csv.DictReader(content)
            imported_count = 0
            for row in reader:
                if "amount" in row and "type" in row and "category" in row:
                    try:
                        amt = float(row["amount"])
                        if amt > 0:
                            add_transaction({
                                "date": row.get("date", datetime.now().strftime("%Y-%m-%d")),
                                "type": row.get("type", "Expense"),
                                "category": row.get("category", "Others"),
                                "amount": amt,
                                "payment_mode": row.get("payment_mode", "UPI"),
                                "description": row.get("description", "Imported Entry")
                            })
                            imported_count += 1
                    except (ValueError, TypeError):
                        continue
            st.success(f"✅ Successfully imported {imported_count} transactions from uploaded CSV.")
            st.rerun()
        except Exception as error:
            st.error(f"Failed to process CSV file: {error}")

    st.markdown("---")

    # --- SECTION 4: RESET / CLEAR ALL DATA ---
    st.subheader("4. Danger Zone: Reset Database")
    st.caption("Permanently clears all stored transactions and resets budgets back to an empty state. An automated backup is created first.")

    col_rst1, _ = st.columns([1, 2])
    with col_rst1:
        if st.button("🗑️ Reset All Data to Clean Empty State", key="btn_reset_all_data_reports", type="secondary", use_container_width=True):
            if clear_all_data():
                st.warning("All records wiped. Database restored to clean default empty state.")
                st.rerun()
            else:
                st.error("Failed to reset database.")
