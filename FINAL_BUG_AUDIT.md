# SpendWise – Technical Audit, Bug Fixes & Stability Report
**Document:** `FINAL_BUG_AUDIT.md`  
**Institution:** Bennett University (Times Group)  
**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Academic Year:** 2026–2027  
**System Architecture:** Multi-User Cryptographic Financial Platform (Streamlit, SQLite, Plotly, PBKDF2-HMAC-SHA256)  
**Status:** Completed & Fully Verified (55/55 Unit Tests Passed)  

---

## 1. Executive Summary

A comprehensive, deep-level technical audit and stability refactoring was performed on the SpendWise application. The investigation identified and resolved two critical blockers alongside six hidden architectural and concurrency vulnerabilities.

All 55 automated unit tests across 5 test suites pass with zero failures and zero errors. End-to-end multi-user data isolation, PBKDF2 cryptographic authentication, and isolated sample demo dataset seeding were verified both programmatically and via live browser execution on `http://localhost:8502`.

```text
Ran 55 tests in 1.356s
OK (All Tests Passed - 100% Pass Rate)
```

---

## 2. Issues Discovered & Root Causes

### 🔴 Critical Bug 1: "Load Sample Demo Dataset" Button Failed to Populate Multi-User Dashboard
- **Symptom:** Clicking *"🚀 Load Sample Demo Dataset (INR ₹)"* in the Overview Dashboard or Reports tab flashed a success message, but the dashboard remained completely empty with 0 transactions.
- **Root Cause:** `modules/sample_data.py` was invoking `save_transactions(sample_txns)` and `set_monthly_budget(...)` without passing the resolved `user_id`. `save_transactions()` only wrote to the legacy `data/transactions.csv` file, completely bypassing the SQLite `transactions` table. In multi-user mode, `load_transactions()` queries SQLite strictly with `WHERE user_id = ?`, which returned 0 records because the data was never written to the database under the authenticated user's ID.
- **Resolution:**
  1. Updated `load_sample_dataset(user_id=None, replace_existing=True)` in [`modules/sample_data.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/sample_data.py) to resolve `user_id` via `_resolve_user_id()`.
  2. Implemented `batch_add_user_transactions(uid, sample_txns, is_demo=1)` in [`modules/database.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/database.py) using an atomic SQLite transaction.
  3. Added an `is_demo` tracking column to the `transactions` table with an automated schema migration.
  4. Tagged all demo transactions with `is_demo = 1` and unique identifiers (`demo_...`).
  5. Implemented `has_sample_dataset()`, `get_user_demo_transaction_count()`, and `remove_user_sample_dataset()`.
  6. Added safety controls in [`views/view_reports.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_reports.py) that prompt the user when demo data is already active and provide a safe button to *"Remove Only My Demo Records"*, guaranteeing genuine transactions are never deleted.

---

### 🔴 Critical Bug 2: Login and Authentication Intermittently Failed or Threw Exceptions
- **Symptom:** Authentication sometimes succeeded and sometimes threw unexpected exceptions, dropped active sessions, or failed to update input fields.
- **Root Cause 1 (`app.py` Module Reload Loop):** An `importlib.reload(sys.modules[mod_name])` loop was executing across all modules on every single Streamlit script rerun. In Streamlit's multi-threaded model, reloading modules mid-execution invalidates Python type identities, breaks session state object references, causes race conditions, resets database connection pools, and produces unpredictable `ImportError` or auth drops.
- **Root Cause 2 (`views/view_login.py` Widget Key & Form Handling):**
  - The *"Show Password / PIN"* checkbox was embedded *inside* `st.form("spendwise_login_form")`. Streamlit does not process widget state toggles inside forms until form submission, making the toggle non-responsive.
  - The Quick Select dropdown was not synchronizing with controlled session-state keys, causing text inputs to occasionally retain stale credentials from previous attempts.
  - Full Name input was not verified against the registered student record for the entered enrollment number.
- **Resolution:**
  1. Completely removed the destructive `importlib.reload` loop from [`app.py`](file:///Users/harshraj/Desktop/SpendWise_Project/app.py).
  2. Rebuilt [`views/view_login.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_login.py) with clean session state initialization.
  3. Moved the *"Show Password / PIN"* checkbox outside the form so toggling responds immediately without submitting.
  4. Implemented `validate_login_credentials(enrollment_no, password, full_name)` in [`modules/database.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/database.py), which checks enrollment existence, account activation status, name matching, and PBKDF2 hash verification, returning human-readable, specific error messages.

---

### 🟡 Bug 3: Database Concurrency & SQLite Connection Locking Risks
- **Symptom:** Concurrent reads and writes could trigger `sqlite3.OperationalError: database is locked`.
- **Root Cause:** `get_db_connection()` lacked Write-Ahead Logging (`WAL`) mode and busy timeout settings, and some database functions did not use connection context managers.
- **Resolution:**
  1. Configured `PRAGMA journal_mode = WAL;` and `PRAGMA busy_timeout = 10000;` in `get_db_connection()`.
  2. Increased connection timeout to 15 seconds.
  3. Wrapped all database write operations in `with conn:` context managers with automatic rollback on failure and `conn.close()` inside `finally:` blocks.

---

### 🟡 Bug 4: Hardcoded User Profile in Settings View
- **Symptom:** Regardless of which of the 5 team members was logged in, [`views/view_settings.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_settings.py) always displayed "Harsh Raj" in the user profile card.
- **Root Cause:** Hardcoded strings in `view_settings.py` instead of inspecting `st.session_state["user"]`.
- **Resolution:** Refactored `views/view_settings.py` to dynamically inspect `st.session_state.get("user")`, rendering the active user's full name, initials avatar, role badge, enrollment number, and assigned contribution, while highlighting them in the team collaboration roster with a `"You"` badge.

---

### 🟡 Bug 5: Incomplete Database Reset in Reports & Data
- **Symptom:** Clicking *"Reset All Data to Clean Empty State"* deleted transactions but left configured monthly budgets intact in SQLite.
- **Root Cause:** `clear_all_data()` in `modules/data_manager.py` only called `clear_user_transactions(uid)` and omitted budget deletion.
- **Resolution:** Added `clear_user_budgets(uid)` in `modules/database.py` and called it inside `clear_all_data()`.

---

### 🟡 Bug 6: Demo Data Cross-User Contamination Prevention
- **Symptom:** Risk that demo records loaded by User A might leak or overwrite User B's records.
- **Root Cause:** Previously, demo data did not store user ownership or distinguish demo entries from real entries.
- **Resolution:** Demo data now writes strictly with `user_id = uid` and `is_demo = 1` into SQLite. User A's demo dataset is completely invisible to User B, and User B can independently load or remove their own demo dataset without affecting User A.

---

## 3. Files Modified & Fixes Implemented

| File Path | Nature of Change | Key Improvements Implemented |
| :--- | :---: | :--- |
| [`modules/database.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/database.py) | **Core Database Layer** | Added WAL journal mode & 10s busy timeout; added `is_demo` schema migration & index; implemented `validate_login_credentials`, `batch_add_user_transactions`, `get_user_demo_transaction_count`, `delete_user_demo_transactions`, and `clear_user_budgets`; enforced `with conn:` atomic rollbacks. |
| [`modules/sample_data.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/sample_data.py) | **Demo Seeder** | Implemented multi-user aware `load_sample_dataset()`; added `has_sample_dataset()` and `remove_user_sample_dataset()`; added duplicate load detection (`already_exists`); preserved legacy CSV/JSON fallback for unit tests. |
| [`modules/data_manager.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/data_manager.py) | **Persistence Layer** | Updated `clear_all_data()` to clear both transactions and budgets; imported new database demo functions; preserved dual-mode compatibility. |
| [`app.py`](file:///Users/harshraj/Desktop/SpendWise_Project/app.py) | **Main Controller** | Removed dangerous module reload loop; added idempotent session state initialization; added unique key to logout button with clean session clearing. |
| [`views/view_login.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_login.py) | **Authentication View** | Moved Show/Hide password checkbox outside form; integrated `validate_login_credentials()` with specific human error messages; stabilized Quick Select autofill. |
| [`views/view_reports.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_reports.py) | **Reports View** | Added demo dataset status detection (`has_sample_dataset()`); added *"Reload Demo"* and *"Remove Only My Demo Records"* buttons; added unique widget keys. |
| [`views/view_overview.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_overview.py) | **Overview View** | Added unique key `btn_overview_load_demo` to demo button in empty state; ensured instant population of KPI cards, charts, and transaction feeds. |
| [`views/view_settings.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_settings.py) | **Settings View** | Made user profile card dynamic based on authenticated session state; highlighted active user in collaboration roster. |
| [`tests/test_multi_user.py`](file:///Users/harshraj/Desktop/SpendWise_Project/tests/test_multi_user.py) | **Automated Tests** | Added 4 new test methods: `test_login_name_validation`, `test_sample_demo_dataset_loading_and_isolation`, `test_demo_data_removal_preserves_genuine_transactions`, and `test_multi_user_csv_export_isolation`. |
| [`docs/testing_report.md`](file:///Users/harshraj/Desktop/SpendWise_Project/docs/testing_report.md) | **Documentation** | Updated executive summary and test breakdown tables to reflect 55 passing tests. |
| [`docs/viva_questions_answers.md`](file:///Users/harshraj/Desktop/SpendWise_Project/docs/viva_questions_answers.md) | **Documentation** | Added viva preparation Q&A for multi-user security, row-level isolation, and PBKDF2 cryptography. |

---

## 4. Complete Test Suite Execution Results

Running `.venv/bin/python3 -m unittest discover tests -v`:

```text
test_calculate_remaining_budget (test_budget_engine.TestBudgetEngine) ... ok
test_check_category_budget_details (test_budget_engine.TestBudgetEngine) ... ok
test_get_budget_alerts_prioritization (test_budget_engine.TestBudgetEngine) ... ok
test_rank_spending_categories (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_above_100_is_budget_exceeded (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_below_70_is_normal (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_between_70_and_90 (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_between_90_and_100 (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_exactly_100_is_budget_exceeded (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_exactly_70_is_spending_awareness (test_budget_engine.TestBudgetEngine) ... ok
test_utilization_exactly_90_is_high_spending_warning (test_budget_engine.TestBudgetEngine) ... ok
test_zero_budget_and_positive_expenses_unbudgeted_spend (test_budget_engine.TestBudgetEngine) ... ok
test_zero_budget_and_zero_expenses (test_budget_engine.TestBudgetEngine) ... ok
test_category_expenses_aggregation (test_calculations.TestFinancialCalculations) ... ok
test_format_inr_basic (test_calculations.TestFinancialCalculations) ... ok
test_format_inr_negative (test_calculations.TestFinancialCalculations) ... ok
test_format_inr_small_amount (test_calculations.TestFinancialCalculations) ... ok
test_net_balance (test_calculations.TestFinancialCalculations) ... ok
test_savings_rate_negative_balance (test_calculations.TestFinancialCalculations) ... ok
test_savings_rate_normal (test_calculations.TestFinancialCalculations) ... ok
test_savings_rate_zero_income (test_calculations.TestFinancialCalculations) ... ok
test_total_expenses (test_calculations.TestFinancialCalculations) ... ok
test_total_income (test_calculations.TestFinancialCalculations) ... ok
test_add_and_load_transaction (test_data_manager.TestDataManager) ... ok
test_budget_set_and_get (test_data_manager.TestDataManager) ... ok
test_clear_all_data (test_data_manager.TestDataManager) ... ok
test_delete_transaction (test_data_manager.TestDataManager) ... ok
test_export_and_backup_operations (test_data_manager.TestDataManager) ... ok
test_init_data_files_creates_empty_files (test_data_manager.TestDataManager) ... ok
test_invalid_transaction_amount_rejected (test_data_manager.TestDataManager) ... ok
test_update_transaction (test_data_manager.TestDataManager) ... ok
test_average_daily_spending (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_calendar_context_february_leap_year (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_calendar_context_historical_month (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_generate_budget_intelligence_full_pipeline (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_month_end_forecast (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_projected_overspending (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_risk_index_critical_risk_boundary (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_risk_index_high_risk_boundary (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_risk_index_low_risk_boundary (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_risk_index_moderate_risk_boundary (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_safe_daily_spending_normal (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_safe_daily_spending_when_budget_exceeded (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_safe_daily_spending_zero_remaining_days (test_intelligence_engine.TestIntelligenceEngine) ... ok
test_account_deactivation_blocks_login (test_multi_user.TestMultiUserPlatform) ... ok
test_all_five_official_members_authenticate (test_multi_user.TestMultiUserPlatform) ... ok
test_authentication_invalid_credentials (test_multi_user.TestMultiUserPlatform) ... ok
test_demo_data_removal_preserves_genuine_transactions (test_multi_user.TestMultiUserPlatform) ... ok
test_login_name_validation (test_multi_user.TestMultiUserPlatform) ... ok
test_multi_user_csv_export_isolation (test_multi_user.TestMultiUserPlatform) ... ok
test_password_hashing_and_verification (test_multi_user.TestMultiUserPlatform) ... ok
test_password_update_and_audit_logging (test_multi_user.TestMultiUserPlatform) ... ok
test_row_level_data_isolation_budgets (test_multi_user.TestMultiUserPlatform) ... ok
test_row_level_data_isolation_transactions (test_multi_user.TestMultiUserPlatform) ... ok
test_sample_demo_dataset_loading_and_isolation (test_multi_user.TestMultiUserPlatform) ... ok

----------------------------------------------------------------------
Ran 55 tests in 1.356s

OK
```

---

## 5. Summary of System Health Across All Views

1. **Authentication Portal:** Robust PBKDF2 verification, full name validation, password visibility toggle, session persistence, credential helper.
2. **Overview Dashboard:** Instant rendering of KPI cards, grouped bar Cash Flow chart, category share Donut chart, active spending alerts, recent transaction feed.
3. **Add Transaction:** Dual-tab Income and Expense recording with date picker, category dropdown, amount validation, payment mode selector, and remarks.
4. **All Transactions:** Search and multi-criteria filtering (month, type, category, keyword), responsive summary metrics, interactive edit form, and secure deletion.
5. **Budget Management:** 4-tier threshold alerts (Normal < 70%, Awareness 70–89%, Warning 90–99%, Exceeded $\ge$ 100%), ranked utilization bars, and inline budget configuration.
6. **Smart Budget Intelligence:** Daily safe-to-spend limits, burn rate, linear end-of-month projection, overspending risk index (0–100), interactive gauge, and dynamic recommendations.
7. **Spending Analytics:** Donut charts, cumulative spending velocity charts, and payment mode breakdowns.
8. **Reports & Data:** Demo dataset management (Load, Reload, Remove Only Demo Records), CSV export, automated timestamped snapshots, and safe database reset.
9. **About Project:** Bennett University course metadata, project objectives, official team roster, and viva python concept guide.
10. **Settings:** Dynamic user profile inspection with initials avatar, fiscal parameters, theme telemetry, and storage diagnostics.
11. **Admin Console:** Restricted to HARSH (`role == 'admin'`), managing team accounts, status toggling, password resets, and security audit logs.

---

## 6. Remaining Issues

- **None.** All discovered bugs have been analyzed, root causes diagnosed, code fixes implemented, unit tests expanded, and end-to-end functionality verified.
