"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_intelligence.py
Description: Smart Budget Intelligence Engine View. Visualizes daily safe limits,
             linear run-rate projections, risk index, and recommendations.
Assigned Contribution: HARSH (S26CSEU1935) - Intelligence & Alert Logic
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from config import COLORS
from modules.data_manager import load_transactions, get_monthly_budget
from modules.calc_engine import format_inr, get_available_months
from modules.budget_engine import get_budget_alerts
from modules.intelligence_engine import generate_budget_intelligence


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Smart Budget Intelligence</h1>
        <div class="hero-subtitle">Computational forecasting, daily safe-to-spend run-rate limits, and explainable overspending risk modeling.</div>
    </div>
    """, unsafe_allow_html=True)

    # Educational Lead Banner
    st.markdown(f"""
    <div style="background-color: {COLORS['card_bg']}; border: 1.5px solid {COLORS['card_border']}; border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div>
                <strong style="color: {COLORS['accent_green']}; font-size: 1.05rem;">⚡ Deterministic Intelligence Layer</strong>
                <span style="color: {COLORS['text_muted']}; font-size: 0.85rem; margin-left: 10px;">(Module Lead: Harsh – S26CSEU1935)</span>
            </div>
            <div style="color: {COLORS['text_muted']}; font-size: 0.82rem;">
                Mathematical Modeling • Zero-Division Safety • Rule-Based Risk Index
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Month Selector
    transactions = load_transactions()
    available_months = get_available_months(transactions)
    current_ym = datetime.now().strftime("%Y-%m")

    col_m, _ = st.columns([2, 3])
    with col_m:
        selected_month = st.selectbox(
            "Select Evaluation Timeline:",
            options=available_months,
            index=available_months.index(current_ym) if current_ym in available_months else 0
        )

    # Fetch budget data and run intelligence pipeline
    budget_data = get_monthly_budget(selected_month)
    intel = generate_budget_intelligence(selected_month, transactions, budget_data)
    cal = intel["calendar"]

    # Historical Month Notice if inspecting past month
    if cal["is_past"]:
        st.info(f"ℹ️ You are viewing **historical records** for {cal['month_name']} {cal['year']}. Forecast projections and daily safe limits are only active for the current calendar month.")

    # --- TOP 4 KPI CARDS: DAILY SAFE, FORECAST, OVERSPEND, RISK ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Safe Daily Spending</div>
            <div class="kpi-value green">{format_inr(intel['safe_daily_spending'])}</div>
            <div class="kpi-subtext">{cal['remaining_days']} days left in {cal['month_name']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        forecast_val = intel["projected_expenses"]
        total_bud = intel["total_budget"]
        forecast_class = "green" if (total_bud > 0 and forecast_val <= total_bud) else "red"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Projected Month-End Spend</div>
            <div class="kpi-value {forecast_class}">{format_inr(forecast_val)}</div>
            <div class="kpi-subtext">Burn Rate: {format_inr(intel['avg_daily_spending'])}/day</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        overspend = intel["projected_overspending"]
        over_class = "green" if overspend == 0 else "red"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Projected Overspending</div>
            <div class="kpi-value {over_class}">{format_inr(overspend)}</div>
            <div class="kpi-subtext">{'Surplus planned' if overspend == 0 else 'Projected Deficit'}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Overspending Risk Index</div>
            <div class="kpi-value" style="color: {intel['risk_color']};">{intel['risk_score']}/100</div>
            <div class="kpi-subtext">Level: <strong>{intel['risk_level']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 2: GAUGE CHART & SMART RECOMMENDATIONS ---
    col_chart, col_recom = st.columns([1, 1])

    with col_chart:
        st.subheader("Overspending Risk Gauge")
        # Plotly Gauge Chart for Risk Index
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=intel["risk_score"],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Score: {intel['risk_level']}", 'font': {'color': COLORS['text_main'], 'size': 16}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': COLORS['text_muted']},
                'bar': {'color': intel['risk_color']},
                'bgcolor': COLORS['card_bg'],
                'borderwidth': 2,
                'bordercolor': COLORS['card_border'],
                'steps': [
                    {'range': [0, 70], 'color': "rgba(16, 185, 129, 0.2)"},    # Low (0-69)
                    {'range': [70, 90], 'color': "rgba(245, 158, 11, 0.2)"},   # Moderate (70-89)
                    {'range': [90, 100], 'color': "rgba(239, 68, 68, 0.25)"}   # High / Critical (90-100)
                ],
                'threshold': {
                    'line': {'color': "#EF4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS['text_main']),
            height=280,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption("ℹ️ *Rule-based mathematical indicator of projected budget utilization (0–69 Low, 70–89 Moderate, 90–99 High, 100 Critical).*")

    with col_recom:
        st.subheader("💡 Smart Financial Recommendations")
        recommendations = intel["recommendations"]
        if not recommendations:
            st.info("No recommendations generated. Add transactions or configure monthly budgets to view advice.")
        else:
            for rec in recommendations:
                st.markdown(f"""
                <div style="background-color: {COLORS['card_bg']}; border-left: 4px solid {COLORS['accent_cyan']}; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.65rem; font-size: 0.9rem;">
                    {rec}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 3: CATEGORY BUDGET RANKING & PROGRESS ---
    st.subheader("Category Expenditure Ranking & Utilization")
    ranked = intel["ranked_categories"]

    for item in ranked:
        cat = item["category"]
        spent = item["spent"]
        budget = item["budget"]
        remaining = item["remaining"]
        util = item["utilization_pct"]
        status = item["status"]

        with st.container():
            c1, c2 = st.columns([3, 4])
            with c1:
                if status == "Normal":
                    b_badge = '<span class="badge-safe">Normal</span>'
                elif status == "Spending Awareness":
                    b_badge = '<span class="badge-warning">Awareness</span>'
                elif status == "High Spending Warning":
                    b_badge = '<span style="background-color: rgba(249, 115, 22, 0.15); color: #F97316; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">Warning</span>'
                elif status == "Budget Exceeded":
                    b_badge = '<span class="badge-danger">Exceeded</span>'
                else:
                    b_badge = f'<span style="color: {COLORS["text_muted"]}; font-size: 0.8rem;">{status}</span>'

                u_str = f"{util:.1f}%" if util is not None else "N/A"
                st.markdown(f"**#{item['rank']} {cat}** {b_badge} &nbsp;|&nbsp; Spent: **{format_inr(spent)}** of {format_inr(budget)} ({u_str})", unsafe_allow_html=True)

            with c2:
                if budget > 0:
                    prog_frac = min(1.0, spent / budget)
                    st.progress(prog_frac)
                    if remaining >= 0:
                        st.caption(f"Remaining: {format_inr(remaining)} | Share of Total: {item['share_of_total_pct']}%")
                    else:
                        st.caption(f"<span style='color:#EF4444;'>Deficit: -{format_inr(abs(remaining))}</span> | Share: {item['share_of_total_pct']}%", unsafe_allow_html=True)
                else:
                    st.caption("No budget set for this category.")

        st.markdown("<hr style='border: 0.5px solid #23314E; margin: 0.4rem 0 0.8rem 0;'>", unsafe_allow_html=True)

    # --- ROW 4: MATHEMATICAL FORMULAS (TRANSPARENT VIVA REFERENCE) ---
    with st.expander("📐 Computational Thinking & Mathematical Formulas (Viva Reference)", expanded=False):
        st.markdown(r"""
        ### Mathematical Modeling Breakdown:
        
        1. **Average Daily Spending ($A$)**:
           $$A = \frac{\text{Month-to-Date Incurred Expenses}}{\text{Days Elapsed in Current Month}}$$
        
        2. **Month-End Linear Run-Rate Forecast ($E_{\text{forecast}}$)**:
           $$E_{\text{forecast}} = A \times \text{Total Days in Month}$$
        
        3. **Projected Overspending Amount ($O_{\text{projected}}$)**:
           $$O_{\text{projected}} = \max(0, E_{\text{forecast}} - \text{Monthly Budget})$$
        
        4. **Safe Daily Spending Limit ($L_{\text{safe}}$)**:
           $$\text{Remaining Budget} = \text{Monthly Budget} - \text{Incurred Expenses}$$
           $$\text{Remaining Days} = \text{Total Days in Month} - \text{Current Day} + 1$$
           $$L_{\text{safe}} = \begin{cases} \frac{\text{Remaining Budget}}{\text{Remaining Days}} & \text{if Remaining Budget} > 0 \\ 0.00 & \text{if Remaining Budget} \le 0 \end{cases}$$
        
        5. **Overspending Risk Index (0–100 Rule-Based Score)**:
           $$\text{Raw Ratio} = \left(\frac{E_{\text{forecast}}}{\text{Monthly Budget}}\right) \times 100$$
           $$\text{Risk Score} = \min(100, \max(0, \text{round}(\text{Raw Ratio})))$$
           - **0 to 69:** Low Risk (Spending within healthy budget envelope)
           - **70 to 89:** Moderate Risk (Enters caution / awareness territory)
           - **90 to 99:** High Risk (Critical warning, approaching ceiling)
           - **100:** Critical Risk (Forecast meets or exceeds 100% allocation)
        """)
