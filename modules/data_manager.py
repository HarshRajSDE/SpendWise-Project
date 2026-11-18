"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/data_manager.py
Description: Data Persistence Layer with Dual-Mode Support:
             1. Multi-User Mode: Strict row-level SQLite database isolation per
                authenticated Bennett University team member.
             2. Legacy/Test Mode: Direct CSV/JSON file operations for unit testing
                and historical file export/backup.
================================================================================
"""

import os
import csv
import json
import uuid
import shutil
import io
from datetime import datetime
from typing import Optional, List, Dict, Any

from config import (
    TRANSACTIONS_FILE,
    BUDGET_FILE,
    BACKUPS_DIR,
    TRANSACTION_CSV_HEADERS,
    EXPENSE_CATEGORIES
)
from modules.database import (
    init_db,
    add_user_transaction,
    get_user_transactions,
    get_user_transaction_by_id,
    update_user_transaction,
    delete_user_transaction,
    clear_user_transactions,
    clear_user_budgets,
    delete_user_demo_transactions,
    get_user_demo_transaction_count,
    get_user_monthly_budget,
    set_user_monthly_budget,
    get_user_all_budgets
)


def _resolve_user_id(user_id: Optional[int] = None) -> Optional[int]:
    """
    Resolves the active user ID either from an explicit parameter or
    from Streamlit's authenticated session state.
    Returns None when executing outside of a logged-in user context (e.g. unit tests).
    """
    if user_id is not None:
        return user_id
    try:
        import streamlit as st
        if "user" in st.session_state and isinstance(st.session_state["user"], dict):
            return st.session_state["user"].get("id")
    except Exception:
        pass
    return None


# ==============================================================================
# 1. FILE & DATABASE INITIALIZATION
# ==============================================================================

def init_data_files():
    """
    Ensures both SQLite multi-user database and legacy CSV/JSON files exist on disk.
    """
    init_db()

    # Initialize empty CSV file if missing (for tests/legacy)
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(TRANSACTION_CSV_HEADERS)

    # Initialize empty JSON file if missing
    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, mode="w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)


# ==============================================================================
# 2. TRANSACTION MANAGEMENT (USER-ISOLATED SQLITE + LEGACY CSV FALLBACK)
# ==============================================================================

def load_transactions(user_id: Optional[int] = None) -> list:
    """
    Reads transactions.
    - If user_id is resolved: queries SQLite for ONLY that user's records.
    - Otherwise (legacy / test harness): reads from CSV.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        return get_user_transactions(uid)

    # Legacy / Test Fallback
    init_data_files()
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row or "id" not in row or not row.get("id"):
                    continue
                try:
                    amount_val = float(row.get("amount", 0.0))
                except (ValueError, TypeError):
                    amount_val = 0.0

                transactions.append({
                    "id": str(row.get("id", "")).strip(),
                    "date": str(row.get("date", "")).strip(),
                    "type": str(row.get("type", "Expense")).strip(),
                    "category": str(row.get("category", "Others")).strip(),
                    "amount": round(amount_val, 2),
                    "payment_mode": str(row.get("payment_mode", "UPI")).strip(),
                    "description": str(row.get("description", "")).strip()
                })
    except Exception as error:
        print(f"[SpendWise DataManager] Error reading transactions CSV: {error}")
        return []

    return transactions


def save_transactions(transactions: list) -> bool:
    """
    Overwrites the entire transactions.csv file (Legacy/Test support).
    """
    try:
        with open(TRANSACTIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=TRANSACTION_CSV_HEADERS)
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    "id": t.get("id"),
                    "date": t.get("date"),
                    "type": t.get("type"),
                    "category": t.get("category"),
                    "amount": f"{float(t.get('amount', 0.0)):.2f}",
                    "payment_mode": t.get("payment_mode"),
                    "description": t.get("description", "")
                })
        return True
    except Exception as error:
        print(f"[SpendWise DataManager] Error saving transactions: {error}")
        return False


def add_transaction(transaction: dict, user_id: Optional[int] = None) -> bool:
    """
    Appends a single transaction.
    - If user_id is resolved: stores in SQLite owned by user_id.
    - Otherwise: appends to CSV.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        success, _ = add_user_transaction(
            user_id=uid,
            t_date=str(transaction.get("date", "")),
            t_type=str(transaction.get("type", "Expense")),
            category=str(transaction.get("category", "Others")),
            amount=float(transaction.get("amount", 0.0)),
            payment_mode=str(transaction.get("payment_mode", "UPI")),
            description=str(transaction.get("description", ""))
        )
        return success

    # Legacy / Test CSV Append
    init_data_files()
    if not transaction.get("id"):
        transaction["id"] = str(uuid.uuid4())[:8]

    try:
        amount_val = float(transaction.get("amount", 0.0))
        if amount_val <= 0:
            return False
        transaction["amount"] = f"{amount_val:.2f}"
    except (ValueError, TypeError):
        return False

    try:
        with open(TRANSACTIONS_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=TRANSACTION_CSV_HEADERS)
            writer.writerow({
                "id": transaction.get("id"),
                "date": transaction.get("date"),
                "type": transaction.get("type"),
                "category": transaction.get("category"),
                "amount": transaction.get("amount"),
                "payment_mode": transaction.get("payment_mode"),
                "description": transaction.get("description", "")
            })
        return True
    except Exception as error:
        print(f"[SpendWise DataManager] Error appending transaction: {error}")
        return False


def delete_transaction(transaction_id: str, user_id: Optional[int] = None) -> bool:
    """
    Deletes a transaction by ID.
    Enforces user_id ownership check when authenticated.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        return delete_user_transaction(uid, transaction_id)

    # Legacy / Test Mode
    transactions = load_transactions()
    initial_count = len(transactions)
    updated_transactions = [t for t in transactions if t.get("id") != transaction_id]
    if len(updated_transactions) == initial_count:
        return False
    return save_transactions(updated_transactions)


def update_transaction(updated_txn: dict, user_id: Optional[int] = None) -> bool:
    """
    Updates an existing transaction by ID.
    Enforces user_id ownership check when authenticated.
    """
    target_id = updated_txn.get("id")
    if not target_id:
        return False

    uid = _resolve_user_id(user_id)
    if uid is not None:
        success, _ = update_user_transaction(
            user_id=uid,
            txn_id=target_id,
            t_date=str(updated_txn.get("date", "")),
            t_type=str(updated_txn.get("type", "Expense")),
            category=str(updated_txn.get("category", "Others")),
            amount=float(updated_txn.get("amount", 0.0)),
            payment_mode=str(updated_txn.get("payment_mode", "UPI")),
            description=str(updated_txn.get("description", ""))
        )
        return success

    # Legacy / Test Mode
    transactions = load_transactions()
    found = False
    for i, t in enumerate(transactions):
        if t.get("id") == target_id:
            try:
                amt_val = float(updated_txn.get("amount", t.get("amount", 0.0)))
                if amt_val <= 0:
                    return False
            except (ValueError, TypeError):
                return False

            transactions[i] = {
                "id": target_id,
                "date": str(updated_txn.get("date", t.get("date"))),
                "type": str(updated_txn.get("type", t.get("type"))),
                "category": str(updated_txn.get("category", t.get("category"))),
                "amount": round(amt_val, 2),
                "payment_mode": str(updated_txn.get("payment_mode", t.get("payment_mode"))),
                "description": str(updated_txn.get("description", t.get("description", ""))).strip()
            }
            found = True
            break

    if not found:
        return False
    return save_transactions(transactions)


# ==============================================================================
# 3. BUDGET CONFIGURATION MANAGEMENT
# ==============================================================================

def load_budget(user_id: Optional[int] = None) -> dict:
    """
    Reads budget configurations for the resolved user or from JSON file.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        return get_user_all_budgets(uid)

    # Legacy / Test Mode
    init_data_files()
    try:
        with open(BUDGET_FILE, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except Exception as error:
        print(f"[SpendWise DataManager] Error reading budget JSON: {error}")
        return {}


def save_budget(budget_data: dict) -> bool:
    """Saves entire budget dictionary to budget.json (Legacy/Test support)."""
    try:
        with open(BUDGET_FILE, mode="w", encoding="utf-8") as file:
            json.dump(budget_data, file, indent=4)
        return True
    except Exception as error:
        print(f"[SpendWise DataManager] Error writing budget JSON: {error}")
        return False


def get_monthly_budget(year_month: str, user_id: Optional[int] = None) -> dict:
    """
    Fetches the budget allocated for a specific month for the resolved user.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        b_data = get_user_monthly_budget(uid, year_month)
        # Ensure all defined expense categories are populated
        complete_cats = {}
        for cat in EXPENSE_CATEGORIES:
            complete_cats[cat] = float(b_data.get("categories", {}).get(cat, 0.0))
        return {
            "monthly_total": b_data.get("monthly_total", sum(complete_cats.values())),
            "categories": complete_cats
        }

    # Legacy / Test Mode
    all_budgets = load_budget()
    if year_month in all_budgets:
        data = all_budgets[year_month]
        categories = data.get("categories", {})
        complete_categories = {cat: float(categories.get(cat, 0.0)) for cat in EXPENSE_CATEGORIES}
        monthly_total = float(data.get("monthly_total", sum(complete_categories.values())))
        return {
            "monthly_total": monthly_total,
            "categories": complete_categories
        }

    return {
        "monthly_total": 0.0,
        "categories": {cat: 0.0 for cat in EXPENSE_CATEGORIES}
    }


def set_monthly_budget(year_month: str, category_budgets: dict, total_budget: float = None, user_id: Optional[int] = None) -> bool:
    """
    Saves or updates the budget for a specific month for the resolved user.
    """
    clean_categories = {}
    for cat in EXPENSE_CATEGORIES:
        try:
            clean_categories[cat] = round(float(category_budgets.get(cat, 0.0)), 2)
        except (ValueError, TypeError):
            clean_categories[cat] = 0.0

    if total_budget is None or float(total_budget) <= 0:
        total_budget = sum(clean_categories.values())
    else:
        total_budget = round(float(total_budget), 2)

    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        return set_user_monthly_budget(uid, year_month, total_budget, clean_categories)

    # Legacy / Test Mode
    all_budgets = load_budget()
    all_budgets[year_month] = {
        "monthly_total": total_budget,
        "categories": clean_categories
    }
    return save_budget(all_budgets)


# ==============================================================================
# 4. BACKUP, EXPORT & RESET UTILITIES
# ==============================================================================

def backup_data() -> dict:
    """Creates a timestamped snapshot of transactions and budget files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(BACKUPS_DIR, exist_ok=True)

    csv_backup = os.path.join(BACKUPS_DIR, f"transactions_{timestamp}.csv")
    json_backup = os.path.join(BACKUPS_DIR, f"budget_{timestamp}.json")

    try:
        if os.path.exists(TRANSACTIONS_FILE):
            shutil.copy2(TRANSACTIONS_FILE, csv_backup)
        if os.path.exists(BUDGET_FILE):
            shutil.copy2(BUDGET_FILE, json_backup)
        return {
            "success": True,
            "timestamp": timestamp,
            "csv_backup": csv_backup,
            "json_backup": json_backup
        }
    except Exception as error:
        return {"success": False, "error": str(error)}


def clear_all_data(user_id: Optional[int] = None) -> bool:
    """
    Clears data.
    - If user_id is resolved: clears ONLY that user's transactions and budgets from SQLite.
    - Otherwise (test mode): clears CSV and JSON.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        init_db()
        backup_data()
        clear_user_transactions(uid)
        clear_user_budgets(uid)
        return True

    # Legacy / Test Mode
    backup_data()
    try:
        with open(TRANSACTIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(TRANSACTION_CSV_HEADERS)
        with open(BUDGET_FILE, mode="w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)
        return True
    except Exception as error:
        print(f"[SpendWise DataManager] Error clearing data: {error}")
        return False


def export_transactions_csv(user_id: Optional[int] = None) -> str:
    """
    Returns transactions as a CSV string.
    - If user_id is resolved: generates CSV of ONLY that user's transactions.
    - Otherwise: reads raw transactions.csv.
    """
    uid = _resolve_user_id(user_id)
    if uid is not None:
        user_txns = get_user_transactions(uid)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=TRANSACTION_CSV_HEADERS)
        writer.writeheader()
        for t in user_txns:
            writer.writerow({
                "id": t.get("id"),
                "date": t.get("date"),
                "type": t.get("type"),
                "category": t.get("category"),
                "amount": f"{float(t.get('amount', 0.0)):.2f}",
                "payment_mode": t.get("payment_mode"),
                "description": t.get("description", "")
            })
        return output.getvalue()

    init_data_files()
    try:
        with open(TRANSACTIONS_FILE, mode="r", encoding="utf-8") as file:
            return file.read()
    except Exception as error:
        return ""
