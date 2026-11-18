"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_overview.py
Description: Luxury Fintech Overview Dashboard View.
             Features high-level KPI cards, responsive cash flow & donut charts,
             smart budget alert cards with utilization metrics, and a premium
             recent transaction feed with seamless navigation.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from config import COLORS, EXPENSE_CATEGORIES
from modules.data_manager import load_transactions, get_monthly_budget
from modules.calc_engine import (
    get_financial_summary,
    format_inr,
    calculate_category_expenses,
    filter_transactions_by_month,
    get_available_months
)
from modules.budget_engine import compute_utilization, get_budget_alerts
from modules.sample_data import load_sample_dataset

# Category Icon Mapping for Premium UI Representation
CATEGORY_ICONS = {
    "Food": "🍔",
    "Transport": "🚗",
    "Shopping": "🛍️",
    "Education": "📚",
    "Entertainment": "🎬",
    "Bills": "💡",
    "Others": "📦",
    "Salary": "💼",
    "Allowance / Pocket Money": "💵",
    "Freelance / Gig": "💻",
    "Scholarship": "🎓",
    "Gifts / Bonus": "🎁",
    "Investments": "📈",
    "Overall Budget": "🏛️",
}


def _get_severity_meta(status: str) -> dict:
    """Returns color, badge label, and icon for spending alert severity levels."""
    if status == "Budget Exceeded":
        return {"color": "#FF5478", "badge": "Exceeded", "icon": "🚨"}
    elif status == "High Spending Warning":
        return {"color": "#F97316", "badge": "Critical", "icon": "⚠️"}
    elif status == "Spending Awareness":
        return {"color": "#FFB547", "badge": "Warning", "icon": "⚡"}
    elif status == "Normal":
        return {"color": "#35D49A", "badge": "Safe", "icon": "✅"}
    else:
        return {"color": "#A69BBE", "badge": "Notice", "icon": "ℹ️"}


def render():
    transactions = load_transactions()

    # --- TOP WELCOME HEADER ---
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Financial Dashboard</h1>
        <div class="hero-subtitle">Real-time overview of your income, expenditure, liquidity, and active budget health.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- EMPTY STATE CHECK ---
    if not transactions:
        st.markdown("""
        <div class="empty-state-box">
            <div class="empty-state-icon">💳</div>
            <div class="empty-state-title">Welcome to SpendWise</div>
            <div class="empty-state-desc">
                Your personal expense tracker is ready and waiting for your first entry.
                Record a transaction manually or load the curated sample demo dataset
                to test all intelligence calculations and interactive visualizations.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([1, 1.2, 1])
        with col_b:
            if st.button("🚀 Load Sample Demo Dataset (INR ₹)", key="btn_overview_load_demo", use_container_width=True, type="primary"):
                result = load_sample_dataset()
                st.success(f"Loaded {result['transactions_loaded']} sample transactions successfully!")
                st.rerun()
        return

    # --- TIMELINE FILTER SELECTOR ---
    available_months = get_available_months(transactions)
    current_ym = datetime.now().strftime("%Y-%m")

    col_flt, _ = st.columns([2.5, 4])
    with col_flt:
        selected_period = st.selectbox(
            "Evaluation Period",
            options=["All Time"] + available_months,
            index=1 if current_ym in available_months else 0
        )

    # Filter transactions based on selection
    if selected_period == "All Time":
        active_txns = transactions
        period_label = "All Time Activity"
        eval_month = current_ym
    else:
        active_txns = filter_transactions_by_month(transactions, selected_period)
        period_label = datetime.strptime(selected_period, "%Y-%m").strftime("%B %Y")
        eval_month = selected_period

    # Core Financial Metrics
    summary = get_financial_summary(active_txns)
    total_income = summary["total_income"]
    total_expenses = summary["total_expenses"]
    net_balance = summary["net_balance"]
    savings_rate = summary["savings_rate"]

    # Budget Context for Month
    budget_data = get_monthly_budget(eval_month)
    total_budget = budget_data.get("monthly_total", 0.0)
    category_budgets = budget_data.get("categories", {})
    expense_txns = [t for t in active_txns if t.get("type") == "Expense"]
    cat_expenses = calculate_category_expenses(expense_txns)

    # ==========================================================================
    # ROW 1: PRIMARY KPI CARDS
    # ==========================================================================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                <span>TOTAL INCOME</span>
                <span style="color:#35D49A; font-size:1rem;">📈</span>
            </div>
            <div class="kpi-value green">{format_inr(total_income)}</div>
            <div class="kpi-subtext">Period: {period_label}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                <span>TOTAL EXPENDITURE</span>
                <span style="color:#FF5478; font-size:1rem;">📉</span>
            </div>
            <div class="kpi-value red">{format_inr(total_expenses)}</div>
            <div class="kpi-subtext">{len(expense_txns)} expense entries</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        bal_class = "green" if net_balance >= 0 else "red"
        bal_icon = "🟢" if net_balance >= 0 else "🔴"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                <span>NET BALANCE</span>
                <span>{bal_icon}</span>
            </div>
            <div class="kpi-value {bal_class}">{format_inr(net_balance)}</div>
            <div class="kpi-subtext">{'Surplus liquidity' if net_balance >= 0 else 'Deficit overdraft'}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                <span>SAVINGS RATE</span>
                <span style="color:#B66DFF; font-size:1rem;">🎯</span>
            </div>
            <div class="kpi-value purple">{savings_rate:.1f}%</div>
            <div class="kpi-subtext">Ratio of income retained</div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # MONTHLY BUDGET PROGRESS BAR
    # ==========================================================================
    if total_budget > 0:
        util_pct, util_status = compute_utilization(total_expenses, total_budget)
        prog_val = min(1.0, max(0.0, total_expenses / total_budget))
        rem_budget = total_budget - total_expenses
        badge_style = "badge-safe" if util_status == "Normal" else ("badge-warning" if util_status == "Spending Awareness" else "badge-danger")

        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1D1733 0%, #151026 100%); border: 1px solid #2E2248; border-radius: 12px; padding: 0.95rem 1.25rem; margin: 0.65rem 0 1.25rem 0; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px; flex-wrap:wrap; gap:8px;">
                <span style="font-weight:600; font-size: 0.88rem; color: #FFFFFF;">
                    Monthly Budget Progress ({eval_month}): <strong>{format_inr(total_expenses)}</strong> of <strong>{format_inr(total_budget)}</strong>
                </span>
                <span class="{badge_style}">
                    {util_status} ({util_pct:.1f}%)
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(prog_val)
        rem_color = "#35D49A" if rem_budget >= 0 else "#FF5478"
        st.caption(f"Remaining budget allocation: <strong style='color:{rem_color};'>{format_inr(rem_budget)}</strong>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================================
    # BALANCED TWO-COLUMN DASHBOARD LAYOUT
    # Left:  Cash Flow Chart + Active Spending Alerts
    # Right: Expense Category Donut + Recent Transactions
    # ==========================================================================
    col_left, col_right = st.columns([1, 1], gap="medium")

    # --------------------------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------------------------
    with col_left:
        # 1. CASH FLOW: INCOME VS EXPENSE (Grouped Bar Chart)
        st.markdown("""
        <div class="dashboard-card" style="margin-bottom:1.25rem;">
            <div class="card-header-title">
                <h3>📊 Cash Flow: Income vs. Expense</h3>
                <span class="card-header-badge">Grouped Bar Analysis</span>
            </div>
        """, unsafe_allow_html=True)

        fig_cf = go.Figure()

        # If All Time selected with multiple months, display timeline progression
        if selected_period == "All Time" and len(available_months) > 1:
            recent_months = available_months[-5:]
            x_labels = [datetime.strptime(m, "%Y-%m").strftime("%b %y") for m in recent_months]
            inc_vals = []
            exp_vals = []
            for m in recent_months:
                m_txns = filter_transactions_by_month(transactions, m)
                m_sum = get_financial_summary(m_txns)
                inc_vals.append(m_sum["total_income"])
                exp_vals.append(m_sum["total_expenses"])

            fig_cf.add_trace(go.Bar(
                name="Income",
                x=x_labels,
                y=inc_vals,
                marker=dict(
                    color="#35D49A",
                    line=dict(color="rgba(53, 212, 154, 0.7)", width=1.5),
                    cornerradius=6
                ),
                text=[format_inr(v) for v in inc_vals],
                textposition="auto",
                textfont=dict(family="JetBrains Mono", size=10, color="#FFFFFF"),
                hovertemplate="<b>%{x}</b><br>Income: ₹%{y:,.2f}<extra></extra>"
            ))
            fig_cf.add_trace(go.Bar(
                name="Expenses",
                x=x_labels,
                y=exp_vals,
                marker=dict(
                    color="#FF5478",
                    line=dict(color="rgba(255, 84, 120, 0.7)", width=1.5),
                    cornerradius=6
                ),
                text=[format_inr(v) for v in exp_vals],
                textposition="auto",
                textfont=dict(family="JetBrains Mono", size=10, color="#FFFFFF"),
                hovertemplate="<b>%{x}</b><br>Expenses: ₹%{y:,.2f}<extra></extra>"
            ))
        else:
            # Single evaluation period comparison
            fig_cf.add_trace(go.Bar(
                name="Income",
                x=["Current Flow"],
                y=[total_income],
                marker=dict(
                    color="#35D49A",
                    line=dict(color="rgba(53, 212, 154, 0.7)", width=1.5),
                    cornerradius=8
                ),
                text=[format_inr(total_income)],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#35D49A"),
                hovertemplate="<b>Income</b><br>Amount: ₹%{y:,.2f}<extra></extra>"
            ))
            fig_cf.add_trace(go.Bar(
                name="Expenses",
                x=["Current Flow"],
                y=[total_expenses],
                marker=dict(
                    color="#FF5478",
                    line=dict(color="rgba(255, 84, 120, 0.7)", width=1.5),
                    cornerradius=8
                ),
                text=[format_inr(total_expenses)],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color="#FF5478"),
                hovertemplate="<b>Expenses</b><br>Amount: ₹%{y:,.2f}<extra></extra>"
            ))

        fig_cf.update_layout(
            barmode="group",
            bargap=0.25,
            bargroupgap=0.1,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#A69BBE", size=11),
            yaxis=dict(
                gridcolor="rgba(46, 34, 72, 0.5)",
                zerolinecolor="rgba(46, 34, 72, 0.8)",
                tickfont=dict(family="JetBrains Mono", size=10, color="#7B7192"),
                tickprefix="₹"
            ),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(family="Plus Jakarta Sans", size=11, color="#FFFFFF")
            ),
            height=320,
            margin=dict(l=15, r=15, t=35, b=25),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11, color="#FFFFFF"),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_cf, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # 2. ACTIVE SPENDING ALERTS
        alerts = get_budget_alerts(category_budgets, cat_expenses, total_budget, total_expenses)
        alert_count_badge = f"{len(alerts)} Active Alerts" if alerts else "0 Alerts • Healthy"

        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-header-title">
                <h3>🔔 Active Spending Alerts</h3>
                <span class="card-header-badge">{alert_count_badge}</span>
            </div>
        """, unsafe_allow_html=True)

        if not alerts:
            st.markdown("""
            <div style="background: rgba(53, 212, 154, 0.08); border-left: 4px solid #35D49A; border-radius: 10px; padding: 1.15rem; color: #FFFFFF; font-size: 0.88rem; line-height: 1.5;">
                <strong style="color: #35D49A;">✅ All Limits Healthy:</strong> All category expenditures and the monthly aggregate budget are operating below the 70.0% threshold. Discretionary burn-rate is stable.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Render up to 4 prioritized alerts
            for al in alerts[:4]:
                cat = al["category"]
                status = al["status"]
                util_pct = al.get("utilization_pct")
                msg = al["message"]
                meta = _get_severity_meta(status)
                cat_icon = CATEGORY_ICONS.get(cat, "📦")

                # Compute remaining budget
                if cat == "Overall Budget":
                    budget_val = total_budget
                    spent_val = total_expenses
                else:
                    budget_val = category_budgets.get(cat, 0.0)
                    spent_val = cat_expenses.get(cat, 0.0)
                rem_val = budget_val - spent_val

                rem_text = f"Remaining: {format_inr(rem_val)}" if rem_val >= 0 else f"Deficit: {format_inr(abs(rem_val))}"
                rem_color = "#35D49A" if rem_val >= 0 else "#FF5478"
                util_str = f"{util_pct:.1f}% Utilized" if util_pct is not None else "Unbudgeted"

                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #251B40 0%, #1D1733 100%); border: 1px solid rgba(182, 109, 255, 0.15); border-left: 4px solid {meta['color']}; border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 0.65rem; box-shadow: 0 4px 14px rgba(0,0,0,0.25);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                        <div style="display:flex; align-items:center; gap:7px;">
                            <span style="font-size:1.1rem;">{cat_icon}</span>
                            <strong style="color:#FFFFFF; font-size:0.9rem;">{cat}</strong>
                        </div>
                        <span style="background:{meta['color']}22; color:{meta['color']}; border:1px solid {meta['color']}55; padding:2px 8px; border-radius:6px; font-size:0.72rem; font-weight:700;">
                            {meta['icon']} {meta['badge']}
                        </span>
                    </div>
                    <div style="font-size:0.8rem; color:#A69BBE; margin: 4px 0 8px 0; line-height:1.4;">
                        {msg}
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(46, 34, 72, 0.6); padding-top:6px; font-size:0.75rem;">
                        <span style="color:#B66DFF; font-weight:600;">📊 {util_str}</span>
                        <span style="color:{rem_color}; font-weight:700; font-family:JetBrains Mono;">{rem_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------------------------
    with col_right:
        # 1. EXPENSE CATEGORY SHARE (Donut Chart with Center Total)
        st.markdown("""
        <div class="dashboard-card" style="margin-bottom:1.25rem;">
            <div class="card-header-title">
                <h3>🍩 Expense Category Share</h3>
                <span class="card-header-badge">Proportional Breakdown</span>
            </div>
        """, unsafe_allow_html=True)

        cat_data = [{"Category": cat, "Amount": amt} for cat, amt in cat_expenses.items() if amt > 0]
        if cat_data:
            # Luxury Fintech balanced color sequence
            fintech_colors = ["#9147FF", "#B66DFF", "#38BDF8", "#35D49A", "#FFB547", "#FF5478", "#E879F9"]

            fig_donut = go.Figure(data=[go.Pie(
                labels=[f"{CATEGORY_ICONS.get(c['Category'], '📦')} {c['Category']}" for c in cat_data],
                values=[c["Amount"] for c in cat_data],
                hole=0.68,
                marker=dict(
                    colors=fintech_colors,
                    line=dict(color="#1D1733", width=2.5)
                ),
                textinfo="percent",
                textposition="inside",
                insidetextfont=dict(family="JetBrains Mono", size=10, color="#FFFFFF"),
                hovertemplate="<b>%{label}</b><br>Expenditure: ₹%{value:,.2f}<br>Category Share: %{percent}<extra></extra>"
            )])

            # Center Annotation: Total Expenditure
            fig_donut.update_layout(
                annotations=[
                    dict(
                        text=f"<span style='font-size:0.68rem; color:#A69BBE; font-weight:700; letter-spacing:0.06em; text-transform:uppercase;'>TOTAL SPENT</span><br><b style='font-size:1.2rem; color:#FFFFFF; font-family:JetBrains Mono;'>{format_inr(total_expenses)}</b>",
                        x=0.5,
                        y=0.5,
                        showarrow=False
                    )
                ],
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", color="#FFFFFF"),
                height=320,
                margin=dict(l=15, r=15, t=15, b=25),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.24,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10, color="#A69BBE"),
                    bgcolor="rgba(0,0,0,0)"
                )
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No expense transactions recorded in this period to display category breakdown.")

        st.markdown("</div>", unsafe_allow_html=True)

        # 2. RECENT TRANSACTIONS FEED
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header-title">
                <h3>📑 Recent Transactions</h3>
                <span class="card-header-badge">Latest 5 Entries</span>
            </div>
        """, unsafe_allow_html=True)

        recent_txns = sorted(active_txns, key=lambda x: x.get("date", ""), reverse=True)[:5]

        if not recent_txns:
            st.info("No recent transactions recorded.")
        else:
            for t in recent_txns:
                is_inc = t.get("type") == "Income"
                sign = "+" if is_inc else "-"
                amt_color = "#35D49A" if is_inc else "#FF5478"
                badge_bg = "rgba(53, 212, 154, 0.15)" if is_inc else "rgba(255, 84, 120, 0.15)"
                badge_text = "Income" if is_inc else "Expense"
                cat_name = t.get("category", "Others")
                cat_icon = CATEGORY_ICONS.get(cat_name, "💳")
                desc = t.get("description", "").strip() or cat_name
                dt_str = t.get("date", "")
                mode = t.get("payment_mode", "Cash")

                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #251B40 0%, #1D1733 100%); border: 1px solid #2E2248; border-radius: 11px; padding: 0.65rem 0.85rem; margin-bottom: 0.55rem; display: flex; align-items: center; justify-content: space-between; gap: 10px; transition: transform 0.2s ease;">
                    <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1;">
                        <div style="width:36px; height:36px; border-radius:9px; background:rgba(145, 71, 255, 0.14); border:1px solid rgba(182, 109, 255, 0.25); display:flex; align-items:center; justify-content:center; font-size:1.15rem; flex-shrink:0;">
                            {cat_icon}
                        </div>
                        <div style="min-width:0; flex:1;">
                            <div style="display:flex; align-items:center; gap:6px;">
                                <span style="font-weight:700; font-size:0.86rem; color:#FFFFFF; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{desc}</span>
                                <span style="background:{badge_bg}; color:{amt_color}; font-size:0.65rem; font-weight:700; padding:1px 6px; border-radius:4px; flex-shrink:0;">{badge_text}</span>
                            </div>
                            <div style="font-size:0.72rem; color:#A69BBE; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                {dt_str} • {mode} • {cat_name}
                            </div>
                        </div>
                    </div>
                    <div style="font-size:0.95rem; font-weight:800; color:{amt_color}; font-family:JetBrains Mono; white-space:nowrap; flex-shrink:0;">
                        {sign} {format_inr(t.get('amount', 0))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # View All Transactions Button with seamless router override
            st.markdown("<div style='margin-top:0.75rem;'>", unsafe_allow_html=True)
            if st.button("📋 View All Transactions →", use_container_width=True, key="btn_view_all_txns"):
                st.session_state["nav_override"] = "All Transactions"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
