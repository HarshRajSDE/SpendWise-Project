# SpendWise – Comprehensive Viva Voce Preparation Guide
## 45+ Practice Questions & Answers in Student-Friendly Hinglish

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  
**Module Focus:** Harsh (`S26CSEU1935`) – Budget Monitoring & Alert Logic  

---

## 📌 Section 1: General Project & Architecture Questions

### Q1. SpendWise project ka basic objective kya hai?
**Answer:** SpendWise ek personal expense aur budget tracking dashboard hai jo college students ko unke monthly allowance, stipends aur kharche manage karne me madad karta hai. Isme humne kisi external paid API ya black-box machine learning model ke bina, **transparent computational formulas** aur local CSV/JSON storage se real-time forecasting aur budget alert system build kiya hai.

---

### Q2. Aapne project ko ek hi python file me likhne ke bajaye modular architecture me kyu banaya?
**Answer:** Modular programming se code **readable, maintainable, aur testable** banta hai:
- `data_manager.py` sirf file I/O aur backups handle karta hai.
- `calc_engine.py` basic totals aur balance nikalta hai.
- `budget_engine.py` aur `intelligence_engine.py` budget monitoring aur alert logic sambhalte hain.
- `views/` folder me har screen ka UI alag render function me encapsulated hai.
Is separation of concerns se team ke sabhi 5 members bina conflict ke alag-alag modules pe kaam kar sake aur unit tests likhna easy ho gaya.

---

### Q3. Aapne SQL database ke badle CSV aur JSON kyu use kiya?
**Answer:**
1. **Academic relevance:** Course "Computational Thinking & Programming" me core Python file handling concepts (`open()`, `csv.DictReader`, `json.dump`) demonstrate karne the.
2. **Portability:** External MySQL ya PostgreSQL server setup ki zarurat nahi hoti. Project ko kisi bhi machine pe bina database installation ke instant run kiya ja sakta hai.
3. **Data separation:** Tabular data (transactions) CSV me naturally fit hota hai, jabki hierarchical nested data (monthly category limits) JSON me perfectly structure hota hai.

---

## 🛡️ Section 2: Harsh's Assigned Contribution (Budget & Intelligence Logic)

### Q4. Harsh, aapka specific contribution kya tha is project me?
**Answer:** "Sir, mera primary contribution **Budget Monitoring and Alert Logic** design aur implement karna tha. Maine do core business logic modules banaye hain:
1. `modules/budget_engine.py`: Jo category-wise aur overall budget utilization calculate karta hai aur **70%, 90%, aur 100%** thresholds pe automated color-coded alerts generate karta hai.
2. `modules/intelligence_engine.py`: Jo daily burn rate calculate karke end-of-month spending predict karta hai, **Daily Safe-to-Spend limit** nikalta hai, aur ek explainable **Overspending Risk Index (0–100)** compute karta hai."

---

### Q5. Aapne alert system ke liye exact kya thresholds choose kiye aur kyu?
**Answer:** Humne 4-tier threshold system implement kiya hai:
1. **Normal (< 70%):** Spending pace healthy hai, surplus bachega (Green badge).
2. **Spending Awareness (70% to < 90%):** User ko alert milta hai ki budget ka major hissa consume ho chuka hai (Amber Yellow badge).
3. **High Spending Warning (90% to < 100%):** Critical zone, user ko non-essential spending turant rokhne ki advice di jaati hai (Orange badge).
4. **Budget Exceeded (≥ 100%):** Limit breach ho chuki hai, deficit alert activate hota hai aur safe daily spending ₹0/day lock ho jati hai (Crimson Red badge).

---

### Q6. Budget Utilization calculate karne ka formula kya hai?
**Answer:**
$$\text{Utilization \%} = \left(\frac{\text{Actual Spent}}{\text{Allocated Budget}}\right) \times 100$$
**Example:** Agar Food ka budget ₹5,000 hai aur actual kharcha ₹4,500 hua:
$$\text{Utilization} = \left(\frac{4500}{5000}\right) \times 100 = 90.0\%$$
Status trigger hoga: **"High Spending Warning"** (kyunki 90% boundary hit ho gayi).

---

### Q7. Agar kisi category ka budget ₹0 ho aur user usme kharcha kar de, toh aapka code crash hoga ya nahi?
**Answer:** Nahi sir, bilkul crash nahi hoga. Humne defensive programming use karke is edge case ko handle kiya hai:
```python
if b <= 0.0:
    if s == 0.0:
        return (0.0, "Unbudgeted")
    else:
        return (None, "Unbudgeted Spend")
```
Division perform hi nahi hota, isliye `ZeroDivisionError` nahi aata. Sath hi hum isse false "Budget Exceeded" alert bhi nahi dikhate, balki separately report karte hain ki yeh category unbudgeted hai.

---

### Q8. Average Daily Spending (Burn Rate) kaise calculate hota hai?
**Answer:**
$$\text{Average Daily Spend} = \frac{\text{Month-to-Date Expenses}}{\text{Days Elapsed}}$$
**Example:** Agar month ke first 15 days me total kharcha ₹15,000 hua:
$$\text{Average Daily Spend} = \frac{15000}{15} = ₹1,000.00/\text{day}$$

---

### Q9. Month-End Expense Forecast kaise nikalte hain?
**Answer:**
$$\text{Projected Monthly Expenses} = \text{Average Daily Spend} \times \text{Total Days in Month}$$
Continuing the previous example (30-day month):
$$\text{Forecast} = 1000 \times 30 = ₹30,000.00$$
Agar allocated budget ₹25,000 tha, toh projected overspending hogi:
$$\text{Projected Overspending} = \max(0, 30000 - 25000) = ₹5,000.00$$

---

### Q10. Safe Daily Spending limit ka formula kya hai aur budget exceed hone par kya hota hai?
**Answer:**
$$\text{Remaining Budget} = \text{Monthly Budget} - \text{Incurred Expenses}$$
$$\text{Remaining Days} = \text{Total Days in Month} - \text{Current Day} + 1$$
$$\text{Safe Daily Spend} = \frac{\text{Remaining Budget}}{\text{Remaining Days}}$$
**Strict Rule:** Agar budget already exceed ho gaya hai ($\text{Remaining Budget} \le 0$), toh formula division nahi karta balki strictly **₹0.00/day** return karta hai, taaki user ko clear message mile ki ab discretionary kharcha nahi kiya ja sakta.

---

### Q11. Overspending Risk Index kya hai? Kya yeh Machine Learning hai?
**Answer:** Sir, yeh bilkul **Machine Learning nahi hai**. Yeh ek **deterministic, rule-based computational metric** hai:
$$\text{Risk Score} = \min\left(100, \max\left(0, \text{round}\left( \frac{\text{Projected Expenses}}{\text{Monthly Budget}} \times 100 \right)\right)\right)$$
- 0 to 69: Low Risk
- 70 to 89: Moderate Risk
- 90 to 99: High Risk
- 100: Critical Risk (Forecast budget se match ya exceed kar raha hai).
Yeh financial loss ki probability nahi hai, balki budget ceiling exhaustion ka transparent measurement hai.

---

### Q12. February me leap year ka issue aapne kaise solve kiya?
**Answer:** Hardcoded 30 ya 31 days lene ke bajaye humne Python ki standard `calendar` library use ki hai:
```python
import calendar
_, total_days = calendar.monthrange(year, month)
```
`calendar.monthrange(2024, 2)` automatically 29 days return karta hai, jabki `calendar.monthrange(2026, 2)` 28 days return karta hai. Isse leap year me forecast bilkul accurate rehta hai.

---

### Q13. Agar user historical (pichle) month ka data dekhe, toh forecast kaise react karega?
**Answer:** `get_month_calendar_context` function check karta hai:
Agar selected month current calendar month se pehle ka hai, toh `is_past = True` flag set hota hai. Historical months ke liye future projection disabled rehti hai aur actual incurred expense hi final amount ke roop me display hoti hai, kyunki beete hue mahine me future burn rate ka koi concept nahi hota.

---

## 🐍 Section 3: Python Concepts & Language Fundamentals

### Q14. Python me mutable aur immutable data types me kya farak hai? Project me kahan use hue?
**Answer:**
- **Mutable:** Jinhe create karne ke baad modify kiya ja sakta hai (e.g., `list`, `dict`, `set`). Project me `transactions` list aur `category_budgets` dictionary mutable hain.
- **Immutable:** Jinhe modify nahi kiya ja sakta (e.g., `int`, `float`, `str`, `tuple`). Project me function se return hone wale `(utilization, status)` tuples aur constants immutable hain.

---

### Q15. Dictionary aur List me retrieval complexity me kya difference hai?
**Answer:**
- Dictionary hash table implementation use karti hai, isliye key se value fetch karna average $O(1)$ time complexity leta hai (e.g., `category_budgets["Food"]`).
- List me kisi element ko dhoondne ke liye linear search hota hai, jisme $O(N)$ time lagta hai. Isliye humne category budgets ke lookup ke liye dictionary use ki.

---

### Q16. `with open(...)` context manager use karne ka kya benefit hai?
**Answer:** `with open(...)` Python ka context management protocol (`__enter__` aur `__exit__`) follow karta hai. Iska sabse bada benefit yeh hai ki chahe block ke andar koi exception ya error bhi aa jaye, file stream safely aur automatically close ho jati hai, jisse memory leak ya file corruption nahi hota.

---

### Q17. `csv.DictReader` normal `csv.reader` se kaise different hai?
**Answer:**
- `csv.reader` har row ko list of strings ke roop me deta hai, jisme hume column access karne ke liye index yaad rakhna padta hai (jaise `row[4]`).
- `csv.DictReader` pehli line ko header mankar har row ko ek Python dictionary bana deta hai (jaise `row['amount']` ya `row['category']`), jisse code readable aur self-explanatory ho jata hai.

---

### Q18. Project me `try-except` blocks kahan aur kyu lagaye gaye hain?
**Answer:** Defensive programming ke liye teen primary jagaho pe `try-except` use hua hai:
1. `modules/data_manager.py`: File read/write ke time agar file missing ya corrupted ho toh application crash hone ke bajaye empty list ya error return kare.
2. `modules/calc_engine.py`: User input amount ko `float()` me convert karte waqt `ValueError` ko catch karne ke liye.
3. `calculate_savings_rate()`: Agar total income ₹0 ho toh `ZeroDivisionError` ko intercept karke `0.0%` return karne ke liye.

---

### Q19. Python me Lambda function kya hota hai aur project me kahan use hua?
**Answer:** Lambda ek anonymous, inline function hota hai jisme single expression evaluate hoti hai.
Project me categories ko unke spent amount ke hisaab se descending order me sort karne ke liye lambda use kiya gaya hai:
```python
# From modules/budget_engine.py
ranked.sort(key=lambda item: item["spent"], reverse=True)
```

---

### Q20. List comprehension kya hoti hai? Ek code example dein jo aapke project me ho.
**Answer:** List comprehension Python me existing iterable se nayi list create karne ka concise syntax hai.
Example from `modules/intelligence_engine.py`:
```python
expense_txns = [t for t in month_txns if t.get("type") == "Expense"]
```
Yeh normal 4-line `for` loop aur `if` condition ko ek hi clean line me execute karta hai.

---

### Q21. `*args` aur `**kwargs` me kya farak hai?
**Answer:**
- `*args` variable number of non-keyword (positional) arguments ko as a tuple accept karta hai.
- `**kwargs` variable number of keyword arguments ko as a dictionary accept karta hai.

---

### Q22. Project me `set` data structure kahan use hua hai?
**Answer:** `modules/calc_engine.py` ke `get_available_months()` function me:
```python
months = set()
for txn in transactions:
    d = txn.get("date", "")
    if len(d) >= 7 and d[4] == "-":
        months.add(d[:7])
```
Transactions me hazaron rows ho sakti hain jisme dates repeat hoti hain. `set` automatically duplicate months ko discard kar deta hai, jisse hume unique `YYYY-MM` list milti hai dropdown ke liye.

---

## 🧪 Section 4: Testing & Quality Assurance

### Q23. Aapne automated testing ke liye kaunsa tool use kiya aur kitne tests likhe?
**Answer:** Humne Python ka built-in `unittest` module use kiya hai. Poore project me total **51 unit test cases** likhe gaye hain across 5 modules (`test_calculations.py`, `test_data_manager.py`, `test_budget_engine.py`, `test_intelligence_engine.py`, aur `test_multi_user.py`). Sabhi 51 tests pass hote hain with 0 failures and 0 errors.

---

### Q24. Boundary value testing ka ek example bataiye jo aapne budget alerts me test kiya.
**Answer:** Threshold boundaries pe off-by-one errors common hote hain. Humne exact boundaries test ki hain:
- `69.9%` utilization $\to$ `Normal`
- `70.0%` utilization $\to$ `Spending Awareness`
- `89.9%` utilization $\to$ `Spending Awareness`
- `90.0%` utilization $\to$ `High Spending Warning`
- `99.9%` utilization $\to$ `High Spending Warning`
- `100.0%` utilization $\to$ `Budget Exceeded`
- `120.0%` utilization $\to$ `Budget Exceeded`

---

### Q25. Aapne Streamlit app ko bina browser open kiye kaise test kiya?
**Answer:** Streamlit ka modern headless testing framework `AppTest` use karke:
```python
from streamlit.testing.v1 import AppTest
at = AppTest.from_file('app.py')
at.run()
assert not at.exception
```
Isse saari 8 navigation pages programmatically simulate hoti hain aur render exceptions check ho jaate hain.

---

## 💼 Section 5: Teamwork, Roles & Soft Skills

### Q26. Team ke baaki 4 members ka kya role tha?
**Answer:**
- **Ridhima (`S26CSEU1925`):** Transaction recording workflow aur input form validations.
- **Anoushka (`S26CSEU1922`):** Project documentation, reports aur data manager backup routines.
- **AATIRTH (`S26CSEU1913`):** Core calculation engine (Income, expense, balance, savings rate) aur INR formatter.
- **SRISHTHI (`S26CSEU1939`):** Spending analytics, interactive Plotly charts, aur UI styling.

---

### Q27. Agar user galti se apna saara data clear kar de, toh kya data recover ho sakta hai?
**Answer:** Haan sir, bilkul! Humne `modules/data_manager.py` me `clear_all_data()` aur `load_sample_dataset()` execute hone se pehle automated snapshot backup mechanism lagaya hai:
```python
backup_data()  # data/backups/ folder me timestamped copy save ho jati hai
```
User Reports tab me jaakar stored backups ko inspect aur restore kar sakta hai.

---

### Q28. Future me is project me kya add kiya ja sakta hai?
**Answer:**
1. Multi-currency conversion (USD, EUR, GBP) using fixed conversion tables.
2. Recurring expense reminders (jaise monthly Wi-Fi bill ya room rent).
3. Automated monthly summary report downloadable as a formatted PDF.

---

### Q29. Agar viva me examiner bole "Mujhe code run karke dikhao", toh step-by-step kya karoge?
**Answer:**
1. Terminal open karke project directory me navigate karenge: `cd SpendWise_Project`
2. Virtual environment activate karenge: `source .venv/bin/activate`
3. Tests run karke verify karenge: `python3 -m unittest discover tests -v` (All 51 tests pass)
4. Streamlit dashboard launch karenge: `streamlit run app.py`
5. Browser me authentication page load hogi:
   - Team member select karenge (jaise Harsh: `S26CSEU1935`, PIN: `Harsh@1935`).
   - Log in karke personal dashboard open hoga.
   - Lead Admin role hone ki wajah se "Admin Console" bhi visible hoga jisme team management aur audit logs dikha sakte hain.

---

### Q30. Multi-user architecture me privacy aur data isolation kaise ensure kiya gaya hai?
**Answer:**
Humne SQLite me row-level security implement ki hai.
1. `transactions` aur `budgets` tables me `user_id INTEGER NOT NULL` foreign key column hai.
2. Sabhi database queries me strictly `WHERE user_id = ?` filter enforced hai.
3. Kisi bhi user ko doosre user ki financial records ka access nahi milta.
4. Agar User B attack karke User A ka transaction ID pass karke update ya delete karne ki koshish kare, toh query 0 rows match karti hai aur transaction block ho jati hai. Yeh `tests/test_multi_user.py` me automate karke mathematically prove kiya gaya hai.

---

### Q31. Passwords ko secure rakhne ke liye kaunsa cryptographic mechanism use kiya hai?
**Answer:**
Humne industry standard **PBKDF2-HMAC-SHA256** use kiya hai:
1. Har password ke liye 16-byte cryptographically secure random salt generate hota hai (`os.urandom(16)`).
2. Key derivation me **260,000 iterations** run hoti hain brute-force attacks ko prevent karne ke liye.
3. Verification constant-time comparison (`hmac.compare_digest`) se hoti hai taaki timing side-channel attacks na ho sakein.
4. Database me plaintext passwords kabhi save nahi hote.
