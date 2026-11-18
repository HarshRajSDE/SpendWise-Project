"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_analytics.py
Description: Premium Visual Analytics View. Interactive Plotly charts for
             category distributions, multi-month comparisons, cumulative daily
             trends, payment mode distributions, and ranked tables.
================================================================================
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from modules.data_manager import load_transactions
from modules.calc_engine import (
    format_inr,
    calculate_category_expenses,
    get_available_months,
    filter_transactions_by_month
)
from config import COLORS


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Spending Analytics</h1>
        <div class="hero-subtitle">Interactive data visualizations, trend trajectories, and category composition insights.</div>
    </div>
    """, unsafe_allow_html=True)

    transactions = load_transactions()

    if not transactions:
        st.markdown("""
        <div class="empty-state-box">
            <div class="empty-state-icon">📊</div>
            <div class="empty-state-title">No Analytics Data Available</div>
            <div class="empty-state-desc">
                Record transactions or load the sample demo dataset to explore interactive charts,
                spending velocity graphs, and category breakdowns.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Timeline Selector
    available_months = ["All Time"] + get_available_months(transactions)
    col_sel, _ = st.columns([2.5, 4])
    with col_sel:
        selected_period = st.selectbox("Select Analytics Timeline:", options=available_months)

    if selected_period == "All Time":
        active_txns = transactions
        period_title = "All Time"
    else:
        active_txns = filter_transactions_by_month(transactions, selected_period)
        period_title = datetime.strptime(selected_period, "%Y-%m").strftime("%B %Y")

    if not active_txns:
        st.warning("No transactions recorded for the selected timeline.")
        return

    expense_txns = [t for t in active_txns if t.get("type") == "Expense"]
    income_txns = [t for t in active_txns if t.get("type") == "Income"]

    # --- ROW 1: CATEGORY DONUT & PAYMENT MODE BREAKDOWN ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🍩 Expense Category Share")
        cat_expenses = calculate_category_expenses(expense_txns)
        chart_data = [{"Category": cat, "Amount": amt} for cat, amt in cat_expenses.items() if amt > 0]

        if chart_data:
            df_cat = pd.DataFrame(chart_data)
            fig_pie = px.pie(
                df_cat,
                names="Category",
                values="Amount",
                hole=0.55,
                color_discrete_sequence=["#10B981", "#00B4D8", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#3B82F6"]
            )
            fig_pie.update_traces(
                textposition="outside",
                textinfo="percent+label",
                marker=dict(line=dict(color="#0B132B", width=2))
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=COLORS['text_main']),
                height=320,
                margin=dict(l=20, r=20, t=30, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data recorded in this period.")

    with col2:
        st.subheader("💳 Spending by Payment Mode")
        pm_totals = {}
        for t in expense_txns:
            pm = t.get("payment_mode", "UPI")
            pm_totals[pm] = pm_totals.get(pm, 0.0) + t.get("amount", 0.0)

        if pm_totals:
            df_pm = pd.DataFrame([{"Mode": k, "Amount": v} for k, v in pm_totals.items()])
            fig_pm = px.bar(
                df_pm,
                x="Mode",
                y="Amount",
                color="Mode",
                color_discrete_sequence=px.colors.qualitative.Prism,
                text="Amount"
            )
            fig_pm.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            fig_pm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=COLORS['text_main']),
                yaxis=dict(gridcolor="#1E2D4A", showgrid=True),
                xaxis=dict(showgrid=False),
                height=320,
                margin=dict(l=20, r=20, t=30, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_pm, use_container_width=True)
        else:
            st.info("No payment mode data available.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 2: DAILY SPENDING TREND & CUMULATIVE TRAJECTORY ---
    st.subheader(f"📈 Daily Spending Trajectory ({period_title})")
    if expense_txns:
        df_exp = pd.DataFrame(expense_txns)
        # Group by date
        daily_grp = df_exp.groupby("date")["amount"].sum().reset_index().sort_values("date")
        daily_grp["cumulative"] = daily_grp["amount"].cumsum()

        fig_trend = go.Figure()
        # Daily spending bar
        fig_trend.add_trace(go.Bar(
            x=daily_grp["date"],
            y=daily_grp["amount"],
            name="Daily Spend",
            marker_color="rgba(16, 185, 129, 0.4)",
            yaxis="y"
        ))
        # Cumulative line
        fig_trend.add_trace(go.Scatter(
            x=daily_grp["date"],
            y=daily_grp["cumulative"],
            name="Cumulative Total",
            line=dict(color="#00B4D8", width=3),
            yaxis="y2"
        ))
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS['text_main']),
            xaxis=dict(showgrid=False, title="Date"),
            yaxis=dict(title="Daily Amount (₹)", gridcolor="#1E2D4A"),
            yaxis2=dict(title="Cumulative (₹)", overlaying="y", side="right", showgrid=False),
            height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No expense data available to build trend chart.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 3: MULTI-MONTH COMPARISON ---
    all_months_list = get_available_months(transactions)
    if len(all_months_list) > 1:
        st.subheader("🗓️ Multi-Month Financial Comparison")
        month_records = []
        for ym in reversed(all_months_list[:6]):
            m_txns = filter_transactions_by_month(transactions, ym)
            inc = sum(t["amount"] for t in m_txns if t.get("type") == "Income")
            exp = sum(t["amount"] for t in m_txns if t.get("type") == "Expense")
            month_records.append({"Month": ym, "Type": "Income", "Amount": inc})
            month_records.append({"Month": ym, "Type": "Expense", "Amount": exp})

        df_multi = pd.DataFrame(month_records)
        fig_multi = px.bar(
            df_multi,
            x="Month",
            y="Amount",
            color="Type",
            barmode="group",
            color_discrete_map={"Income": "#10B981", "Expense": "#EF4444"}
        )
        fig_multi.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS['text_main']),
            yaxis=dict(gridcolor="#1E2D4A"),
            xaxis=dict(showgrid=False),
            height=320,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_multi, use_container_width=True)
