"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: app.py
Description: Main application entry point and sidebar routing controller.
             Theme: Deep Dark Navy with Emerald Green SaaS aesthetic.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
Institution: Bennett University
================================================================================
"""

import streamlit as st
from datetime import datetime

from config import PROJECT_NAME, COURSE_CODE, ACADEMIC_YEAR, COLORS
from modules.styles import apply_custom_styles
from modules.brand_logo import render_main_header_logo, render_sidebar_logo, render_sidebar_bottom
from modules.data_manager import init_data_files, load_transactions
from modules.calc_engine import calculate_total_income, calculate_total_expenses, calculate_net_balance, format_inr

# Import View Modules
from views import (
    view_overview,
    view_add_transaction,
    view_transactions,
    view_budget,
    view_intelligence,
    view_analytics,
    view_reports,
    view_about,
    view_settings,
    view_login,
    view_admin
)

# ==============================================================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="SpendWise – Smart Financial Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark Navy + Emerald Green custom SaaS design theme
apply_custom_styles()

# Ensure database and data files exist
init_data_files()

# ==============================================================================
# 2. MULTI-USER AUTHENTICATION GATE
# ==============================================================================
if not st.session_state.get("authenticated", False):
    view_login.render_login_page()
    st.stop()

current_user = st.session_state.get("user", {})

# ==============================================================================
# 3. SIDEBAR NAVIGATION & QUICK STATUS
# ==============================================================================
with st.sidebar:
    # Brand Identity Header (Compact Custom Logo)
    st.markdown(render_sidebar_logo(), unsafe_allow_html=True)

    # Advanced Fintech SaaS Navigation menu
    nav_options = [
        "Overview Dashboard",
        "Add Transaction",
        "All Transactions",
        "Budget Management",
        "Smart Budget Intelligence",
        "Spending Analytics",
        "Reports & Data",
        "About Project",
        "Settings"
    ]
    if current_user.get("role") == "admin":
        nav_options.append("Admin Console")

    default_idx = 0
    if "nav_override" in st.session_state:
        target = st.session_state.pop("nav_override")
        if target in nav_options:
            default_idx = nav_options.index(target)

    nav_selection = st.radio(
        "NAVIGATION",
        options=nav_options,
        index=default_idx,
        label_visibility="collapsed"
    )

    # Quick Financial Health Widget & Profile in Sidebar
    txns = load_transactions()
    total_inc = calculate_total_income(txns)
    total_exp = calculate_total_expenses(txns)
    balance = calculate_net_balance(total_inc, total_exp)
    now_str = datetime.now().strftime("%B %Y")

    # Bottom Sidebar Section (Profile, Liquidity, Version)
    st.markdown(
        render_sidebar_bottom(
            total_txns=len(txns),
            balance_str=format_inr(balance),
            balance_val=balance,
            total_exp_str=format_inr(total_exp),
            now_str=now_str,
            user_info=current_user
        ),
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True, type="secondary", help="Securely end current user session"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state.clear()
        st.rerun()


# ==============================================================================
# 4. MAIN DASHBOARD BRAND HEADER (Visible on every application page)
# ==============================================================================
st.markdown(render_main_header_logo(show_meta=True, user_info=current_user), unsafe_allow_html=True)


# ==============================================================================
# 5. VIEW ROUTER
# ==============================================================================
if nav_selection == "Overview Dashboard":
    view_overview.render()
elif nav_selection == "Add Transaction":
    view_add_transaction.render()
elif nav_selection == "All Transactions":
    view_transactions.render()
elif nav_selection == "Budget Management":
    view_budget.render()
elif nav_selection == "Smart Budget Intelligence":
    view_intelligence.render()
elif nav_selection == "Spending Analytics":
    view_analytics.render()
elif nav_selection in ("Reports & Data", "Reports and Data Management"):
    view_reports.render()
elif nav_selection == "About Project":
    view_about.render()
elif nav_selection == "Settings":
    view_settings.render()
elif nav_selection == "Admin Console":
    view_admin.render()
