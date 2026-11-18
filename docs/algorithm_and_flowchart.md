# SpendWise – Algorithms & Flowchart Specification
## Computational Logic & Decision Tree Documentation

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  

---

## 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph UI_Layer [Streamlit Presentation Layer]
        Nav["Sidebar Navigation Router"]
        P1["Overview Dashboard"]
        P2["Add Transaction Form"]
        P3["All Transactions Ledger"]
        P4["Budget Management"]
        P5["Smart Budget Intelligence"]
        P6["Spending Analytics"]
        P7["Reports & Backups"]
        P8["About & Viva Notes"]
    end

    subgraph Logic_Layer [Business & Intelligence Engines]
        Calc["calc_engine.py<br/>(Income, Expense, Balance, Savings Rate)"]
        Budget["budget_engine.py [Harsh]<br/>(Utilization %, 70/90/100% Thresholds, Alerts)"]
        Intel["intelligence_engine.py [Harsh]<br/>(Daily Burn, Forecast, Safe Daily Limit, Risk)"]
    end

    subgraph Data_Layer [Data Persistence Layer]
        DM["data_manager.py<br/>(CSV Reader/Writer, JSON Loader, Backups)"]
        CSV[("transactions.csv")]
        JSON[("budget.json")]
        Backups[("backups/")]
    end

    Nav --> P1 & P2 & P3 & P4 & P5 & P6 & P7 & P8
    P1 & P3 & P6 --> Calc
    P1 & P4 & P5 --> Budget
    P5 --> Intel
    Calc & Budget & Intel --> DM
    DM <--> CSV
    DM <--> JSON
    DM --> Backups
```

---

## 2. Transaction Ingestion & Validation Algorithm

```mermaid
flowchart TD
    Start([User Submits Transaction]) --> ValidateAmount{Amount > 0 ?}
    ValidateAmount -- No --> ShowError[Display Error: 'Amount must be > ₹0']
    ValidateAmount -- Yes --> CheckID{ID provided ?}
    CheckID -- No --> GenID[Generate 8-char UUID]
    CheckID -- Yes --> PrepareDict[Prepare Clean Dictionary]
    GenID --> PrepareDict
    PrepareDict --> OpenFile[Open transactions.csv in append mode 'a']
    OpenFile --> WriteCSV[Write DictWriter row]
    WriteCSV --> Success[Display Success Message & Refresh Dashboard]
    Success --> End([Finished])
    ShowError --> End
```

### Pseudocode:
```text
Algorithm AddTransaction(transaction_data):
    Input: dictionary containing date, type, category, amount, payment_mode, description
    Output: boolean success flag

    If float(transaction_data.amount) <= 0:
        Return False (Invalid Amount)

    If transaction_data does not contain "id":
        transaction_data.id = GenerateUUID(8)

    Open "data/transactions.csv" with mode="append":
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writerow(transaction_data)

    Return True
```

---

## 3. Budget Threshold Evaluation Algorithm (Harsh's Focus)

Evaluates actual spending against planned category or monthly limits using exact 70%, 90%, and 100% thresholds.

```mermaid
flowchart TD
    StartEval([Compute Utilization]) --> CheckBudget{Budget > 0 ?}
    CheckBudget -- No --> CheckSpend{Spent > 0 ?}
    CheckSpend -- No --> Unbudgeted[Status = 'Unbudgeted'<br/>utilization = 0%]
    CheckSpend -- Yes --> UnbudgetedSpend[Status = 'Unbudgeted Spend'<br/>utilization = None]
    
    CheckBudget -- Yes --> CalcUtil[Utilization % = Spent / Budget * 100]
    CalcUtil --> T1{Utilization < 70% ?}
    T1 -- Yes --> Normal[Status: 'Normal'<br/>Badge: Green]
    T1 -- No --> T2{Utilization < 90% ?}
    T2 -- Yes --> Awareness[Status: 'Spending Awareness'<br/>Badge: Amber Yellow]
    T2 -- No --> T3{Utilization < 100% ?}
    T3 -- Yes --> Warning[Status: 'High Spending Warning'<br/>Badge: Orange]
    T3 -- No --> Exceeded[Status: 'Budget Exceeded'<br/>Badge: Crimson Red]

    Normal & Awareness & Warning & Exceeded & Unbudgeted & UnbudgetedSpend --> ReturnTuple([Return utilization %, Status])
```

---

## 4. Safe Daily Spending Algorithm

Calculates allowable daily burn rate to avoid overspending:

```mermaid
flowchart TD
    StartSafe([Calculate Safe Daily Spending]) --> CalcRemainingBudget[Remaining Budget = Monthly Budget - Incurred Expenses]
    CalcRemainingBudget --> CheckOverspent{Remaining Budget <= 0 ?}
    CheckOverspent -- Yes --> LockZero[Safe Daily Spending = ₹0.00 / day<br/>Alert: Budget Exceeded]
    CheckOverspent -- No --> CalcDays[Remaining Days = Total Days in Month - Current Day + 1]
    CalcDays --> CheckDays{Remaining Days <= 0 ?}
    CheckDays -- Yes --> LockZero
    CheckDays -- No --> Divide[Safe Daily Spending = Remaining Budget / Remaining Days]
    Divide --> ReturnVal([Return rounded float in ₹])
    LockZero --> ReturnVal
```

---

## 5. Overspending Risk Index Algorithm

Produces an explainable, deterministic risk index from 0 to 100 based on month-end linear extrapolation:

```mermaid
flowchart TD
    StartRisk([Calculate Risk Index]) --> BurnRate[Daily Burn Rate = Month-to-date Expenses / Elapsed Days]
    BurnRate --> Forecast[Projected Month-End Spend = Burn Rate * Total Days in Month]
    Forecast --> CheckBud{Monthly Budget > 0 ?}
    CheckBud -- No --> CheckProj{Projected Spend > 0 ?}
    CheckProj -- Yes --> Score100[Score = 100, Critical Risk (Unbudgeted)]
    CheckProj -- No --> Score0[Score = 0, Low Risk]
    
    CheckBud -- Yes --> ComputeRatio[Raw Ratio = Projected Spend / Monthly Budget * 100]
    ComputeRatio --> Clamp[Score = min(100, max(0, round(Raw Ratio)))]
    Clamp --> CheckTier{Score < 70 ?}
    CheckTier -- Yes --> LowRisk[Level = 'Low Risk']
    CheckTier -- No --> CheckTier2{Score < 90 ?}
    CheckTier2 -- Yes --> ModRisk[Level = 'Moderate Risk']
    CheckTier2 -- No --> CheckTier3{Score < 100 ?}
    CheckTier3 -- Yes --> HighRisk[Level = 'High Risk']
    CheckTier3 -- No --> CritRisk[Level = 'Critical Risk']
    
    LowRisk & ModRisk & HighRisk & CritRisk & Score100 & Score0 --> ReturnRisk([Return Score, Level, Description, Color])
```
