"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_budget.py
Description: Advanced Budget Management and Threshold Monitoring View.
Assigned Contribution: HARSH (S26CSEU1935) - Budget Monitoring & Alert Logic
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
from datetime import datetime
from config import (
    EXPENSE_CATEGORIES,
    THRESHOLD_SAFE,
    THRESHOLD_WARNING,
    THRESHOLD_CRITICAL,
    COLORS
)
from modules.data_manager import (
    get_monthly_budget,
    set_monthly_budget,
    load_transactions
)
from modules.calc_engine import (
    format_inr,
    filter_transactions_by_month,
    calculate_category_expenses,
    get_available_months
)
from modules.budget_engine import (
    compute_utilization,
    get_budget_alerts,
    rank_spending_categories,
    check_category_budget
)


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Budget Management & Limits</h1>
        <div class="hero-subtitle">Plan, allocate, and monitor category-wise spending limits with deterministic 4-tier alert monitoring.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- TOP EDUCATIONAL BANNER: THRESHOLD LOGIC (Harsh's Focus) ---
    st.markdown(f"""
    <div style="background-color: {COLORS['card_bg']}; border: 1.5px solid {COLORS['card_border']}; border-radius: 12px; padding: 1.1rem 1.35rem; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div>
                <strong style="color: {COLORS['accent_green']}; font-size: 1.05rem;">🛡️ SpendWise Multi-Tier Alert System</strong>
                <span style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin-left: 10px;">(Module Lead: Harsh – S26CSEU1935)</span>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="badge-safe">Normal (&lt; 70%)</span>
                <span class="badge-warning">Awareness (70% – 89%)</span>
                <span style="background-color: rgba(249, 115, 22, 0.15); color: #F97316; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(249, 115, 22, 0.3);">
                    Warning (90% – 99%)
                </span>
                <span class="badge-danger">Exceeded (≥ 100%)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- MONTH SELECTOR ---
    transactions = load_transactions()
    available_months = get_available_months(transactions)
    current_ym = datetime.now().strftime("%Y-%m")

    col_m1, col_m2 = st.columns([2, 3])
    with col_m1:
        selected_month = st.selectbox(
            "Select Target Budget Month:",
            options=available_months,
            index=available_months.index(current_ym) if current_ym in available_months else 0
        )

    # Load budget configuration for selected month
    budget_data = get_monthly_budget(selected_month)
    total_budget = budget_data.get("monthly_total", 0.0)
    category_budgets = budget_data.get("categories", {})

    # Calculate actual expenses incurred in selected month
    month_txns = filter_transactions_by_month(transactions, selected_month)
    expense_txns = [t for t in month_txns if t.get("type") == "Expense"]
    category_expenses = calculate_category_expenses(expense_txns)
    total_expenses = sum(category_expenses.values())

    # --- SECTION 1: OVERALL MONTHLY BUDGET UTILIZATION ---
    overall_util, overall_status = compute_utilization(total_expenses, total_budget)

    st.subheader(f"1. Overall Budget Performance ({selected_month})")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Allocated Budget</div>
            <div class="kpi-value cyan">{format_inr(total_budget)}</div>
            <div class="kpi-subtext">Total planned limit</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Actual Expenses</div>
            <div class="kpi-value red">{format_inr(total_expenses)}</div>
            <div class="kpi-subtext">{len(expense_txns)} expense transactions</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        remaining_budget = total_budget - total_expenses
        rem_class = "green" if remaining_budget >= 0 else "red"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Remaining Budget</div>
            <div class="kpi-value {rem_class}">{format_inr(remaining_budget)}</div>
            <div class="kpi-subtext">{'Surplus' if remaining_budget >= 0 else 'Deficit'}</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        if total_budget > 0:
            if overall_status == "Normal":
                util_color = "green"
            elif overall_status == "Spending Awareness":
                util_color = "yellow"
            else:
                util_color = "red"
            util_display = f"{overall_util:.1f}%"
        else:
            util_color = "cyan"
            util_display = "No Budget"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Overall Utilization</div>
            <div class="kpi-value {util_color}">{util_display}</div>
            <div class="kpi-subtext">Status: <strong>{overall_status}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    if total_budget > 0:
        progress_val = min(1.0, max(0.0, total_expenses / total_budget))
        st.progress(progress_val)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 2: ACTIVE SPENDING ALERTS ---
    alerts = get_budget_alerts(category_budgets, category_expenses, total_budget, total_expenses)

    st.subheader("2. Spending Alert Notifications")
    if not alerts:
        st.success("✅ All budget categories and monthly totals are within safe spending limits (< 70%). No critical alerts active.")
    else:
        for alert in alerts:
            border_color = alert.get("color", "#EF4444")
            st.markdown(f"""
            <div style="background-color: {COLORS['card_bg']}; border-left: 5px solid {border_color}; border-radius: 8px; padding: 0.85rem 1.15rem; margin-bottom: 0.65rem; border-top: 1px solid {COLORS['card_border']}; border-right: 1px solid {COLORS['card_border']}; border-bottom: 1px solid {COLORS['card_border']};">
                <div style="display:flex; justify-content: space-between; align-items:center;">
                    <strong style="color: {border_color}; font-size: 0.95rem;">{alert['severity']} — {alert['category']}</strong>
                    <span style="font-size: 0.8rem; color: {COLORS['text_muted']};">{alert['status']}</span>
                </div>
                <div style="margin-top: 4px; color: {COLORS['text_main']}; font-size: 0.9rem;">
                    {alert['message']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 3: CATEGORY BUDGET PROGRESS & RANKING ---
    st.subheader("3. Category Budget Tracking & Breakdown")
    ranked = rank_spending_categories(category_expenses, category_budgets)

    for item in ranked:
        cat = item["category"]
        spent = item["spent"]
        budget = item["budget"]
        remaining = item["remaining"]
        util = item["utilization_pct"]
        status = item["status"]

        with st.container():
            col_info, col_bar = st.columns([3, 4])
            with col_info:
                if status == "Normal":
                    badge_html = '<span class="badge-safe">Normal</span>'
                elif status == "Spending Awareness":
                    badge_html = '<span class="badge-warning">Awareness</span>'
                elif status == "High Spending Warning":
                    badge_html = '<span style="background-color: rgba(249, 115, 22, 0.15); color: #F97316; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">Warning</span>'
                elif status == "Budget Exceeded":
                    badge_html = '<span class="badge-danger">Exceeded</span>'
                else:
                    badge_html = f'<span style="color: {COLORS["text_muted"]}; font-size: 0.8rem;">{status}</span>'

                util_str = f"{util:.1f}%" if util is not None else "N/A"
                st.markdown(f"**#{item['rank']} {cat}** {badge_html} &nbsp;|&nbsp; Spent: **{format_inr(spent)}** of {format_inr(budget)} ({util_str})", unsafe_allow_html=True)

            with col_bar:
                if budget > 0:
                    prog_frac = min(1.0, spent / budget)
                    st.progress(prog_frac)
                    if remaining >= 0:
                        st.caption(f"Remaining allowance: {format_inr(remaining)}")
                    else:
                        st.caption(f"<span style='color:#EF4444;'>Deficit: -{format_inr(abs(remaining))}</span>", unsafe_allow_html=True)
                else:
                    st.caption("No budget set for this category.")

        st.markdown("<hr style='border: 0.5px solid #23314E; margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # --- SECTION 4: EDIT/UPDATE CATEGORY BUDGET ALLOCATION ---
    st.subheader("4. Update Category Budget Allocation")
    st.caption(f"Adjust planned expenditure limits for {selected_month}. Enter ₹0 for unbudgeted categories.")

    with st.form("update_budget_form"):
        updated_allocations = {}
        cols = st.columns(2)

        for idx, cat in enumerate(EXPENSE_CATEGORIES):
            c_target = cols[idx % 2]
            with c_target:
                curr_val = float(category_budgets.get(cat, 0.0))
                new_val = st.number_input(
                    f"{cat} Limit (in ₹)",
                    min_value=0.0,
                    max_value=1000000.0,
                    value=curr_val,
                    step=500.0,
                    format="%.2f",
                    key=f"cfg_bud_{cat}"
                )
                updated_allocations[cat] = new_val

        save_btn = st.form_submit_button("💾 Save Budget Limits", use_container_width=True)

        if save_btn:
            new_total = sum(updated_allocations.values())
            if set_monthly_budget(selected_month, updated_allocations, total_budget=new_total):
                st.success(f"✅ Budget limits for {selected_month} successfully saved! Total allocation: {format_inr(new_total)}")
                st.rerun()
            else:
                st.error("Failed to save budget settings.")
