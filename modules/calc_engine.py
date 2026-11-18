"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/calc_engine.py
Description: Core Financial Calculation Engine. Computes total income,
             expenditure, net balance, savings rate, category subtotals,
             and handles Indian Rupee (INR ₹) currency formatting.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

from datetime import datetime
from config import EXPENSE_CATEGORIES


# ==============================================================================
# 1. INDIAN RUPEE (INR ₹) CURRENCY FORMATTER
# ==============================================================================

def format_inr(amount: float, include_symbol: bool = True) -> str:
    """
    Formats a numeric float into standard Indian Rupee notation.
    In the Indian numbering system, the last 3 digits are grouped,
    and subsequent higher groupings are by 2 digits (e.g., ₹12,34,567.89).

    Args:
        amount (float): The monetary value to format.
        include_symbol (bool): Whether to prepend the '₹' symbol.

    Returns:
        str: Beautifully formatted INR currency string.
    """
    try:
        val = float(amount)
    except (ValueError, TypeError):
        val = 0.0

    is_negative = val < 0
    val = abs(val)

    # Separate integer and decimal portions
    int_part = int(val)
    decimal_part = f"{val - int_part:.2f}"[1:]  # e.g., ".50"

    s = str(int_part)
    if len(s) <= 3:
        formatted_int = s
    else:
        # Group last 3 digits, then every 2 digits to the left
        last_three = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ",".join(groups) + "," + last_three

    result = f"{formatted_int}{decimal_part}"

    if include_symbol:
        result = f"₹{result}"

    if is_negative:
        result = f"-{result}"

    return result


# ==============================================================================
# 2. CORE FINANCIAL CALCULATIONS
# ==============================================================================

def calculate_total_income(transactions: list) -> float:
    """
    Calculates total income from a list of transaction dictionaries.
    
    Formula:
        Total Income = Sum of amounts where type == 'Income'
    """
    total = 0.0
    for txn in transactions:
        if txn.get("type") == "Income":
            try:
                total += float(txn.get("amount", 0.0))
            except (ValueError, TypeError):
                continue
    return round(total, 2)


def calculate_total_expenses(transactions: list) -> float:
    """
    Calculates total expenses from a list of transaction dictionaries.
    
    Formula:
        Total Expenses = Sum of amounts where type == 'Expense'
    """
    total = 0.0
    for txn in transactions:
        if txn.get("type") == "Expense":
            try:
                total += float(txn.get("amount", 0.0))
            except (ValueError, TypeError):
                continue
    return round(total, 2)


def calculate_net_balance(total_income: float, total_expenses: float) -> float:
    """
    Calculates remaining net balance.
    
    Formula:
        Balance = Total Income - Total Expenses
    """
    return round(float(total_income) - float(total_expenses), 2)


def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    """
    Calculates savings rate as a percentage of total income.
    Handles zero-income edge cases gracefully to avoid ZeroDivisionError.
    
    Formula:
        Savings Rate (%) = ((Income - Expenses) / Income) * 100
        If Income <= 0, returns 0.0%
    """
    try:
        inc = float(total_income)
        exp = float(total_expenses)
    except (ValueError, TypeError):
        return 0.0

    if inc <= 0:
        return 0.0

    balance = inc - exp
    rate = (balance / inc) * 100.0
    return round(rate, 2)


def get_financial_summary(transactions: list) -> dict:
    """
    Generates a consolidated summary dictionary containing all primary metrics.
    
    Returns:
        dict: {
            'total_income': float,
            'total_expenses': float,
            'net_balance': float,
            'savings_rate': float,
            'transaction_count': int
        }
    """
    income = calculate_total_income(transactions)
    expenses = calculate_total_expenses(transactions)
    balance = calculate_net_balance(income, expenses)
    savings_rate = calculate_savings_rate(income, expenses)

    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": balance,
        "savings_rate": savings_rate,
        "transaction_count": len(transactions)
    }


# ==============================================================================
# 3. CATEGORY-WISE AGGREGATIONS
# ==============================================================================

def calculate_category_expenses(transactions: list) -> dict:
    """
    Computes total expenditure grouped by category.
    Initializes all official categories to 0.0 to guarantee complete datasets.
    
    Returns:
        dict: Mapping category name to total spent in ₹.
    """
    category_totals = {cat: 0.0 for cat in EXPENSE_CATEGORIES}

    for txn in transactions:
        if txn.get("type") == "Expense":
            cat = txn.get("category", "Others")
            try:
                amt = float(txn.get("amount", 0.0))
            except (ValueError, TypeError):
                amt = 0.0

            if cat not in category_totals:
                category_totals[cat] = 0.0
            category_totals[cat] += amt

    # Round all values to 2 decimal places
    for cat in category_totals:
        category_totals[cat] = round(category_totals[cat], 2)

    return category_totals


def calculate_category_breakdown(transactions: list) -> list:
    """
    Produces a detailed list of categories with spent amount and share percentage.
    
    Returns:
        list of dicts sorted from highest to lowest spending:
        [
            {'category': 'Food', 'amount': 3500.0, 'percentage': 35.0},
            ...
        ]
    """
    cat_expenses = calculate_category_expenses(transactions)
    total_spent = sum(cat_expenses.values())

    breakdown = []
    for cat, amt in cat_expenses.items():
        if amt > 0:
            pct = (amt / total_spent * 100.0) if total_spent > 0 else 0.0
            breakdown.append({
                "category": cat,
                "amount": amt,
                "percentage": round(pct, 1)
            })

    # Sort descending by spent amount
    breakdown.sort(key=lambda item: item["amount"], reverse=True)
    return breakdown


# ==============================================================================
# 4. DATE AND MONTH FILTERING
# ==============================================================================

def filter_transactions_by_month(transactions: list, year_month: str) -> list:
    """
    Filters transactions belonging to a specific calendar month.
    
    Args:
        transactions (list): All transactions.
        year_month (str): Target month in 'YYYY-MM' format (e.g., '2026-11').
        
    Returns:
        list: Filtered transactions.
    """
    filtered = []
    for txn in transactions:
        date_str = txn.get("date", "")
        # Date string is expected in format 'YYYY-MM-DD'
        if date_str.startswith(year_month):
            filtered.append(txn)
    return filtered


def get_available_months(transactions: list) -> list:
    """
    Extracts all unique months present in the transaction history,
    sorted in descending chronological order (newest first).
    
    Returns:
        list: List of 'YYYY-MM' strings. If none exist, returns current month.
    """
    months = set()
    for txn in transactions:
        d = txn.get("date", "")
        if len(d) >= 7 and d[4] == "-":
            months.add(d[:7])

    current_ym = datetime.now().strftime("%Y-%m")
    months.add(current_ym)

    return sorted(list(months), reverse=True)
