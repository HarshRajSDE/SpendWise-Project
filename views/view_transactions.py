"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_transactions.py
Description: Transaction Ledger & Management View. Enables searching, filtering,
             inspecting, editing, and deleting stored transactions.
================================================================================
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_manager import load_transactions, delete_transaction, update_transaction
from modules.calc_engine import format_inr, get_available_months
from config import EXPENSE_CATEGORIES, INCOME_CATEGORIES, PAYMENT_MODES, COLORS


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Transaction History</h1>
        <div class="hero-subtitle">Inspect, search, filter, edit, or delete stored financial transaction records.</div>
    </div>
    """, unsafe_allow_html=True)

    transactions = load_transactions()

    if not transactions:
        st.markdown("""
        <div class="empty-state-box">
            <div class="empty-state-icon">📋</div>
            <div class="empty-state-title">No Transactions Recorded</div>
            <div class="empty-state-desc">
                Your transaction ledger is completely empty. Add entries from the
                <strong>'Add Transaction'</strong> tab or load sample data from Reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # --- FILTER BAR ---
    with st.expander("🔍 Search & Filter Controls", expanded=True):
        f1, f2, f3, f4 = st.columns(4)

        with f1:
            all_months = ["All Months"] + get_available_months(transactions)
            selected_month = st.selectbox("Month Filter", options=all_months)

        with f2:
            selected_type = st.selectbox("Type Filter", options=["All", "Expense", "Income"])

        with f3:
            all_cats = ["All Categories"] + sorted(list(set(EXPENSE_CATEGORIES + INCOME_CATEGORIES)))
            selected_cat = st.selectbox("Category Filter", options=all_cats)

        with f4:
            search_query = st.text_input("Search Keyword", placeholder="e.g., Grocery, GPay, Uber")

    # Apply filters
    filtered = []
    for t in transactions:
        if selected_month != "All Months" and not t.get("date", "").startswith(selected_month):
            continue
        if selected_type != "All" and t.get("type") != selected_type:
            continue
        if selected_cat != "All Categories" and t.get("category") != selected_cat:
            continue
        if search_query:
            q = search_query.lower()
            desc = str(t.get("description", "")).lower()
            cat = str(t.get("category", "")).lower()
            mode = str(t.get("payment_mode", "")).lower()
            if q not in desc and q not in cat and q not in mode:
                continue
        filtered.append(t)

    # Sort descending by date
    filtered.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Filtered Metrics
    f_income = sum(t["amount"] for t in filtered if t.get("type") == "Income")
    f_expense = sum(t["amount"] for t in filtered if t.get("type") == "Expense")
    f_net = f_income - f_expense

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Matching Transactions", len(filtered))
    m2.metric("Filtered Income", format_inr(f_income))
    m3.metric("Filtered Expenses", format_inr(f_expense))
    m4.metric("Filtered Net Cash Flow", format_inr(f_net))

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.warning("No transactions match the selected filter criteria.")
        return

    # Render Table
    table_rows = []
    for t in filtered:
        table_rows.append({
            "ID": t.get("id"),
            "Date": t.get("date"),
            "Type": t.get("type"),
            "Category": t.get("category"),
            "Amount": format_inr(t.get("amount", 0)),
            "Payment Mode": t.get("payment_mode"),
            "Description": t.get("description")
        })

    df_table = pd.DataFrame(table_rows)
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- EDIT & DELETE ACTIONS ---
    tab_edit, tab_delete = st.tabs(["✏️ Edit a Transaction", "🗑️ Delete a Transaction"])

    # 1. EDIT TRANSACTION
    with tab_edit:
        st.caption("Select a transaction ID to modify its amount, category, date, or remarks:")
        edit_ids = [t["id"] for t in filtered]
        sel_edit_id = st.selectbox("Choose Transaction ID to Edit:", options=edit_ids, key="sel_edit_id")
        target_txn = next((t for t in filtered if t["id"] == sel_edit_id), None)

        if target_txn:
            with st.form("form_edit_txn"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_date = st.date_input(
                        "Date",
                        value=datetime.strptime(target_txn["date"], "%Y-%m-%d").date(),
                        key="edit_date"
                    )
                    is_expense = target_txn.get("type") == "Expense"
                    avail_cats = EXPENSE_CATEGORIES if is_expense else INCOME_CATEGORIES
                    curr_cat_idx = avail_cats.index(target_txn["category"]) if target_txn["category"] in avail_cats else 0
                    e_cat = st.selectbox("Category", options=avail_cats, index=curr_cat_idx, key="edit_cat")
                    e_amt = st.number_input(
                        "Amount (in ₹)",
                        min_value=1.0,
                        max_value=10000000.0,
                        value=float(target_txn["amount"]),
                        step=50.0,
                        format="%.2f",
                        key="edit_amt"
                    )

                with ec2:
                    curr_pm_idx = PAYMENT_MODES.index(target_txn["payment_mode"]) if target_txn["payment_mode"] in PAYMENT_MODES else 0
                    e_pm = st.selectbox("Payment Mode", options=PAYMENT_MODES, index=curr_pm_idx, key="edit_pm")
                    e_desc = st.text_input("Description", value=target_txn.get("description", ""), key="edit_desc")

                submit_edit = st.form_submit_button("Update Transaction Record", use_container_width=True)
                if submit_edit:
                    upd_payload = {
                        "id": sel_edit_id,
                        "date": e_date.strftime("%Y-%m-%d"),
                        "type": target_txn["type"],
                        "category": e_cat,
                        "amount": e_amt,
                        "payment_mode": e_pm,
                        "description": e_desc.strip()
                    }
                    if update_transaction(upd_payload):
                        st.success(f"✅ Transaction {sel_edit_id} updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update transaction.")

    # 2. DELETE TRANSACTION
    with tab_delete:
        st.caption("Select a transaction ID to permanently remove it from your records:")
        d_col1, d_col2 = st.columns([3, 1.2])

        with d_col1:
            sel_del_id = st.selectbox("Choose Transaction ID to Delete:", options=edit_ids, key="sel_del_id")
            del_txn_obj = next((t for t in filtered if t["id"] == sel_del_id), None)
            if del_txn_obj:
                st.write(
                    f"**Selected Record:** `{del_txn_obj['id']}` • {del_txn_obj['date']} • "
                    f"**{del_txn_obj['type']}** • {del_txn_obj['category']} • **{format_inr(del_txn_obj['amount'])}**"
                )

        with d_col2:
            st.write("")
            st.write("")
            if st.button("Permanently Delete", type="primary", use_container_width=True):
                if sel_del_id and delete_transaction(sel_del_id):
                    st.success(f"Transaction {sel_del_id} deleted successfully.")
                    st.rerun()
                else:
                    st.error("Failed to delete transaction.")
