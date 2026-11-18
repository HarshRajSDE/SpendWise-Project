# SpendWise – Installation & Local Execution Guide
## Step-by-Step Setup Instructions for Students & Evaluators

**Course:** Computational Thinking and Programming (`2026CSAE100`)  
**Institution:** Bennett University  
**Academic Year:** 2026–2027  

---

## 1. System Prerequisites

Before running **SpendWise**, ensure your machine has:
- **Operating System:** Windows 10/11, macOS (Intel or Apple Silicon), or Linux (Ubuntu, Debian, Fedora).
- **Python Version:** Python 3.9, 3.10, 3.11, or 3.12. (Check with `python3 --version` or `python --version`).
- **Disk Space:** Minimal (< 100 MB for dependencies).
- **Internet Access:** Only required once for initial `pip install`. All dashboard functionality runs 100% offline locally.

---

## 2. Step-by-Step Installation

### Step 1: Open Terminal / Command Prompt
Open your terminal application:
- **macOS:** Terminal or iTerm2
- **Windows:** PowerShell or Command Prompt (CMD)
- **Linux:** Bash terminal

Navigate to the project folder:
```bash
cd path/to/SpendWise_Project
```

---

### Step 2: Create a Virtual Environment
Isolating dependencies in a virtual environment prevents version conflicts with other Python projects on your system:

- **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **On Windows:**
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```

*(Your terminal prompt should now display `(.venv)` at the beginning of the line).*

---

### Step 3: Install Required Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

This installs:
- `streamlit>=1.30.0`
- `plotly>=5.18.0`
- `pandas>=2.0.0`

---

### Step 4: Run the Automated Unit Test Suite
Verify that all 44 automated tests pass before launching the application:
```bash
python -m unittest discover tests -v
```

Expected output:
```text
test_calculate_remaining_budget (test_budget_engine.TestBudgetEngine) ... ok
test_check_category_budget_details (test_budget_engine.TestBudgetEngine) ... ok
...
Ran 44 tests in 0.007s
OK
```

---

### Step 5: Launch the Streamlit Dashboard
Start the local web application:
```bash
streamlit run app.py
```

The terminal will display the active local URL:
```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser (Google Chrome, Microsoft Edge, Safari, or Firefox).

---

## 3. Initial App Exploration

1. **Clean Default State:** Upon first launch, the dashboard opens with an empty ledger.
2. **Load Demo Dataset:**
   - In the sidebar, click **"Reports and Data Management"**.
   - Click the green button: **"🚀 Load Sample Demo Data (INR ₹)"**.
   - Return to the **"Overview Dashboard"** or **"Smart Budget Intelligence"** to explore interactive charts, budget progress bars, and the risk gauge.
3. **Reset Database:**
   - Click **"🗑️ Reset All Data to Clean Empty State"** in Reports whenever you wish to clear test records. An automated backup is created first.

---

## 4. Troubleshooting Common Issues

### Issue 1: `Port 8501 is already in use`
**Cause:** Another Streamlit application or process is using port 8501.  
**Solution:** Specify an alternate port, such as 8502 or 8505:
```bash
streamlit run app.py --server.port 8502
```

### Issue 2: `ModuleNotFoundError: No module named 'streamlit'`
**Cause:** The virtual environment is either not activated or dependencies were not installed in the active environment.  
**Solution:**
```bash
source .venv/bin/activate    # (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

### Issue 3: Streamlit prompts for Email on First Launch
**Cause:** Streamlit's telemetry prompt.  
**Solution:** Press `Enter` to leave it blank, or configure `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = false

[server]
headless = true
```
