"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/intelligence_engine.py
Description: Smart Budget Intelligence Engine. Computes average daily burn rate,
             month-end expenditure forecasts, safe-to-spend daily limits,
             rule-based overspending risk indices, and actionable guidance.
Assigned Contribution: HARSH (S26CSEU1935)
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import calendar
from datetime import datetime, date
from config import EXPENSE_CATEGORIES
from modules.calc_engine import format_inr, filter_transactions_by_month, calculate_category_expenses
from modules.budget_engine import compute_utilization, rank_spending_categories, calculate_remaining_budget


# ==============================================================================
# 1. DATE & CALENDAR CONTEXT HANDLER
# ==============================================================================

def get_month_calendar_context(year_month: str, as_of_date: date = None) -> dict:
    """
    Computes elapsed days, total days in month, and remaining days.
    Handles leap years (e.g., February 2024 vs February 2025/2026) using calendar.monthrange.
    Distinguishes historical (past), current, and future months.

    Args:
        year_month (str): Format 'YYYY-MM'.
        as_of_date (date, optional): Reference date (defaults to today).

    Returns:
        dict: {
            'year': int,
            'month': int,
            'month_name': str,
            'total_days': int,
            'elapsed_days': int,
            'remaining_days': int,
            'is_current': bool,
            'is_past': bool,
            'is_future': bool
        }
    """
    if as_of_date is None:
        as_of_date = date.today()

    try:
        parts = year_month.split("-")
        yr = int(parts[0])
        mo = int(parts[1])
    except (ValueError, IndexError):
        yr = as_of_date.year
        mo = as_of_date.month

    # calendar.monthrange returns (first_weekday, num_days_in_month)
    # Correctly handles leap years for February automatically!
    _, total_days = calendar.monthrange(yr, mo)
    month_name = calendar.month_name[mo]

    current_yr = as_of_date.year
    current_mo = as_of_date.month
    current_day = as_of_date.day

    # Determine timeline relationship
    if (yr < current_yr) or (yr == current_yr and mo < current_mo):
        # Past (historical) month: completely elapsed
        is_past = True
        is_current = False
        is_future = False
        elapsed_days = total_days
        remaining_days = 0

    elif yr == current_yr and mo == current_mo:
        # Current active month
        is_past = False
        is_current = True
        is_future = False
        elapsed_days = min(current_day, total_days)
        # Remaining days includes today
        remaining_days = max(1, total_days - elapsed_days + 1)

    else:
        # Future month: not yet started
        is_past = False
        is_current = False
        is_future = True
        elapsed_days = 0
        remaining_days = total_days

    return {
        "year": yr,
        "month": mo,
        "month_name": month_name,
        "total_days": total_days,
        "elapsed_days": elapsed_days,
        "remaining_days": remaining_days,
        "is_current": is_current,
        "is_past": is_past,
        "is_future": is_future
    }


# ==============================================================================
# 2. CORE MATHEMATICAL FORMULAS
# ==============================================================================

def calculate_average_daily_spending(month_expenses: float, elapsed_days: int) -> float:
    """
    Formula A: Average Daily Spending
        Average Daily Spending = Month-to-date Expenses / Elapsed Days

    If elapsed_days is 0 or expenses are negative/0, returns 0.0.
    """
    try:
        exp = float(month_expenses)
        days = int(elapsed_days)
    except (ValueError, TypeError):
        return 0.0

    if exp <= 0 or days <= 0:
        return 0.0

    return round(exp / days, 2)


def calculate_monthly_forecast(avg_daily_spend: float, total_days_in_month: int) -> float:
    """
    Formula B: Month-End Expense Forecast
        Projected Monthly Expenses = Average Daily Spending × Total Days in Month
    """
    try:
        daily = float(avg_daily_spend)
        total_days = int(total_days_in_month)
    except (ValueError, TypeError):
        return 0.0

    if daily <= 0 or total_days <= 0:
        return 0.0

    return round(daily * total_days, 2)


def calculate_projected_overspending(projected_expenses: float, monthly_budget: float) -> float:
    """
    Formula C: Projected Overspending Amount
        Projected Overspending = max(0, Projected Expenses - Monthly Budget)

    If projected expenses <= budget, returns 0.0.
    """
    try:
        proj = float(projected_expenses)
        bud = float(monthly_budget)
    except (ValueError, TypeError):
        return 0.0

    if bud <= 0:
        # If no budget was set, the entire projected expense is technically unbudgeted
        return round(proj, 2) if proj > 0 else 0.0

    variance = proj - bud
    return round(max(0.0, variance), 2)


def calculate_safe_daily_spending(monthly_budget: float, month_expenses: float, remaining_days: int) -> float:
    """
    Formula D: Safe Daily Spending Limit
        Remaining Budget = Monthly Budget - Month-to-date Expenses
        Safe Daily Spending = Remaining Budget / Remaining Days

    Rule:
      When the budget has already been exceeded (Remaining Budget <= 0),
      safe daily spending must strictly be 0.0.
      If remaining_days <= 0, returns 0.0.
    """
    try:
        bud = float(monthly_budget)
        exp = float(month_expenses)
        days = int(remaining_days)
    except (ValueError, TypeError):
        return 0.0

    remaining_budget = bud - exp

    # Strict rule: Budget already exhausted or no remaining days -> ₹0.0/day
    if remaining_budget <= 0.0 or days <= 0:
        return 0.0

    return round(remaining_budget / days, 2)


def calculate_overspending_risk_index(projected_expenses: float, monthly_budget: float) -> tuple:
    """
    Formula E: Overspending Risk Index
        Risk Index = (Projected Monthly Expenses / Monthly Budget) × 100
        Clamped between 0 and 100.

    Risk Levels:
      - 0 to 69:   "Low Risk"
      - 70 to 89:  "Moderate Risk"
      - 90 to 99:  "High Risk"
      - 100:       "Critical Risk"

    Note for Viva:
      This is a deterministic, rule-based computational indicator of projected
      budget utilization, NOT a statistical probability of financial loss.

    Returns:
        tuple: (score: int, level_label: str, description: str, color_code: str)
    """
    try:
        proj = float(projected_expenses)
        bud = float(monthly_budget)
    except (ValueError, TypeError):
        return (0, "Low Risk", "Insufficient data.", "#10B981")

    # Edge Case: No budget set
    if bud <= 0:
        if proj <= 0:
            return (0, "Low Risk", "No budget allocated and zero expenses.", "#10B981")
        else:
            return (100, "Critical Risk", "Spending is occurring without an allocated budget limit.", "#EF4444")

    # Compute raw ratio
    raw_ratio = (proj / bud) * 100.0

    # Clamp between 0 and 100
    score = int(round(raw_ratio))
    score = min(100, max(0, score))

    if score < 70:
        level = "Low Risk"
        desc = "Current spending trajectory is healthy and well within monthly allocation."
        color = "#10B981"  # Emerald Green
    elif score < 90:
        level = "Moderate Risk"
        desc = "Projected run-rate is entering caution territory (70%–89%). Moderate discretionary expenses."
        color = "#F59E0B"  # Amber Yellow
    elif score < 100:
        level = "High Risk"
        desc = "Projected run-rate is approaching budget exhaustion (90%–99%). Strict spending pacing required."
        color = "#F97316"  # Orange
    else:  # score == 100
        level = "Critical Risk"
        desc = "Projected run-rate meets or exceeds 100% of total monthly budget. Action needed immediately."
        color = "#EF4444"  # Crimson Red

    return (score, level, desc, color)


# ==============================================================================
# 3. SMART RECOMMENDATIONS GENERATOR
# ==============================================================================

def generate_smart_recommendations(intelligence: dict) -> list:
    """
    Generates plain-language, transparent recommendations based on
    computational metrics, category statuses, and safe spending limits.

    Args:
        intelligence (dict): Dictionary produced by generate_budget_intelligence().

    Returns:
        list of str: Actionable advice for the user.
    """
    recommendations = []
    cal = intelligence["calendar"]
    total_budget = intelligence["total_budget"]
    total_expenses = intelligence["total_expenses"]
    safe_daily = intelligence["safe_daily_spending"]
    projected_overspending = intelligence["projected_overspending"]
    risk_level = intelligence["risk_level"]
    ranked_cats = intelligence["ranked_categories"]

    # 1. Historical month guidance
    if cal["is_past"]:
        if total_budget > 0:
            if total_expenses <= total_budget:
                surplus = total_budget - total_expenses
                recommendations.append(
                    f"🎉 Excellent financial control! In {cal['month_name']} {cal['year']}, you finished with a surplus of {format_inr(surplus)}."
                )
            else:
                deficit = total_expenses - total_budget
                recommendations.append(
                    f"⚠️ In {cal['month_name']} {cal['year']}, total spending exceeded budget by {format_inr(deficit)}. Review top categories below to plan upcoming months."
                )
        return recommendations

    # 2. Current Month Budget Health
    if total_budget <= 0:
        recommendations.append(
            "💡 You have not set an overall budget for this month. Set a planned budget in the 'Budget Management' tab to unlock active alerts and daily safe limits."
        )
    elif total_expenses > total_budget:
        deficit = total_expenses - total_budget
        recommendations.append(
            f"🚨 Budget Breached: You have overspent by {format_inr(deficit)}. Freeze non-essential purchases for the remaining {cal['remaining_days']} days."
        )
    elif projected_overspending > 0:
        recommendations.append(
            f"⚠️ Pace Warning: At your current daily burn rate ({format_inr(intelligence['avg_daily_spending'])}/day), you are projected to overshoot your budget by {format_inr(projected_overspending)}."
        )
    else:
        recommendations.append(
            f"✅ Spending On Track: Your safe daily spending limit is {format_inr(safe_daily)}/day for the remaining {cal['remaining_days']} days of {cal['month_name']}."
        )

    # 3. Category-Specific Insights
    warning_or_exceeded = [c for c in ranked_cats if c["status"] in ["Spending Awareness", "High Spending Warning", "Budget Exceeded"]]

    for c in warning_or_exceeded[:3]:
        cat_name = c["category"]
        util = c["utilization_pct"]
        spent = c["spent"]
        budget = c["budget"]

        if c["status"] == "Budget Exceeded":
            over = spent - budget
            recommendations.append(
                f"🛑 {cat_name}: Over budget by {format_inr(over)} ({util:.1f}%). Pause all non-mandatory {cat_name} expenses."
            )
        elif c["status"] == "High Spending Warning":
            rem = budget - spent
            recommendations.append(
                f"🟠 {cat_name}: High utilization at {util:.1f}%. Only {format_inr(rem)} remaining for the next {cal['remaining_days']} days."
            )
        elif c["status"] == "Spending Awareness":
            recommendations.append(
                f"🟡 {cat_name}: Reached {util:.1f}% utilization. Monitor spending pace closely."
            )

    # 4. Top Category Share Insight
    if ranked_cats and ranked_cats[0]["spent"] > 0:
        top_cat = ranked_cats[0]
        recommendations.append(
            f"📊 '{top_cat['category']}' is your largest expense category, accounting for {top_cat['share_of_total_pct']}% ({format_inr(top_cat['spent'])}) of your total spending this month."
        )

    return recommendations


# ==============================================================================
# 4. MASTER CONSOLIDATED INTELLIGENCE ORCHESTRATOR
# ==============================================================================

def generate_budget_intelligence(year_month: str, transactions: list, budget_data: dict, as_of_date: date = None) -> dict:
    """
    Central pipeline that runs all mathematical calculations, budget audits,
    and forecasts for the requested month.

    Args:
        year_month (str): Target month in 'YYYY-MM'.
        transactions (list): Full list of user transactions.
        budget_data (dict): Budget configuration dictionary for the month.
        as_of_date (date, optional): Reference date for tests/simulation.

    Returns:
        dict: Complete intelligence package ready for visualization.
    """
    cal = get_month_calendar_context(year_month, as_of_date)

    # Filter to transactions in the target month and EXCLUDE Income (expenses only)
    month_txns = filter_transactions_by_month(transactions, year_month)
    expense_txns = [t for t in month_txns if t.get("type") == "Expense"]
    total_expenses = sum(t["amount"] for t in expense_txns)

    # Extract budget
    total_budget = float(budget_data.get("monthly_total", 0.0))
    category_budgets = budget_data.get("categories", {})

    # Compute category-level expenses
    cat_expenses = calculate_category_expenses(expense_txns)

    # 1. Average Daily Spending
    if cal["is_past"]:
        # Historical month: average across full month
        avg_daily_spending = calculate_average_daily_spending(total_expenses, cal["total_days"])
        projected_expenses = total_expenses  # No future projection for past months!
    elif cal["is_future"]:
        avg_daily_spending = 0.0
        projected_expenses = 0.0
    else:
        # Current active month
        avg_daily_spending = calculate_average_daily_spending(total_expenses, cal["elapsed_days"])
        projected_expenses = calculate_monthly_forecast(avg_daily_spending, cal["total_days"])

    # 2. Projected Overspending & Variance
    projected_overspending = calculate_projected_overspending(projected_expenses, total_budget)
    projected_variance = round(total_budget - projected_expenses, 2) if total_budget > 0 else 0.0

    # 3. Safe Daily Spending Limit
    if cal["is_past"]:
        safe_daily_spending = 0.0
    else:
        safe_daily_spending = calculate_safe_daily_spending(total_budget, total_expenses, cal["remaining_days"])

    # 4. Overall Utilization
    overall_utilization, overall_status = compute_utilization(total_expenses, total_budget)

    # 5. Overspending Risk Index
    risk_score, risk_level, risk_desc, risk_color = calculate_overspending_risk_index(projected_expenses, total_budget)

    # 6. Ranked Categories
    ranked_cats = rank_spending_categories(cat_expenses, category_budgets)

    # Assemble Result Object
    intelligence = {
        "year_month": year_month,
        "calendar": cal,
        "total_budget": total_budget,
        "total_expenses": round(total_expenses, 2),
        "overall_utilization": overall_utilization,
        "overall_status": overall_status,
        "avg_daily_spending": avg_daily_spending,
        "projected_expenses": projected_expenses,
        "projected_overspending": projected_overspending,
        "projected_variance": projected_variance,
        "safe_daily_spending": safe_daily_spending,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_desc": risk_desc,
        "risk_color": risk_color,
        "category_budgets": category_budgets,
        "category_expenses": cat_expenses,
        "ranked_categories": ranked_cats
    }

    # Generate Plain-Language Recommendations
    intelligence["recommendations"] = generate_smart_recommendations(intelligence)

    return intelligence
