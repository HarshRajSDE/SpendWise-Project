# Python Concepts Guide – SpendWise Implementation
## Mapping Computational Principles to Real Project Source Code

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  

This document explains where and how foundational Python concepts are applied within **SpendWise**. Every concept is backed by actual code snippets from the project.

---

## 1. Variables and Data Types

In Python, variables dynamically reference typed objects in memory:
- **`float`:** Used for monetary amounts, percentages, and budget limits where decimal precision is necessary.
- **`int`:** Used for day counts, ranks, and integer risk scores.
- **`str`:** Used for transaction IDs, dates (`'YYYY-MM-DD'`), categories, descriptions, and status labels.
- **`bool`:** Used for verification flags (`is_past`, `is_current`, `include_symbol`).

```python
# From modules/intelligence_engine.py
def calculate_monthly_forecast(avg_daily_spend: float, total_days_in_month: int) -> float:
    try:
        daily = float(avg_daily_spend)
        total_days = int(total_days_in_month)
    except (ValueError, TypeError):
        return 0.0

    if daily <= 0 or total_days <= 0:
        return 0.0

    return round(daily * total_days, 2)
```

---

## 2. Conditional Statements (`if-elif-else`)

Conditional statements control program execution based on boolean expressions. Used extensively in `modules/budget_engine.py` to evaluate the 4-tier alert threshold boundaries:

```python
# From modules/budget_engine.py
if utilization_pct < (THRESHOLD_SAFE * 100.0):       # < 70%
    status = "Normal"
elif utilization_pct < (THRESHOLD_WARNING * 100.0):   # 70% <= util < 90%
    status = "Spending Awareness"
elif utilization_pct < (THRESHOLD_CRITICAL * 100.0):  # 90% <= util < 100%
    status = "High Spending Warning"
else:                                                 # >= 100%
    status = "Budget Exceeded"
```

---

## 3. Loops (`for`, `while`)

Loops iterate over sequences and datasets:
- **`for` loops:** Used to iterate through transaction rows and compute aggregate totals.
- **`while` loops:** Used in `format_inr` to partition thousands digits into pairs according to the Indian numbering system.

```python
# From modules/calc_engine.py (While loop in INR formatter)
groups = []
while len(remaining) > 2:
    groups.insert(0, remaining[-2:])
    remaining = remaining[:-2]
if remaining:
    groups.insert(0, remaining)
formatted_int = ",".join(groups) + "," + last_three

# From modules/calc_engine.py (For loop in aggregations)
total = 0.0
for txn in transactions:
    if txn.get("type") == "Expense":
        total += float(txn.get("amount", 0.0))
```

---

## 4. Lists & List Comprehensions

Lists are ordered, mutable sequences:
- Used to store records, filter results, and rank categories.
- List comprehensions provide concise filtering and transformation.

```python
# From modules/intelligence_engine.py
expense_txns = [t for t in month_txns if t.get("type") == "Expense"]
warning_cats = [c for c in ranked_cats if c["status"] in ["High Spending Warning", "Budget Exceeded"]]
```

---

## 5. Tuples

Tuples are ordered, immutable sequences used for returning multiple related values from functions:

```python
# From modules/budget_engine.py
def compute_utilization(spent: float, budget: float) -> tuple:
    ...
    return (round(utilization_pct, 2), status)

# From modules/intelligence_engine.py
def calculate_overspending_risk_index(projected_expenses: float, monthly_budget: float) -> tuple:
    ...
    return (score, level, desc, color)
```

---

## 6. Sets

Sets are unordered collections of unique elements. Used in `modules/calc_engine.py` to extract all unique months from transaction dates without duplicates:

```python
# From modules/calc_engine.py
def get_available_months(transactions: list) -> list:
    months = set()
    for txn in transactions:
        d = txn.get("date", "")
        if len(d) >= 7 and d[4] == "-":
            months.add(d[:7])
    months.add(datetime.now().strftime("%Y-%m"))
    return sorted(list(months), reverse=True)
```

---

## 7. Dictionaries

Dictionaries store key-value pairs with $O(1)$ average lookup time:
- Transaction records are structured as dictionaries.
- Category budgets and monthly summaries are mapped with string keys.

```python
# From modules/data_manager.py
transaction = {
    "id": "TXN-01",
    "date": "2026-11-16",
    "type": "Expense",
    "category": "Food",
    "amount": 450.00,
    "payment_mode": "UPI",
    "description": "Lunch"
}
```

---

## 8. Functions & Modular Programming

Code is partitioned into pure functions with single responsibilities, clear parameters, and descriptive docstrings:

```python
# From modules/budget_engine.py
def calculate_remaining_budget(budget: float, spent: float) -> float:
    """Calculates remaining budget allowance (negative if overspent)."""
    try:
        b = float(budget)
        s = float(spent)
    except (ValueError, TypeError):
        return 0.0
    return round(b - s, 2)
```

---

## 9. File Handling & CSV Storage

File I/O uses Python context managers (`with open`) ensuring automatic resource cleanup and file closing:
- `csv.DictReader`: Maps CSV lines into Python dictionaries using the header row.
- `csv.DictWriter`: Writes Python dictionaries into CSV lines.

```python
# From modules/data_manager.py
def load_transactions() -> list:
    transactions = []
    with open(TRANSACTIONS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions
```

---

## 10. JSON Serialization

JSON stores nested configurations for category budget allocations:
- `json.load()`: Deserializes JSON files into Python dictionaries.
- `json.dump(..., indent=4)`: Serializes Python dictionaries into formatted JSON text.

```python
# From modules/data_manager.py
def load_budget() -> dict:
    with open(BUDGET_FILE, mode="r", encoding="utf-8") as file:
        return json.load(file)

def save_budget(budget_data: dict) -> bool:
    with open(BUDGET_FILE, mode="w", encoding="utf-8") as file:
        json.dump(budget_data, file, indent=4)
        return True
```

---

## 11. Exception Handling (`try-except`)

Defensive programming prevents crashes from runtime anomalies:
- Handles `ValueError` and `TypeError` when parsing user inputs.
- Handles `ZeroDivisionError` when calculating savings rate on ₹0 income.
- Handles `FileNotFoundError` by automatically regenerating default empty files.

```python
# From modules/calc_engine.py
def calculate_savings_rate(total_income: float, total_expenses: float) -> float:
    try:
        inc = float(total_income)
        exp = float(total_expenses)
    except (ValueError, TypeError):
        return 0.0

    # Defensive check against ZeroDivisionError
    if inc <= 0:
        return 0.0

    return round(((inc - exp) / inc) * 100.0, 2)
```

---

## 12. Standard Python Libraries

The project leverages standard Python libraries:
- **`calendar`:** `calendar.monthrange(year, month)` dynamically determines the exact number of days in any month, automatically handling leap years (e.g., February 2024 has 29 days vs. February 2026 has 28 days).
- **`datetime`:** `datetime.now()`, `date.today()` manage transaction timestamps and month-to-date calendar arithmetic.
- **`uuid`:** `uuid.uuid4()` generates unique 8-character alphanumeric IDs for transactions.
- **`shutil`:** `shutil.copy2()` creates atomic file snapshots in `data/backups/`.
- **`os`:** `os.path.join()`, `os.makedirs()` ensure platform-agnostic file paths across Windows, macOS, and Linux.
- **`unittest`:** Built-in testing harness executing all 44 test cases in the test suite.
