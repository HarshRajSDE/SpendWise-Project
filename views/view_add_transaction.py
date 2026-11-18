"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_add_transaction.py
Description: Polished Transaction Entry View. Provides an intuitive form for adding
             income and expense records with clear validation and presets.
================================================================================
"""

import streamlit as st
from datetime import date
from config import EXPENSE_CATEGORIES, INCOME_CATEGORIES, PAYMENT_MODES, COLORS
from modules.data_manager import add_transaction, load_transactions
from modules.calc_engine import format_inr


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Add Transaction</h1>
        <div class="hero-subtitle">Record your daily income and expense entries with payment modes and remarks.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_exp, tab_inc = st.tabs(["💸 Record Expense", "💰 Record Income"])

    # ==========================================================================
    # TAB 1: RECORD EXPENSE
    # ==========================================================================
    with tab_exp:
        with st.form("form_add_expense", clear_on_submit=True):
            st.markdown("### Expense Details")
            c1, c2 = st.columns(2)

            with c1:
                exp_date = st.date_input(
                    "Transaction Date",
                    value=date.today(),
                    key="add_exp_date"
                )
                exp_category = st.selectbox(
                    "Expense Category",
                    options=EXPENSE_CATEGORIES,
                    key="add_exp_category"
                )
                exp_amount = st.number_input(
                    "Amount (in ₹)",
                    min_value=1.0,
                    max_value=10000000.0,
                    value=250.0,
                    step=50.0,
                    format="%.2f",
                    key="add_exp_amount"
                )

            with c2:
                exp_payment = st.selectbox(
                    "Payment Mode",
                    options=PAYMENT_MODES,
                    key="add_exp_payment"
                )
                exp_desc = st.text_input(
                    "Description / Remarks",
                    placeholder="e.g., Campus lunch, Metro recharge, Books",
                    key="add_exp_desc"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_exp = st.form_submit_button("💾 Save Expense Entry", use_container_width=True)

            if submit_exp:
                if exp_amount <= 0:
                    st.error("⚠️ Please specify a valid expense amount greater than ₹0.")
                else:
                    new_rec = {
                        "date": exp_date.strftime("%Y-%m-%d"),
                        "type": "Expense",
                        "category": exp_category,
                        "amount": exp_amount,
                        "payment_mode": exp_payment,
                        "description": exp_desc.strip() if exp_desc.strip() else f"{exp_category} Expense"
                    }
                    if add_transaction(new_rec):
                        st.success(f"✅ Successfully recorded expense of {format_inr(exp_amount)} under '{exp_category}'!")
                    else:
                        st.error("Failed to append transaction. Please verify file permissions.")

    # ==========================================================================
    # TAB 2: RECORD INCOME
    # ==========================================================================
    with tab_inc:
        with st.form("form_add_income", clear_on_submit=True):
            st.markdown("### Income Details")
            c1, c2 = st.columns(2)

            with c1:
                inc_date = st.date_input(
                    "Received Date",
                    value=date.today(),
                    key="add_inc_date"
                )
                inc_category = st.selectbox(
                    "Income Source / Category",
                    options=INCOME_CATEGORIES,
                    key="add_inc_category"
                )
                inc_amount = st.number_input(
                    "Amount (in ₹)",
                    min_value=1.0,
                    max_value=10000000.0,
                    value=5000.0,
                    step=500.0,
                    format="%.2f",
                    key="add_inc_amount"
                )

            with c2:
                inc_payment = st.selectbox(
                    "Payment Mode / Channel",
                    options=PAYMENT_MODES,
                    key="add_inc_payment"
                )
                inc_desc = st.text_input(
                    "Description / Source Details",
                    placeholder="e.g., Monthly stipend, Parental allowance, Freelance gig",
                    key="add_inc_desc"
                )

            st.markdown("<br>", unsafe_allow_html=True)
            submit_inc = st.form_submit_button("💾 Save Income Entry", use_container_width=True)

            if submit_inc:
                if inc_amount <= 0:
                    st.error("⚠️ Please specify a valid income amount greater than ₹0.")
                else:
                    new_rec = {
                        "date": inc_date.strftime("%Y-%m-%d"),
                        "type": "Income",
                        "category": inc_category,
                        "amount": inc_amount,
                        "payment_mode": inc_payment,
                        "description": inc_desc.strip() if inc_desc.strip() else f"{inc_category} Income"
                    }
                    if add_transaction(new_rec):
                        st.success(f"✅ Successfully recorded income of {format_inr(inc_amount)} from '{inc_category}'!")
                    else:
                        st.error("Failed to append transaction. Please verify file permissions.")

    # --- RECENT TRANSACTIONS QUICK PREVIEW ---
    st.markdown("<br>", unsafe_allow_html=True)
    all_txns = load_transactions()
    if all_txns:
        with st.expander("👀 View Recently Added Transactions (Latest 5 Entries)", expanded=False):
            recent_sorted = sorted(all_txns, key=lambda x: x.get("date", ""), reverse=True)[:5]
            for r in recent_sorted:
                is_inc = r.get("type") == "Income"
                st.write(
                    f"**{r.get('date')}** | {'🟢' if is_inc else '🔴'} **{r.get('type')}** | "
                    f"{r.get('category')} | **{format_inr(r.get('amount', 0))}** via {r.get('payment_mode')} ({r.get('description')})"
                )
