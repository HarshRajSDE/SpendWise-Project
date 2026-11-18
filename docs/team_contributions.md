# SpendWise – Team Contributions Breakdown
## Distribution of Responsibilities & Individual Roles

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  

---

## 👥 Project Team Overview

| Member Name | Student ID | Core Contribution / Focus | Primary Implementation Files |
| :--- | :---: | :--- | :--- |
| **Ridhima** | `S26CSEU1925` | **Project Coordination & Expense-Tracking Workflow** | `views/view_add_transaction.py`, `views/view_transactions.py` |
| **Anoushka** | `S26CSEU1922` | **Project Documentation & Organization of Report Content** | `docs/*`, `modules/data_manager.py` |
| **AATIRTH** | `S26CSEU1913` | **Transaction Data Handling & Calculation Logic** | `modules/calc_engine.py`, `tests/test_calculations.py` |
| **HARSH** | `S26CSEU1935` | **Budget Monitoring & Alert Logic (Special Computational Focus)** | `modules/budget_engine.py`, `modules/intelligence_engine.py`, `views/view_intelligence.py`, `views/view_budget.py` |
| **SRISHTHI** | `S26CSEU1939` | **Spending Analysis & Visualization / Reporting** | `views/view_analytics.py`, `views/view_overview.py`, `modules/styles.py` |

---

## 🔍 Detailed Individual Contribution Reports

### 1. Ridhima (`S26CSEU1925`)
- **Assigned Focus:** Project coordination and expense-tracking workflow.
- **Key Deliverables:**
  - Designed the dual-tab transaction recording workflow for Expense and Income in [`views/view_add_transaction.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_add_transaction.py).
  - Implemented field-level validations (positive amount constraint, date sanitization, and fallback descriptions).
  - Coordinated team syncs, verified milestones against college requirements, and streamlined the input ledger workflow.

---

### 2. Anoushka (`S26CSEU1922`)
- **Assigned Focus:** Project documentation and organization of report content.
- **Key Deliverables:**
  - Structured and authored the complete documentation suite in `docs/` following Bennett University submission guidelines.
  - Assisted in designing the file persistence utilities in [`modules/data_manager.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/data_manager.py), specifically the automated snapshot backup routines.
  - Organized test logs, installation instructions, and flowchart specifications.

---

### 3. AATIRTH (`S26CSEU1913`)
- **Assigned Focus:** Transaction data handling and calculation logic.
- **Key Deliverables:**
  - Implemented the core financial calculation routines in [`modules/calc_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/calc_engine.py):
    - Total Income ($I = \sum \text{Income}$)
    - Total Expenditure ($E = \sum \text{Expense}$)
    - Net Balance ($B = I - E$)
    - Savings Rate ($S = (B / I) \times 100\%$)
  - Engineered the zero-division-safe savings rate logic and the Indian Rupee (`₹`) numbering formatter with standard grouping.
  - Authored the core unit tests in [`tests/test_calculations.py`](file:///Users/harshraj/Desktop/SpendWise_Project/tests/test_calculations.py).

---

### 4. HARSH (`S26CSEU1935`) — *Special Computational Contribution*
- **Assigned Focus:** Budget monitoring and alert logic.
- **Key Deliverables:**
  - Designed and authored the **Budget Monitoring Engine** in [`modules/budget_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/budget_engine.py):
    - Multi-tier alert thresholds (**Normal < 70%, Awareness 70%–89%, Warning 90%–99%, Exceeded $\ge 100\%$**).
    - Unbudgeted expense isolation preventing false budget breach alerts.
    - Prioritized alert card generation.
    - Category-wise spending ranking with budget utilization percentages.
  - Designed and authored the **Smart Budget Intelligence Engine** in [`modules/intelligence_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/intelligence_engine.py):
    - Month-to-date daily burn rate ($A = \text{Expenses} / \text{Elapsed Days}$).
    - Linear end-of-month run-rate forecast ($E_{\text{forecast}} = A \times \text{Total Days}$).
    - Daily safe-to-spend limit ($L_{\text{safe}}$) with zero-clamp when budget is exceeded.
    - Rule-based Overspending Risk Index (0–100 score).
    - Dynamic calendar context handling leap years in February via `calendar.monthrange`.
  - Authored the test suites [`tests/test_budget_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/tests/test_budget_engine.py) and [`tests/test_intelligence_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/tests/test_intelligence_engine.py).

---

### 5. SRISHTHI (`S26CSEU1939`)
- **Assigned Focus:** Spending analysis and visualization / reporting.
- **Key Deliverables:**
  - Designed the interactive visual analytics views in [`views/view_analytics.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_analytics.py) and [`views/view_overview.py`](file:///Users/harshraj/Desktop/SpendWise_Project/views/view_overview.py).
  - Built interactive Plotly figures:
    - Expense category distribution donut chart.
    - Cash flow comparison grouped bar chart.
    - Daily spending bar with cumulative trajectory line.
    - Multi-month income vs. expense grouped bars.
  - Authored the custom SaaS dark navy CSS design system in [`modules/styles.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/styles.py) ensuring visual polish and responsiveness.
