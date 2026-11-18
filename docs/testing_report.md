# SpendWise – Comprehensive Testing Report
## Test Suite Results, Verification Matrices & Quality Assurance

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  
**Test Framework:** Python Standard Library `unittest` + Streamlit `AppTest`  

---

## 1. Executive Summary

- **Total Automated Test Cases:** 51
- **Tests Passed:** 51 (100% Pass Rate)
- **Tests Failed:** 0
- **Execution Duration:** ~1.0 second
- **UI Exception Rate:** 0 exceptions across all navigation views
- **Multi-Tenant Security:** Full row-level data isolation verified with 0 data leakage across accounts

```text
Ran 51 tests in 1.013s
OK
```

---

## 2. Test Execution Breakdown by Module

| Test Module | Test File | Test Cases | Status | Key Features Verified |
| :--- | :--- | :---: | :---: | :--- |
| **Financial Calculations** | `tests/test_calculations.py` | 14 | **PASSED** | Total income, expenses, net balance, savings rate, ZeroDivision safety, INR formatting. |
| **Data Persistence** | `tests/test_data_manager.py` | 10 | **PASSED** | Empty file init, adding rows, deleting rows, updating rows, invalid inputs, backups, export. |
| **Budget Monitoring** | `tests/test_budget_engine.py` | 10 | **PASSED** | Exact 70%, 90%, 100% threshold boundaries, unbudgeted spend, remaining budget, ranking. |
| **Intelligence Engine** | `tests/test_intelligence_engine.py` | 10 | **PASSED** | Daily burn rate, linear forecast, safe daily spend, 0–100 risk score clamp, leap year Feb. |
| **Multi-User Security & Isolation** | `tests/test_multi_user.py` | 7 | **PASSED** | PBKDF2 cryptography, Bennett team roster auth, row-level isolation, attack prevention, audit logs. |

---

## 3. Comprehensive Verification Matrix

### 3.1 Mathematical & Financial Logic
| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-CALC-01` | Total Income Calculation | Txns with ₹50,000 + ₹10,000 Income | ₹60,000.00 | ₹60,000.00 | **PASS** |
| `TC-CALC-02` | Total Expense Calculation | Txns with ₹3,500 + ₹1,500 + ₹500 | ₹5,500.00 | ₹5,500.00 | **PASS** |
| `TC-CALC-03` | Net Balance Calculation | Income ₹60,000, Expense ₹5,500 | ₹54,500.00 | ₹54,500.00 | **PASS** |
| `TC-CALC-04` | Normal Savings Rate | Income ₹10,000, Expense ₹2,500 | 75.0% | 75.0% | **PASS** |
| `TC-CALC-05` | Zero Income Savings Rate | Income ₹0.00, Expense ₹5,000 | 0.0% (No crash) | 0.0% | **PASS** |
| `TC-CALC-06` | Deficit Savings Rate | Income ₹10,000, Expense ₹12,000 | -20.0% | -20.0% | **PASS** |
| `TC-CALC-07` | Indian Currency Notation | Amount 123456.78 | `₹1,23,456.78` | `₹1,23,456.78` | **PASS** |
| `TC-CALC-08` | Negative INR Notation | Amount -4500.00 | `-₹4,500.00` | `-₹4,500.00` | **PASS** |

### 3.2 Budget Thresholds & Alert Logic (Harsh's Focus)
| Test ID | Test Scenario | Incurred / Budget | Expected Status | Actual Status | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-BUD-01` | Below 70% Threshold | ₹699 / ₹1,000 (69.9%) | Normal | Normal | **PASS** |
| `TC-BUD-02` | Exactly 70% Boundary | ₹700 / ₹1,000 (70.0%) | Spending Awareness | Spending Awareness | **PASS** |
| `TC-BUD-03` | Mid-Awareness Tier | ₹850 / ₹1,000 (85.0%) | Spending Awareness | Spending Awareness | **PASS** |
| `TC-BUD-04` | Exactly 90% Boundary | ₹900 / ₹1,000 (90.0%) | High Spending Warning | High Spending Warning | **PASS** |
| `TC-BUD-05` | Mid-Warning Tier | ₹950 / ₹1,000 (95.0%) | High Spending Warning | High Spending Warning | **PASS** |
| `TC-BUD-06` | Exactly 100% Boundary | ₹1,000 / ₹1,000 (100.0%) | Budget Exceeded | Budget Exceeded | **PASS** |
| `TC-BUD-07` | Over 100% Exceeded | ₹1,200 / ₹1,000 (120.0%) | Budget Exceeded | Budget Exceeded | **PASS** |
| `TC-BUD-08` | Zero Budget, Zero Spend | ₹0 / ₹0 | Unbudgeted | Unbudgeted | **PASS** |
| `TC-BUD-09` | Unbudgeted Spending | ₹500 / ₹0 | Unbudgeted Spend (No crash) | Unbudgeted Spend | **PASS** |
| `TC-BUD-10` | Overspent Remaining | Budget ₹5,000, Spent ₹5,500 | -₹500.00 | -₹500.00 | **PASS** |

### 3.3 Intelligence Engine & Calendar Context
| Test ID | Test Scenario | Input Conditions | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-INT-01` | Leap Year February | Year 2024, Month 2 | Total Days = 29 | Total Days = 29 | **PASS** |
| `TC-INT-02` | Standard Year February | Year 2026, Month 2 | Total Days = 28 | Total Days = 28 | **PASS** |
| `TC-INT-03` | Historical Month Flag | Target Jan 2026 as of Nov 2026 | `is_past = True`, remaining = 0 | `is_past = True`, remaining = 0 | **PASS** |
| `TC-INT-04` | Average Daily Spending | Spent ₹15,000 in 15 days | ₹1,000.00/day | ₹1,000.00/day | **PASS** |
| `TC-INT-05` | Month-End Run Forecast | ₹1,000/day × 30 days | ₹30,000.00 | ₹30,000.00 | **PASS** |
| `TC-INT-06` | Projected Overspending | Projected ₹35,000 on ₹30,000 budget | ₹5,000.00 | ₹5,000.00 | **PASS** |
| `TC-INT-07` | Normal Safe Daily Spend | Rem. ₹15,000 across 15 days | ₹1,000.00/day | ₹1,000.00/day | **PASS** |
| `TC-INT-08` | Safe Spend when Exceeded | Budget ₹20,000, Spent ₹22,000 | Strictly ₹0.00/day | Strictly ₹0.00/day | **PASS** |
| `TC-INT-09` | Low Risk Score (< 70) | Projected ₹6,000 on ₹10,000 budget | Score = 60, Low Risk | Score = 60, Low Risk | **PASS** |
| `TC-INT-10` | Moderate Risk (70–89) | Projected ₹7,000 on ₹10,000 budget | Score = 70, Moderate Risk | Score = 70, Moderate Risk | **PASS** |
| `TC-INT-11` | High Risk (90–99) | Projected ₹9,000 on ₹10,000 budget | Score = 90, High Risk | Score = 90, High Risk | **PASS** |
| `TC-INT-12` | Critical Risk Clamp (100) | Projected ₹15,000 on ₹10,000 budget | Clamped to 100, Critical | Clamped to 100, Critical | **PASS** |

### 3.4 Data Persistence & Input Validation
| Test ID | Test Scenario | Input / Operation | Expected Behavior | Actual Behavior | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-DAT-01` | Negative Amount Rejected | `add_transaction({"amount": -500})` | Returns `False` | Returns `False` | **PASS** |
| `TC-DAT-02` | Zero Amount Rejected | `add_transaction({"amount": 0})` | Returns `False` | Returns `False` | **PASS** |
| `TC-DAT-03` | Non-numeric Rejected | `add_transaction({"amount": "abc"})` | Returns `False` | Returns `False` | **PASS** |
| `TC-DAT-04` | Update Transaction | Change amount ₹400 $\to$ ₹550 | Updated in CSV | Updated in CSV | **PASS** |
| `TC-DAT-05` | Delete Transaction | Remove by unique ID | Row deleted from CSV | Row deleted from CSV | **PASS** |
| `TC-DAT-06` | CSV Export | Export complete ledger | Returns valid CSV string | Returns valid CSV string | **PASS** |
| `TC-DAT-07` | Backup Snapshot Creation | Call `backup_data()` | Creates files in `backups/` | Creates files in `backups/` | **PASS** |
| `TC-DAT-08` | Database Reset | Call `clear_all_data()` | Reset to empty default | Reset to empty default | **PASS** |

### 3.5 Multi-User Security & Row-Level Data Isolation (Bennett Team Roster)
| Test ID | Test Scenario | Input / Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-SEC-01` | PBKDF2 Password Hashing | `hash_password("Pass123!")` | 260K iter salted SHA-256 hash | 260K iter salted SHA-256 hash | **PASS** |
| `TC-SEC-02` | Team Roster Authentication | 5 Bennett University accounts | All 5 authenticate with PIN | All 5 authenticated successfully | **PASS** |
| `TC-SEC-03` | Unauthorized Login Rejection | Invalid enrollment / bad PIN | Returns `None` (Access Denied) | Returns `None` | **PASS** |
| `TC-SEC-04` | Row-Level Txn Isolation | User A queries ledgers | User B's transactions invisible | 0 data leakage across users | **PASS** |
| `TC-SEC-05` | Unauthorized Edit Attack | User B attempts edit of User A txn | Query blocked (`rowcount=0`) | Blocked (`False`, Access Denied) | **PASS** |
| `TC-SEC-06` | Unauthorized Delete Attack | User B attempts delete of User A txn | Blocked by `WHERE user_id=?` | Blocked (`False`, Access Denied) | **PASS** |
| `TC-SEC-07` | Account Deactivation & Audit | Deactivate account via Admin | Immediate login block + audit log | Login blocked + audit logged | **PASS** |

---

## 4. UI Headless & Live Browser Verification

- **Headless Streamlit AppTest:**
  - Automated script traversed all 8 navigation options with empty data and demo data.
  - Zero unhandled exceptions or render failures detected.
- **Live Browser Inspection:**
  - Verified live at `http://localhost:8502` using browser subagent.
  - Verified all metric cards, Plotly charts, risk gauges, forms, and tables render smoothly.
