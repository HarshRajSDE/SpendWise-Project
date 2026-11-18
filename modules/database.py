"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/database.py
Description: Production SQLite Database Architecture for Multi-User Personal
             Finance Platform. Implements strict row-level user ownership,
             PBKDF2-HMAC-SHA256 password security, audit logging, and legacy
             data isolation.
Academic Roster Source: Personal_Expense_Budget_Tracker_Project_Report_Printable.docx
Institution: Bennett University (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import os
import sqlite3
import hashlib
import hmac
import json
import uuid
import csv
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

from config import DATA_DIR, EXPENSE_CATEGORIES, INCOME_CATEGORIES

DB_PATH = os.path.join(DATA_DIR, "spendwise.db")

# Authorized Team Roster directly extracted from Project Report
OFFICIAL_TEAM_ROSTER = [
    {
        "full_name": "Ridhima",
        "enrollment_no": "S26CSEU1925",
        "role": "member",
        "default_pin": "Ridhima@1925",
        "contribution": "Project coordination and expense-tracking workflow."
    },
    {
        "full_name": "Anoushka",
        "enrollment_no": "S26CSEU1922",
        "role": "member",
        "default_pin": "Anoushka@1922",
        "contribution": "Project documentation and organization of report content."
    },
    {
        "full_name": "AATIRTH",
        "enrollment_no": "S26CSEU1913",
        "role": "member",
        "default_pin": "Aatirth@1913",
        "contribution": "Transaction data handling and calculation logic."
    },
    {
        "full_name": "HARSH",
        "enrollment_no": "S26CSEU1935",
        "role": "admin",
        "default_pin": "Harsh@1935",
        "contribution": "Budget monitoring and alert logic (Assigned Lead)."
    },
    {
        "full_name": "SRISHTHI",
        "enrollment_no": "S26CSEU1939",
        "role": "member",
        "default_pin": "Srishthi@1939",
        "contribution": "Spending analysis and visualization/reporting."
    }
]


# ==============================================================================
# 1. CRYPTOGRAPHIC SECURITY (PBKDF2-HMAC-SHA256)
# ==============================================================================

def hash_password(password: str) -> str:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with 260,000 iterations
    and a 16-byte cryptographically secure random salt.
    Format: salt_hex$hash_hex
    """
    salt = os.urandom(16)
    pwd_bytes = password.encode("utf-8")
    key = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, 260000)
    return f"{salt.hex()}${key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verifies a plaintext password against a stored PBKDF2 hash using constant-time comparison.
    """
    try:
        salt_hex, key_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        pwd_bytes = password.encode("utf-8")
        computed_key = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt, 260000)
        return hmac.compare_digest(expected_key, computed_key)
    except Exception:
        return False


# ==============================================================================
# 2. DATABASE CONNECTION & INITIALIZATION
# ==============================================================================

def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with WAL mode, busy timeout, foreign keys enabled, and row factory set."""
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes all multi-user tables, foreign key constraints, indexes,
    seeds default categories, and seeds the 5 official Bennett University team accounts.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_no TEXT UNIQUE NOT NULL COLLATE NOCASE,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'member',  -- 'admin' or 'member'
            is_active INTEGER NOT NULL DEFAULT 1,
            contribution TEXT,
            created_at TEXT NOT NULL,
            last_login TEXT
        );
        """)

        # 2. Transactions Table with strict user ownership and demo tracking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,              -- 'Income' or 'Expense'
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,              -- 'YYYY-MM-DD'
            description TEXT,
            payment_mode TEXT,
            created_at TEXT NOT NULL,
            is_demo INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # Automated schema migration: add is_demo if missing from previous version
        cursor.execute("PRAGMA table_info(transactions);")
        existing_cols = [c[1] for c in cursor.fetchall()]
        if "is_demo" not in existing_cols:
            cursor.execute("ALTER TABLE transactions ADD COLUMN is_demo INTEGER NOT NULL DEFAULT 0;")

        # 3. Budgets Table with strict user ownership & unique per month
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,             -- 'YYYY-MM'
            monthly_total REAL NOT NULL DEFAULT 0.0,
            categories_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, month),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 4. User Settings Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            preferences_json TEXT NOT NULL DEFAULT '{}',
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        # 5. Audit Logs Table (Account Security & Administration)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT DEFAULT '127.0.0.1',
            timestamp TEXT NOT NULL
        );
        """)

        # 6. Legacy Transactions Area (Quarantine for pre-migration unowned data)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS legacy_transactions (
            id TEXT PRIMARY KEY,
            original_data_json TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            assigned_user_id INTEGER,
            FOREIGN KEY(assigned_user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)

        # Indexes for High Performance Querying & Isolation
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_txns_user_date ON transactions(user_id, date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_txns_user_category ON transactions(user_id, category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_txns_user_demo ON transactions(user_id, is_demo);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_budgets_user_month ON budgets(user_id, month);")

        conn.commit()

        # Seed the official team roster if not already present
        now_str = datetime.now().isoformat()
        for member in OFFICIAL_TEAM_ROSTER:
            cursor.execute("SELECT id FROM users WHERE enrollment_no = ?;", (member["enrollment_no"],))
            existing = cursor.fetchone()
            if not existing:
                pwd_hash = hash_password(member["default_pin"])
                cursor.execute("""
                    INSERT INTO users (enrollment_no, full_name, password_hash, role, is_active, contribution, created_at)
                    VALUES (?, ?, ?, ?, 1, ?, ?);
                """, (
                    member["enrollment_no"],
                    member["full_name"],
                    pwd_hash,
                    member["role"],
                    member["contribution"],
                    now_str
                ))
                user_id = cursor.lastrowid
                # Seed default empty settings
                cursor.execute("""
                    INSERT OR IGNORE INTO user_settings (user_id, preferences_json, updated_at)
                    VALUES (?, '{}', ?);
                """, (user_id, now_str))

        conn.commit()
    finally:
        conn.close()


# ==============================================================================
# 3. AUTHENTICATION & USER MANAGEMENT
# ==============================================================================

def validate_login_credentials(
    enrollment_no: str,
    password: str,
    full_name: Optional[str] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Comprehensive credential validator returning (is_valid, user_friendly_message, user_dict).
    Validates enrollment existence, active status, name match (if provided), and PBKDF2 hash.
    """
    enrollment_clean = enrollment_no.strip()
    if not enrollment_clean:
        return False, "Please enter your registered Bennett University Enrollment Number.", None

    if not password:
        return False, "Please enter your account Password or Personal PIN.", None

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, enrollment_no, full_name, password_hash, role, is_active, contribution, created_at
            FROM users
            WHERE enrollment_no = ? COLLATE NOCASE;
        """, (enrollment_clean,))
        row = cursor.fetchone()

        if not row:
            log_audit(None, "LOGIN_FAILED_UNKNOWN_ENROLLMENT", f"Attempted enrollment: {enrollment_clean}")
            return False, f"Enrollment Number '{enrollment_clean}' not found in the course roster.", None

        if not row["is_active"]:
            log_audit(row["id"], "LOGIN_REJECTED_DEACTIVATED", f"User {row['enrollment_no']} is deactivated.")
            return False, "This account has been deactivated. Please contact the project administrator.", None

        # Verify full name if entered
        if full_name and full_name.strip():
            entered_norm = full_name.strip().lower()
            stored_norm = row["full_name"].strip().lower()
            entered_tokens = set(entered_norm.split())
            stored_tokens = set(stored_norm.split())
            if not (entered_tokens & stored_tokens or entered_norm in stored_norm or stored_norm in entered_norm):
                log_audit(row["id"], "LOGIN_FAILED_NAME_MISMATCH", f"Entered: {full_name}, Stored: {row['full_name']}")
                return False, f"Full Name does not match the registered record for {enrollment_clean.upper()}.", None

        # Verify PBKDF2 password hash
        if not verify_password(password, row["password_hash"]):
            log_audit(row["id"], "LOGIN_FAILED_BAD_PASSWORD", f"Bad password for {row['enrollment_no']}.")
            return False, f"Incorrect password or PIN for {enrollment_clean.upper()}.", None

        now_str = datetime.now().isoformat()
        with conn:
            cursor.execute("UPDATE users SET last_login = ? WHERE id = ?;", (now_str, row["id"]))

        user_dict = {
            "id": row["id"],
            "enrollment_no": row["enrollment_no"],
            "full_name": row["full_name"],
            "role": row["role"],
            "is_active": bool(row["is_active"]),
            "contribution": row["contribution"],
            "created_at": row["created_at"],
            "last_login": now_str
        }

        log_audit(row["id"], "LOGIN_SUCCESS", f"User {row['full_name']} ({row['enrollment_no']}) logged in.")
        return True, f"Welcome back, {row['full_name']}!", user_dict
    except Exception as e:
        return False, f"Database authentication error: {str(e)}", None
    finally:
        conn.close()


def authenticate_user(
    enrollment_no: str,
    password: str,
    full_name: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Authenticates a user by enrollment number and password.
    Returns user dict on success, None on failure.
    Updates last_login timestamp and writes an audit log.
    """
    valid, _, user_dict = validate_login_credentials(enrollment_no, password, full_name)
    return user_dict if valid else None

    if not row["is_active"]:
        log_audit(row["id"], "LOGIN_REJECTED_DEACTIVATED", f"User {row['enrollment_no']} is deactivated.")
        conn.close()
        return None

    if not verify_password(password, row["password_hash"]):
        log_audit(row["id"], "LOGIN_FAILED_BAD_PASSWORD", f"Bad password for {row['enrollment_no']}.")
        conn.close()
        return None

    now_str = datetime.now().isoformat()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?;", (now_str, row["id"]))
    conn.commit()

    user_dict = {
        "id": row["id"],
        "enrollment_no": row["enrollment_no"],
        "full_name": row["full_name"],
        "role": row["role"],
        "is_active": bool(row["is_active"]),
        "contribution": row["contribution"],
        "created_at": row["created_at"],
        "last_login": now_str
    }

    log_audit(row["id"], "LOGIN_SUCCESS", f"User {row['full_name']} ({row['enrollment_no']}) logged in.")
    conn.close()
    return user_dict


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches user details by primary key ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, enrollment_no, full_name, role, is_active, contribution, created_at, last_login
        FROM users WHERE id = ?;
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_enrollment(enrollment_no: str) -> Optional[Dict[str, Any]]:
    """Fetches user details by enrollment number."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, enrollment_no, full_name, role, is_active, contribution, created_at, last_login
        FROM users WHERE enrollment_no = ? COLLATE NOCASE;
    """, (enrollment_no.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users() -> List[Dict[str, Any]]:
    """Returns list of all registered team members (without password hashes)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, enrollment_no, full_name, role, is_active, contribution, created_at, last_login
        FROM users ORDER BY id ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_user_password(user_id: int, new_password: str, admin_user_id: Optional[int] = None) -> bool:
    """Updates a user's password with fresh PBKDF2 salt and hash."""
    if not new_password or len(new_password) < 6:
        return False
    pwd_hash = hash_password(new_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?;", (pwd_hash, user_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()

    actor = admin_user_id if admin_user_id is not None else user_id
    log_audit(actor, "PASSWORD_UPDATED", f"Password updated for user_id={user_id}")
    return success


def set_user_active_status(user_id: int, is_active: bool, admin_user_id: int) -> bool:
    """Activates or deactivates an account (Admin only)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_active = ? WHERE id = ?;", (1 if is_active else 0, user_id))
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()

    log_audit(admin_user_id, "USER_STATUS_CHANGE", f"user_id={user_id} active={is_active}")
    return success


def log_audit(user_id: Optional[int], action: str, details: str = ""):
    """Records an audit event in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO audit_logs (user_id, action, details, timestamp)
            VALUES (?, ?, ?, ?);
        """, (user_id, action, details, now_str))
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent system audit logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.user_id, u.full_name, u.enrollment_no, a.action, a.details, a.timestamp
        FROM audit_logs a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.id DESC LIMIT ?;
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==============================================================================
# 4. STRICT USER-ISOLATED TRANSACTION CRUD
# ==============================================================================

def add_user_transaction(
    user_id: int,
    t_date: str,
    t_type: str,
    category: str,
    amount: float,
    payment_mode: str = "UPI (GPay / PhonePe / Paytm)",
    description: str = "",
    is_demo: int = 0,
    txn_id: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Adds a new transaction owned strictly by user_id.
    Validates amount > 0, valid category, and valid date.
    Supports demo tagging via is_demo=1.
    """
    try:
        amt = float(amount)
        if amt <= 0:
            return False, "Amount must be strictly greater than zero."
    except (ValueError, TypeError):
        return False, "Invalid numeric amount provided."

    if t_type not in ("Income", "Expense"):
        return False, "Transaction type must be 'Income' or 'Expense'."

    # Ensure date format
    try:
        datetime.strptime(t_date, "%Y-%m-%d")
    except ValueError:
        return False, "Date must be formatted as YYYY-MM-DD."

    if not txn_id:
        prefix = "demo_" if is_demo else "txn_"
        txn_id = f"{prefix}{uuid.uuid4().hex[:12]}"

    created_at = datetime.now().isoformat()
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO transactions (id, user_id, type, amount, category, date, description, payment_mode, created_at, is_demo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                txn_id,
                user_id,
                t_type,
                round(amt, 2),
                category.strip(),
                t_date,
                description.strip(),
                payment_mode.strip(),
                created_at,
                1 if is_demo else 0
            ))
        log_audit(user_id, "TRANSACTION_ADDED", f"id={txn_id} amt={amt} cat={category} is_demo={is_demo}")
        return True, txn_id
    except Exception as e:
        return False, f"Failed to record transaction: {str(e)}"
    finally:
        conn.close()


def batch_add_user_transactions(
    user_id: int,
    transactions: List[Dict[str, Any]],
    is_demo: int = 0
) -> int:
    """
    Inserts a list of transactions in a single atomic database transaction.
    """
    conn = get_db_connection()
    try:
        now_str = datetime.now().isoformat()
        rows_to_insert = []
        for t in transactions:
            t_id = t.get("id") or (f"demo_{uuid.uuid4().hex[:10]}" if is_demo else f"txn_{uuid.uuid4().hex[:12]}")
            if is_demo and not t_id.startswith("demo_"):
                t_id = f"demo_{uuid.uuid4().hex[:6]}_{t_id}"
            amt = float(t.get("amount", 0.0))
            if amt <= 0:
                continue
            rows_to_insert.append((
                t_id,
                user_id,
                str(t.get("type", "Expense")),
                round(amt, 2),
                str(t.get("category", "Others")).strip(),
                str(t.get("date", datetime.now().strftime("%Y-%m-%d"))),
                str(t.get("description", "")).strip(),
                str(t.get("payment_mode", "UPI")).strip(),
                now_str,
                1 if is_demo else 0
            ))

        with conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT OR REPLACE INTO transactions (id, user_id, type, amount, category, date, description, payment_mode, created_at, is_demo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, rows_to_insert)
            inserted = len(rows_to_insert)

        log_audit(user_id, "BATCH_TRANSACTIONS_ADDED", f"count={inserted} is_demo={is_demo}")
        return inserted
    finally:
        conn.close()


def get_user_transactions(user_id: int) -> List[Dict[str, Any]]:
    """
    Fetches all transactions belonging STRICTLY to user_id.
    Never exposes other users' records.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, type, category, amount, payment_mode, description, is_demo
            FROM transactions
            WHERE user_id = ?
            ORDER BY date DESC, created_at DESC;
        """, (user_id,))
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "date": r["date"],
                "type": r["type"],
                "category": r["category"],
                "amount": float(r["amount"]),
                "payment_mode": r["payment_mode"],
                "description": r["description"] or "",
                "is_demo": bool(r["is_demo"]) if "is_demo" in r.keys() else False
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_user_demo_transaction_count(user_id: int) -> int:
    """Returns the count of demo transactions currently loaded for user_id."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT count(*) FROM transactions
            WHERE user_id = ? AND (is_demo = 1 OR id LIKE 'demo_%');
        """, (user_id,))
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def delete_user_demo_transactions(user_id: int) -> int:
    """
    Safely deletes ONLY demo transactions belonging to user_id.
    All genuine personal transactions are strictly preserved.
    """
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM transactions
                WHERE user_id = ? AND (is_demo = 1 OR id LIKE 'demo_%');
            """, (user_id,))
            deleted = cursor.rowcount
        log_audit(user_id, "DEMO_DATA_REMOVED", f"deleted={deleted}")
        return deleted
    finally:
        conn.close()


def clear_user_budgets(user_id: int) -> int:
    """Clears all budgets belonging exclusively to user_id."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM budgets WHERE user_id = ?;", (user_id,))
            deleted = cursor.rowcount
        log_audit(user_id, "BUDGETS_CLEARED", f"count={deleted}")
        return deleted
    finally:
        conn.close()


def get_user_transaction_by_id(user_id: int, txn_id: str) -> Optional[Dict[str, Any]]:
    """Fetches a single transaction verifying user ownership."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, type, category, amount, payment_mode, description
            FROM transactions
            WHERE user_id = ? AND id = ?;
        """, (user_id, txn_id))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "date": row["date"],
            "type": row["type"],
            "category": row["category"],
            "amount": float(row["amount"]),
            "payment_mode": row["payment_mode"],
            "description": row["description"] or ""
        }
    finally:
        conn.close()


def update_user_transaction(
    user_id: int,
    txn_id: str,
    t_date: str,
    t_type: str,
    category: str,
    amount: float,
    payment_mode: str,
    description: str
) -> Tuple[bool, str]:
    """
    Updates a transaction ONLY if owned by user_id.
    Fails if another user attempts to modify it.
    """
    try:
        amt = float(amount)
        if amt <= 0:
            return False, "Amount must be strictly greater than zero."
    except (ValueError, TypeError):
        return False, "Invalid numeric amount."

    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET date = ?, type = ?, category = ?, amount = ?, payment_mode = ?, description = ?
                WHERE user_id = ? AND id = ?;
            """, (
                t_date,
                t_type,
                category.strip(),
                round(amt, 2),
                payment_mode.strip(),
                description.strip(),
                user_id,
                txn_id
            ))
            affected = cursor.rowcount

        if affected > 0:
            log_audit(user_id, "TRANSACTION_UPDATED", f"id={txn_id}")
            return True, "Transaction updated successfully."
        else:
            log_audit(user_id, "TRANSACTION_UPDATE_UNAUTHORIZED_OR_NOTFOUND", f"id={txn_id}")
            return False, "Transaction not found or access denied."
    except Exception as e:
        return False, f"Failed to update transaction: {str(e)}"
    finally:
        conn.close()


def delete_user_transaction(user_id: int, txn_id: str) -> bool:
    """
    Deletes a transaction ONLY if owned by user_id.
    Fails if unauthorized.
    """
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE user_id = ? AND id = ?;", (user_id, txn_id))
            affected = cursor.rowcount

        if affected > 0:
            log_audit(user_id, "TRANSACTION_DELETED", f"id={txn_id}")
            return True
        return False
    finally:
        conn.close()


def clear_user_transactions(user_id: int) -> int:
    """Deletes all transactions belonging exclusively to user_id."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE user_id = ?;", (user_id,))
            deleted = cursor.rowcount

        log_audit(user_id, "ALL_TRANSACTIONS_CLEARED", f"count={deleted}")
        return deleted
    finally:
        conn.close()


# ==============================================================================
# 5. STRICT USER-ISOLATED BUDGET CRUD
# ==============================================================================

def get_user_monthly_budget(user_id: int, month_str: str) -> Dict[str, Any]:
    """
    Fetches the budget for a specific month belonging strictly to user_id.
    Returns: {'monthly_total': float, 'categories': {cat: float}}
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT monthly_total, categories_json
        FROM budgets
        WHERE user_id = ? AND month = ?;
    """, (user_id, month_str))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"monthly_total": 0.0, "categories": {}}

    try:
        categories = json.loads(row["categories_json"])
    except Exception:
        categories = {}

    return {
        "monthly_total": float(row["monthly_total"]),
        "categories": {cat: float(amt) for cat, amt in categories.items()}
    }


def set_user_monthly_budget(
    user_id: int,
    month_str: str,
    total_budget: float,
    category_budgets: Dict[str, float]
) -> bool:
    """
    Creates or updates a user's personal monthly budget.
    """
    try:
        tot = max(0.0, float(total_budget))
    except (ValueError, TypeError):
        tot = 0.0

    sanitized_cats = {}
    for cat, val in category_budgets.items():
        try:
            amt = max(0.0, float(val))
            sanitized_cats[cat] = round(amt, 2)
        except (ValueError, TypeError):
            continue

    cat_json = json.dumps(sanitized_cats)
    now_str = datetime.now().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (user_id, month, monthly_total, categories_json, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, month) DO UPDATE SET
            monthly_total = excluded.monthly_total,
            categories_json = excluded.categories_json,
            updated_at = excluded.updated_at;
    """, (user_id, month_str, round(tot, 2), cat_json, now_str))
    conn.commit()
    conn.close()

    log_audit(user_id, "BUDGET_UPDATED", f"month={month_str} total={tot}")
    return True


def get_user_all_budgets(user_id: int) -> Dict[str, Dict[str, Any]]:
    """Returns all monthly budgets for user_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT month, monthly_total, categories_json
        FROM budgets
        WHERE user_id = ?
        ORDER BY month DESC;
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    result = {}
    for r in rows:
        try:
            cats = json.loads(r["categories_json"])
        except Exception:
            cats = {}
        result[r["month"]] = {
            "monthly_total": float(r["monthly_total"]),
            "categories": {c: float(v) for c, v in cats.items()}
        }
    return result


# ==============================================================================
# 6. LEGACY DATA MIGRATION & QUARANTINE
# ==============================================================================

def migrate_legacy_csv_and_json(csv_path: str, json_path: str) -> Dict[str, int]:
    """
    Reads legacy CSV transactions and JSON budgets and moves them into
    the legacy quarantine table without assigning them to any random user.
    """
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    imported_txns = 0

    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    txn_id = row.get("id") or f"legacy_{uuid.uuid4().hex[:8]}"
                    # Check if already imported
                    cursor.execute("SELECT id FROM legacy_transactions WHERE id = ?;", (txn_id,))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO legacy_transactions (id, original_data_json, imported_at, assigned_user_id)
                            VALUES (?, ?, ?, NULL);
                        """, (txn_id, json.dumps(row), now_str))
                        imported_txns += 1
            conn.commit()
        except Exception as e:
            print(f"Legacy CSV migration note: {e}")

    conn.close()
    return {"legacy_imported": imported_txns}
