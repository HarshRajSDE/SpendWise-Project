# SpendWise – Project Screenshots & Visual Evidence Checklist
## Submission Visual Verification Guide

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  
**Screenshots Storage Directory:** [`screenshots/`](file:///Users/harshraj/Desktop/SpendWise_Project/screenshots/)  

---

## 📸 Verified Screenshots Checklist

| Screen / View Name | Target File Name | Status | Key Visual Elements to Verify |
| :--- | :--- | :---: | :--- |
| **1. Overview Dashboard** | `01_overview_dashboard.png` | Manual / Browser | 4 KPI cards (Income, Expense, Balance, Savings Rate), monthly budget progress bar, cash flow bar chart, and category donut chart. |
| **2. Add Transaction** | `02_add_transaction.py` | Manual / Browser | Dual-tab interface (Expense/Income), ₹ amount input, category dropdown, payment mode, and submit button. |
| **3. Transaction History** | `03_transaction_history.png` | Manual / Browser | Filterable transaction table, search bar, summary cards, pre-filled Edit Transaction form, and Delete button. |
| **4. Budget Management** | `04_budget_management.png` | Manual / Browser | Multi-tier threshold guide banner (70%, 90%, 100%), category progress bars, and budget allocation editor. |
| **5. Smart Budget Intelligence** | `intelligence_engine.png` | **Captured & Verified** | Safe daily spending, projected month-end spend, projected overspending, Plotly 0–100 risk gauge, and smart recommendations. |
| **6. Spending Analytics** | `06_spending_analytics.png` | Manual / Browser | Category donut chart, payment mode distribution bar chart, and daily cumulative spending trajectory. |
| **7. Reports & Data Management** | `07_reports_management.png` | Manual / Browser | Database health summary, CSV download button, backup snapshot button, demo data seeder, and reset control. |
| **8. About Project** | `08_about_project.png` | Manual / Browser | Bennett University header, course metadata, Python concepts expander, and team member cards highlighting Harsh's role. |

---

## 🖼️ Host-Verified Screenshot Preview

### Smart Budget Intelligence Engine (Captured via Browser Inspector)
![Smart Budget Intelligence Engine](screenshots/intelligence_engine.png)

*Visible verified components:*
- **Safe Daily Spending Limit:** `₹536.87/day` (15 days left in current month).
- **Projected Month-End Spend:** `₹31,775.70` (Burn rate `₹1,059.19/day`).
- **Projected Overspending:** `₹6,775.70` deficit.
- **Overspending Risk Index:** `100/100` (Critical Risk Level).
- **Plotly Risk Gauge:** Color-banded arc (Green 0–69, Amber 70–89, Orange 90–99, Crimson 100).
- **Smart Recommendations:** Actionable alerts advising discretionary pacing.

---

## 🛠️ Step-by-Step Manual Screenshot Capture Guide

If you are generating high-resolution PNGs for your printed college submission report or PPT slide deck:

### Step 1: Launch Application with Demo Data
```bash
# Terminal
source .venv/bin/activate
streamlit run app.py
```
1. Open `http://localhost:8501`.
2. Go to **"Reports and Data Management"** and click **"🚀 Load Sample Demo Data (INR ₹)"**.

### Step 2: Capture Full Screen on macOS
- Navigate to each of the 8 sidebar tabs.
- Press **`Cmd + Shift + 4`** then press **`Space`** to take a window screenshot.
- Save each screenshot into the `screenshots/` directory using the filenames in the table above.

### Step 3: Capture Full Screen on Windows
- Press **`Windows Key + Shift + S`** (Snipping Tool).
- Capture the dashboard window and save each PNG into `screenshots/`.
