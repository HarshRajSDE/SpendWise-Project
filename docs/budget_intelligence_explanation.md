# SpendWise – Smart Budget Intelligence & Alert Engine
## Computational Documentation & Viva Presentation Guide

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Academic Year:** 2026–2027  
**Module Lead:** HARSH (`S26CSEU1935`) — *Budget Monitoring & Alert Logic*  
**Implementation Files:** [`modules/budget_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/budget_engine.py), [`modules/intelligence_engine.py`](file:///Users/harshraj/Desktop/SpendWise_Project/modules/intelligence_engine.py)

---

## 1. Overview & Architectural Motivation

In traditional expense tracking systems, budgets are merely passive comparisons between historical sums and a fixed number. In **SpendWise**, the Budget Monitoring and Alert Logic is designed as an **active, predictive intelligence layer** using deterministic computational thinking and transparent arithmetic.

Key architectural design principles:
1. **Zero Black-Box Machine Learning**: No statistical opacity or hallucinations. Every number is calculated using explicit, explainable mathematical formulas.
2. **Defensive Programming**: Zero division errors are strictly prevented when income, budgets, or elapsed days are zero.
3. **Multi-Tier Boundary Evaluation**: A standardized 4-tier alert system is applied consistently across overall monthly budgets and individual categories.

---

## 2. Mathematical Formulas & Calculation Logic

### Formula A: Budget Utilization Percentage ($U$)
Measures the percentage of an allocated budget consumed by actual incurred expenses:
$$U = \left( \frac{\text{Actual Expenses}}{\text{Allocated Budget}} \right) \times 100\%$$

- **Code implementation:** `compute_utilization(spent, budget)` in `modules/budget_engine.py`.
- **Edge cases handled:**
  - If $\text{Budget} == 0$ and $\text{Spent} == 0$: Returns `(0.0, "Unbudgeted")`.
  - If $\text{Budget} == 0$ and $\text{Spent} > 0$: Returns `(None, "Unbudgeted Spend")`. Prevents division by zero and prevents falsely tagging unbudgeted expenses as budget breaches.

---

### Formula B: Average Daily Spending ($A_{\text{daily}}$)
Quantifies the daily burn rate across the elapsed days of the active month:
$$A_{\text{daily}} = \frac{\text{Month-to-Date Incurred Expenses}}{\text{Days Elapsed in Active Month}}$$

- **Code implementation:** `calculate_average_daily_spending(month_expenses, elapsed_days)` in `modules/intelligence_engine.py`.
- **Edge cases handled:**
  - On Day 1: $\text{Elapsed Days} = 1$.
  - When expenses are 0: Returns `₹0.00/day`.

---

### Formula C: Month-End Linear Run-Rate Forecast ($E_{\text{forecast}}$)
Projects the total expenditure expected by the final day of the month assuming current spending velocity continues:
$$E_{\text{forecast}} = A_{\text{daily}} \times \text{Total Days in Month}$$

- **Code implementation:** `calculate_monthly_forecast(avg_daily_spend, total_days_in_month)`.
- **Temporal handling:**
  - **Current Month:** Full linear run-rate projection.
  - **Historical (Past) Month:** Projection is disabled; actual total expenditure is displayed since the month has already completed.
  - **Future Month:** Projection is ₹0.00 until transactions occur.

---

### Formula D: Projected Overspending Variance ($O_{\text{projected}}$)
Computes the anticipated budget breach size:
$$O_{\text{projected}} = \max(0, E_{\text{forecast}} - \text{Monthly Budget})$$

- If $E_{\text{forecast}} \le \text{Monthly Budget}$, $O_{\text{projected}} = 0.00$ (indicates planned surplus).
- If $E_{\text{forecast}} > \text{Monthly Budget}$, outputs the exact deficit amount in ₹.

---

### Formula E: Safe Daily Spending Limit ($L_{\text{safe}}$)
Determines how much money the user can safely spend per day for the rest of the month without breaching their monthly budget:
$$\text{Remaining Budget} = \text{Monthly Budget} - \text{Incurred Expenses}$$
$$\text{Remaining Days} = \text{Total Days in Month} - \text{Current Day} + 1$$
$$L_{\text{safe}} = \begin{cases} \frac{\text{Remaining Budget}}{\text{Remaining Days}} & \text{if Remaining Budget} > 0 \\ 0.00 & \text{if Remaining Budget} \le 0 \end{cases}$$

- **Strict Boundary Rule:** When the budget has already been exceeded ($\text{Remaining Budget} \le 0$), $L_{\text{safe}}$ must strictly return **₹0.00/day**, alerting the user to halt discretionary spending.

---

### Formula F: Overspending Risk Index (0–100 Score)
A deterministic, rule-based computational gauge measuring projected budget exhaustion:
$$\text{Raw Ratio} = \left(\frac{E_{\text{forecast}}}{\text{Monthly Budget}}\right) \times 100$$
$$\text{Risk Score} = \min(100, \max(0, \text{round}(\text{Raw Ratio})))$$

- **Viva Clarification:** This score is a **rule-based computational metric**, NOT a statistical probability of financial loss. It represents the degree to which projected expenditure reaches or exceeds the user's budget ceiling.

---

## 3. Conditional Alert Threshold System

SpendWise applies the following thresholds across overall monthly budgets and individual categories:

| Utilization Range | Tier Label | Color Code | Severity | System Behavior |
| :--- | :--- | :---: | :---: | :--- |
| **$< 70.0\%$** | **Normal** | `#10B981` (Emerald Green) | Safe | Healthy pace, surplus expected. |
| **$70.0\% \le U < 90.0\%$** | **Spending Awareness** | `#F59E0B` (Amber Yellow) | Medium | Pacing warning; discretionary spending review recommended. |
| **$90.0\% \le U < 100.0\%$** | **High Spending Warning** | `#F97316` (Orange) | High | Critical threshold; non-essential spending should be paused. |
| **$\ge 100.0\%$** | **Budget Exceeded** | `#EF4444` (Crimson Red) | Critical | Budget breached; deficit alerts active; daily safe limit set to ₹0. |

```python
# Exact conditional logic implementation
if utilization_pct < 70.0:
    status = "Normal"
elif utilization_pct < 90.0:
    status = "Spending Awareness"
elif utilization_pct < 100.0:
    status = "High Spending Warning"
else:
    status = "Budget Exceeded"
```

---

## 4. Key Python Functions Overview

### In `modules/budget_engine.py`:
- `compute_utilization(spent, budget)`: Computes percentage and maps to exact tier string.
- `calculate_remaining_budget(budget, spent)`: Returns surplus or deficit float.
- `check_category_budget(category, spent, budget)`: Generates detailed audit dictionary for a category.
- `get_budget_alerts(category_budgets, category_expenses, total_budget, total_expenses)`: Generates prioritized alert list (exceeded $\to$ high warning $\to$ awareness).
- `rank_spending_categories(category_expenses, category_budgets)`: Sorts categories descending by expenditure and calculates percentage shares.

### In `modules/intelligence_engine.py`:
- `get_month_calendar_context(year_month, as_of_date)`: Uses Python's standard `calendar.monthrange` to accurately calculate total days (including leap years like February 2024 with 29 days vs 2026 with 28 days) and distinguishes past, current, and future months.
- `calculate_average_daily_spending(month_expenses, elapsed_days)`: Computes daily burn rate.
- `calculate_monthly_forecast(avg_daily_spend, total_days_in_month)`: Projects month-end spending.
- `calculate_projected_overspending(projected_expenses, monthly_budget)`: Computes forecasted deficit.
- `calculate_safe_daily_spending(monthly_budget, month_expenses, remaining_days)`: Calculates allowable spending per day.
- `calculate_overspending_risk_index(projected_expenses, monthly_budget)`: Evaluates risk index clamped between 0 and 100.
- `generate_smart_recommendations(intelligence)`: Generates actionable plain-language financial guidance.
- `generate_budget_intelligence(year_month, transactions, budget_data, as_of_date)`: Master pipeline orchestrating all metrics.

---

## 5. Edge Case Handling Matrix

| Scenario | Risk | System Defense Mechanism |
| :--- | :--- | :--- |
| **Zero Income Recorded** | `ZeroDivisionError` in savings rate | Clamped to `0.0%` with clear explanatory subtitle. |
| **Zero Category Budget Set** | `ZeroDivisionError` in utilization | Classified as `Unbudgeted` or `Unbudgeted Spend` rather than a budget breach. |
| **Budget Already Exceeded** | Negative safe spending calculation | Clamped to strictly `₹0.00/day`. |
| **Day 1 of the Month** | Division by zero in burn rate | `Elapsed Days` initialized to `1`, preventing zero division. |
| **Last Day of the Month** | Division by zero in safe spend | `Remaining Days` is `1` (includes today). |
| **Leap Year February** | Incorrect day count (28 vs 29) | Calculated dynamically using `calendar.monthrange(year, 2)`. |
| **Historical Month Selected** | Misleading future forecast | Forecast disabled; actual final expenditure displayed. |
| **Corrupted or Empty CSV** | Application crash | Graceful fallback to `[]` and automatic file header recreation. |
