"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/sample_data.py
Description: Demo / Sample Dataset Seeder. Contains realistic, clearly-labelled
             sample financial data for college demonstrations and viva evaluation.
             NOTE: This is NEVER loaded automatically; it is only activated when
             the user explicitly clicks 'Load Demo Data'.
================================================================================
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from modules.data_manager import save_transactions, set_monthly_budget, backup_data, _resolve_user_id
from modules.database import (
    batch_add_user_transactions,
    set_user_monthly_budget,
    get_user_demo_transaction_count,
    delete_user_demo_transactions,
    init_db
)


def get_sample_transactions() -> list:
    """
    Generates a rich, realistic list of sample transactions formatted in INR (₹).
    Spans the active current month and the previous month to demonstrate
    trends, category distributions, and budget alerts.
    """
    now = datetime.now()
    cur_year = now.year
    cur_month = now.month

    # Helper to generate formatted date strings in current month
    def make_date(day: int, month_offset: int = 0) -> str:
        target_month = cur_month - month_offset
        target_year = cur_year
        if target_month <= 0:
            target_month += 12
            target_year -= 1
        return f"{target_year:04d}-{target_month:02d}-{day:02d}"

    # Sample transaction list (Income and Expenses across all official categories)
    sample_records = [
        # --- Income Entries ---
        {
            "id": "TXN-IN-01",
            "date": make_date(1),
            "type": "Income",
            "category": "Salary",
            "amount": 45000.00,
            "payment_mode": "Net Banking",
            "description": "Monthly Salary Stipend"
        },
        {
            "id": "TXN-IN-02",
            "date": make_date(10),
            "type": "Income",
            "category": "Freelance / Gig",
            "amount": 8500.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Website Design Project for College Club"
        },
        {
            "id": "TXN-IN-03",
            "date": make_date(15),
            "type": "Income",
            "category": "Allowance / Pocket Money",
            "amount": 5000.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Parental Allowance"
        },

        # --- Expense Entries: Food (Demonstrating healthy progress) ---
        {
            "id": "TXN-EX-01",
            "date": make_date(2),
            "type": "Expense",
            "category": "Food",
            "amount": 1850.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Weekly Grocery at D-Mart"
        },
        {
            "id": "TXN-EX-02",
            "date": make_date(5),
            "type": "Expense",
            "category": "Food",
            "amount": 420.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Campus Canteen Lunch with Friends"
        },
        {
            "id": "TXN-EX-03",
            "date": make_date(8),
            "type": "Expense",
            "category": "Food",
            "amount": 950.00,
            "payment_mode": "Debit Card",
            "description": "Dinner at Cafe Coffee Day"
        },
        {
            "id": "TXN-EX-04",
            "date": make_date(12),
            "type": "Expense",
            "category": "Food",
            "amount": 680.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Zomato Weekend Dinner Order"
        },

        # --- Expense Entries: Transport ---
        {
            "id": "TXN-EX-05",
            "date": make_date(3),
            "type": "Expense",
            "category": "Transport",
            "amount": 1200.00,
            "payment_mode": "Debit Card",
            "description": "Metro Smart Card Monthly Recharge"
        },
        {
            "id": "TXN-EX-06",
            "date": make_date(9),
            "type": "Expense",
            "category": "Transport",
            "amount": 450.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Ola Auto to University Campus"
        },

        # --- Expense Entries: Education ---
        {
            "id": "TXN-EX-07",
            "date": make_date(4),
            "type": "Expense",
            "category": "Education",
            "amount": 2400.00,
            "payment_mode": "Net Banking",
            "description": "Semester Reference Textbooks & Lab Manual"
        },
        {
            "id": "TXN-EX-08",
            "date": make_date(11),
            "type": "Expense",
            "category": "Education",
            "amount": 699.00,
            "payment_mode": "Credit Card",
            "description": "Online Python & Algorithms Course Subscription"
        },

        # --- Expense Entries: Bills ---
        {
            "id": "TXN-EX-09",
            "date": make_date(5),
            "type": "Expense",
            "category": "Bills",
            "amount": 1499.00,
            "payment_mode": "Net Banking",
            "description": "Fiber Broadband Internet Bill"
        },
        {
            "id": "TXN-EX-10",
            "date": make_date(6),
            "type": "Expense",
            "category": "Bills",
            "amount": 850.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Mobile Prepaid Recharge (3 Months)"
        },

        # --- Expense Entries: Shopping (High utilization demo) ---
        {
            "id": "TXN-EX-11",
            "date": make_date(7),
            "type": "Expense",
            "category": "Shopping",
            "amount": 3200.00,
            "payment_mode": "Credit Card",
            "description": "Winter Jacket & Casual Wear"
        },
        {
            "id": "TXN-EX-12",
            "date": make_date(13),
            "type": "Expense",
            "category": "Shopping",
            "amount": 1350.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Wireless Mouse and Desk Pad"
        },

        # --- Expense Entries: Entertainment ---
        {
            "id": "TXN-EX-13",
            "date": make_date(8),
            "type": "Expense",
            "category": "Entertainment",
            "amount": 750.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "IMAX Movie Tickets with Project Team"
        },
        {
            "id": "TXN-EX-14",
            "date": make_date(14),
            "type": "Expense",
            "category": "Entertainment",
            "amount": 299.00,
            "payment_mode": "UPI (GPay / PhonePe / Paytm)",
            "description": "Music Streaming Family Subscription"
        },

        # --- Expense Entries: Others ---
        {
            "id": "TXN-EX-15",
            "date": make_date(10),
            "type": "Expense",
            "category": "Others",
            "amount": 350.00,
            "payment_mode": "Cash",
            "description": "Laundry and Dry Cleaning"
        }
    ]

    return sample_records


def get_sample_budget_config() -> dict:
    """
    Provides a balanced budget allocation for the 7 official expense categories.
    Total planned monthly budget: ₹25,000.
    """
    return {
        "Food": 7000.00,
        "Transport": 3000.00,
        "Shopping": 5000.00,
        "Education": 4000.00,
        "Entertainment": 2000.00,
        "Bills": 3000.00,
        "Others": 1000.00
    }


def has_sample_dataset(user_id: Optional[int] = None) -> int:
    """
    Checks if sample demo data is currently loaded for the resolved user.
    Returns the count of demo transactions.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        return get_user_demo_transaction_count(uid)
    return 0


def remove_user_sample_dataset(user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Safely removes ONLY the demo transactions belonging to the resolved user.
    All genuine personal transactions are 100% preserved.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        deleted = delete_user_demo_transactions(uid)
        return {"status": "success", "deleted": deleted}
    return {"status": "success", "deleted": 0}


def load_sample_dataset(user_id: Optional[int] = None, replace_existing: bool = True) -> dict:
    """
    Safely seeds the application with sample transactions and budget.
    - If user_id is resolved (Multi-User Mode):
      Stores records in SQLite under user_id with is_demo=1.
      Strict row-level isolation guarantees demo data is only visible to this user.
      If replace_existing is False and demo records already exist, informs the caller.
    - If user_id is None (Legacy / Bare Test Mode):
      Saves to CSV and JSON for test harness compatibility.

    Returns:
        dict: Summary of seeded records and status.
    """
    # 1. Protect existing data by backing up
    backup_data()

    current_ym = datetime.now().strftime("%Y-%m")
    sample_txns = get_sample_transactions()
    sample_budget = get_sample_budget_config()

    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        existing_demo = get_user_demo_transaction_count(uid)
        if existing_demo > 0:
            if not replace_existing:
                return {
                    "status": "already_exists",
                    "count": existing_demo,
                    "transactions_loaded": 0,
                    "month_configured": current_ym,
                    "total_budget": 25000.00
                }
            # Clean previous demo records for this user before reload
            delete_user_demo_transactions(uid)

        # Batch insert sample transactions strictly owned by this user
        loaded_count = batch_add_user_transactions(uid, sample_txns, is_demo=1)

        # Set user's personal monthly budget in SQLite
        set_user_monthly_budget(uid, current_ym, 25000.00, sample_budget)

        return {
            "status": "success",
            "transactions_loaded": loaded_count,
            "month_configured": current_ym,
            "total_budget": 25000.00
        }

    # Legacy / Bare Test Fallback Mode
    save_transactions(sample_txns)
    set_monthly_budget(current_ym, sample_budget, total_budget=25000.00)

    return {
        "status": "success",
        "transactions_loaded": len(sample_txns),
        "month_configured": current_ym,
        "total_budget": 25000.00
    }
