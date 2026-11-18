"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/budget_engine.py
Description: Advanced Budget Monitoring and Alert Threshold Logic.
             Assigned Contribution: HARSH (S26CSEU1935)
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

from config import (
    THRESHOLD_SAFE,      # 0.70 (70%)
    THRESHOLD_WARNING,   # 0.90 (90%)
    THRESHOLD_CRITICAL,  # 1.00 (100%)
    EXPENSE_CATEGORIES
)
from modules.calc_engine import format_inr


# ==============================================================================
# 1. BUDGET UTILIZATION & STATUS CLASSIFICATION
# ==============================================================================

def compute_utilization(spent: float, budget: float) -> tuple:
    """
    Computes budget utilization percentage and classifies into alert tiers.

    Exact Thresholds:
      - Below 70%: "Normal"
      - 70% to below 90%: "Spending Awareness"
      - 90% to below 100%: "High Spending Warning"
      - 100% or above: "Budget Exceeded"

    Special Edge Cases:
      - budget == 0 and spent == 0 -> (0.0, "Unbudgeted")
      - budget == 0 and spent > 0  -> (None, "Unbudgeted Spend")
      - spent < 0                  -> clamped to 0.0

    Args:
        spent (float): Incurred expenditure in ₹.
        budget (float): Allocated budget in ₹.

    Returns:
        tuple: (utilization_pct: float or None, status_label: str)
    """
    try:
        s = float(spent)
        b = float(budget)
    except (ValueError, TypeError):
        return (0.0, "Normal")

    if s < 0:
        s = 0.0

    # Case 1: No budget set
    if b <= 0.0:
        if s == 0.0:
            return (0.0, "Unbudgeted")
        else:
            return (None, "Unbudgeted Spend")

    # Case 2: Budget is positive (> 0.0)
    utilization_pct = (s / b) * 100.0

    # Categorize against exact threshold boundaries
    if utilization_pct < (THRESHOLD_SAFE * 100.0):       # < 70%
        status = "Normal"
    elif utilization_pct < (THRESHOLD_WARNING * 100.0):   # 70% <= util < 90%
        status = "Spending Awareness"
    elif utilization_pct < (THRESHOLD_CRITICAL * 100.0):  # 90% <= util < 100%
        status = "High Spending Warning"
    else:                                                 # >= 100%
        status = "Budget Exceeded"

    return (round(utilization_pct, 2), status)


# ==============================================================================
# 2. REMAINING BUDGET CALCULATION
# ==============================================================================

def calculate_remaining_budget(budget: float, spent: float) -> float:
    """
    Calculates remaining budget allowance.
    Can return negative values if expenditure has exceeded allocation.

    Formula:
        Remaining = Budget - Spent

    Args:
        budget (float): Allocated budget in ₹.
        spent (float): Incurred expenditure in ₹.

    Returns:
        float: Remaining amount in ₹ (negative if overspent).
    """
    try:
        b = float(budget)
        s = float(spent)
    except (ValueError, TypeError):
        return 0.0
    return round(b - s, 2)


# ==============================================================================
# 3. CATEGORY BUDGET CHECKER
# ==============================================================================

def check_category_budget(category: str, spent: float, budget: float) -> dict:
    """
    Performs a full audit of an individual category's budget status.

    Args:
        category (str): Name of the expense category.
        spent (float): Amount spent in ₹.
        budget (float): Budget limit in ₹.

    Returns:
        dict: Detailed category health assessment:
              {
                  'category': str,
                  'spent': float,
                  'budget': float,
                  'remaining': float,
                  'utilization_pct': float or None,
                  'status': str,
                  'status_code': str, # 'normal', 'awareness', 'warning', 'exceeded', 'unbudgeted'
                  'alert_message': str,
                  'badge_color': str
              }
    """
    utilization_pct, status = compute_utilization(spent, budget)
    remaining = calculate_remaining_budget(budget, spent)

    # Determine status code, color badge, and conversational alert message
    if status == "Normal":
        status_code = "normal"
        badge_color = "#10B981"  # Emerald Green
        alert_msg = f"{category} spending is within safe limits ({utilization_pct:.1f}% used). Remaining: {format_inr(remaining)}."

    elif status == "Spending Awareness":
        status_code = "awareness"
        badge_color = "#F59E0B"  # Amber Yellow
        alert_msg = f"Spending Awareness: {category} has reached {utilization_pct:.1f}% of budget. Consider moderating expenses."

    elif status == "High Spending Warning":
        status_code = "warning"
        badge_color = "#F97316"  # Orange
        alert_msg = f"High Spending Warning: {category} is at {utilization_pct:.1f}% utilization! Only {format_inr(remaining)} left before limit."

    elif status == "Budget Exceeded":
        status_code = "exceeded"
        badge_color = "#EF4444"  # Crimson Red
        overspent = abs(remaining)
        alert_msg = f"Budget Exceeded: {category} is over budget by {format_inr(overspent)} ({utilization_pct:.1f}% used)!"

    elif status == "Unbudgeted Spend":
        status_code = "unbudgeted"
        badge_color = "#64748B"  # Slate Gray
        alert_msg = f"{category} has expenses of {format_inr(spent)} but no allocated budget was set."

    else:  # "Unbudgeted" (0 spent, 0 budget)
        status_code = "unbudgeted"
        badge_color = "#64748B"
        alert_msg = f"No budget allocated for {category}."

    return {
        "category": category,
        "spent": round(float(spent), 2),
        "budget": round(float(budget), 2),
        "remaining": remaining,
        "utilization_pct": utilization_pct,
        "status": status,
        "status_code": status_code,
        "alert_message": alert_msg,
        "badge_color": badge_color
    }


# ==============================================================================
# 4. COMPREHENSIVE BUDGET ALERTS GENERATOR
# ==============================================================================

def get_budget_alerts(category_budgets: dict, category_expenses: dict, total_budget: float, total_expenses: float) -> list:
    """
    Evaluates both overall monthly budget and all individual categories to
    generate prioritized alert cards.

    Priority Ordering:
      1. Overall Budget Exceeded / Warning
      2. Category Budget Exceeded
      3. Category High Spending Warning
      4. Category Spending Awareness
      5. Unbudgeted Spend with notable expenses

    Args:
        category_budgets (dict): {cat_name: budget_amount}
        category_expenses (dict): {cat_name: spent_amount}
        total_budget (float): Total monthly budget in ₹.
        total_expenses (float): Total incurred expenses in ₹.

    Returns:
        list of dict: Ordered alert cards with severity, category, message, and metrics.
    """
    alerts = []

    # 1. Overall Monthly Budget Evaluation
    if total_budget > 0:
        overall_util, overall_status = compute_utilization(total_expenses, total_budget)
        remaining_total = total_budget - total_expenses

        if overall_status == "Budget Exceeded":
            alerts.append({
                "scope": "Overall Monthly Budget",
                "category": "Overall Budget",
                "severity": "CRITICAL",
                "status": overall_status,
                "utilization_pct": overall_util,
                "message": f"🚨 Monthly Budget Exceeded! You have spent {format_inr(total_expenses)} out of {format_inr(total_budget)} ({overall_util:.1f}%). Deficit: {format_inr(abs(remaining_total))}.",
                "color": "#EF4444"
            })
        elif overall_status == "High Spending Warning":
            alerts.append({
                "scope": "Overall Monthly Budget",
                "category": "Overall Budget",
                "severity": "HIGH",
                "status": overall_status,
                "utilization_pct": overall_util,
                "message": f"⚠️ High Monthly Spending: {overall_util:.1f}% of overall monthly budget consumed. Remaining liquidity: {format_inr(remaining_total)}.",
                "color": "#F97316"
            })
        elif overall_status == "Spending Awareness":
            alerts.append({
                "scope": "Overall Monthly Budget",
                "category": "Overall Budget",
                "severity": "MEDIUM",
                "status": overall_status,
                "utilization_pct": overall_util,
                "message": f"ℹ️ Spending Awareness: You have utilized {overall_util:.1f}% of your monthly budget. Remaining: {format_inr(remaining_total)}.",
                "color": "#F59E0B"
            })

    # 2. Individual Category Evaluations
    for cat in EXPENSE_CATEGORIES:
        spent = category_expenses.get(cat, 0.0)
        budget = category_budgets.get(cat, 0.0)
        audit = check_category_budget(cat, spent, budget)

        if audit["status"] == "Budget Exceeded":
            alerts.append({
                "scope": "Category",
                "category": cat,
                "severity": "CRITICAL",
                "status": audit["status"],
                "utilization_pct": audit["utilization_pct"],
                "message": audit["alert_message"],
                "color": audit["badge_color"]
            })
        elif audit["status"] == "High Spending Warning":
            alerts.append({
                "scope": "Category",
                "category": cat,
                "severity": "HIGH",
                "status": audit["status"],
                "utilization_pct": audit["utilization_pct"],
                "message": audit["alert_message"],
                "color": audit["badge_color"]
            })
        elif audit["status"] == "Spending Awareness":
            alerts.append({
                "scope": "Category",
                "category": cat,
                "severity": "MEDIUM",
                "status": audit["status"],
                "utilization_pct": audit["utilization_pct"],
                "message": audit["alert_message"],
                "color": audit["badge_color"]
            })
        elif audit["status"] == "Unbudgeted Spend" and spent >= 500.0:
            alerts.append({
                "scope": "Category",
                "category": cat,
                "severity": "LOW",
                "status": audit["status"],
                "utilization_pct": None,
                "message": audit["alert_message"],
                "color": audit["badge_color"]
            })

    return alerts


# ==============================================================================
# 5. CATEGORY EXPENDITURE RANKING
# ==============================================================================

def rank_spending_categories(category_expenses: dict, category_budgets: dict = None) -> list:
    """
    Ranks expense categories by expenditure in descending order (highest spending first).
    Includes allocated budget, utilization percentage, status, and share of total expenses.

    Args:
        category_expenses (dict): {category_name: spent_amount}
        category_budgets (dict, optional): {category_name: budget_amount}

    Returns:
        list of dict: Ranked categories with metrics:
        [
            {
                'rank': 1,
                'category': 'Food',
                'spent': 4500.0,
                'budget': 7000.0,
                'remaining': 2500.0,
                'utilization_pct': 64.29,
                'status': 'Normal',
                'share_of_total_pct': 38.5
            },
            ...
        ]
    """
    if category_budgets is None:
        category_budgets = {}

    total_spent = sum(category_expenses.values())
    ranked = []

    for cat in EXPENSE_CATEGORIES:
        spent = float(category_expenses.get(cat, 0.0))
        budget = float(category_budgets.get(cat, 0.0))
        utilization_pct, status = compute_utilization(spent, budget)
        remaining = calculate_remaining_budget(budget, spent)
        share_pct = (spent / total_spent * 100.0) if total_spent > 0 else 0.0

        ranked.append({
            "category": cat,
            "spent": round(spent, 2),
            "budget": round(budget, 2),
            "remaining": remaining,
            "utilization_pct": utilization_pct,
            "status": status,
            "share_of_total_pct": round(share_pct, 1)
        })

    # Sort descending by spent amount
    ranked.sort(key=lambda item: item["spent"], reverse=True)

    # Assign 1-based rank
    for idx, item in enumerate(ranked, start=1):
        item["rank"] = idx

    return ranked
