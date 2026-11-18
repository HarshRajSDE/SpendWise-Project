"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: config.py
Description: Central configuration file containing application constants,
             categories, file paths, budget thresholds, and styling themes.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import os

# ==============================================================================
# 1. ACADEMIC & PROJECT METADATA
# ==============================================================================
PROJECT_NAME = "SpendWise – Personal Expense and Budget Tracker"
COURSE_NAME = "Computational Thinking and Programming"
COURSE_CODE = "2026CSAE100"
ACADEMIC_YEAR = "2026–27"

TEAM_MEMBERS = [
    {"name": "Ridhima", "id": "S26CSEU1925", "role": "Transaction Recording & Input Validation"},
    {"name": "Anoushka", "id": "S26CSEU1922", "role": "Data Persistence, CSV & JSON Management"},
    {"name": "AATIRTH", "id": "S26CSEU1913", "role": "Core Financial Calculations & Aggregations"},
    {"name": "HARSH", "id": "S26CSEU1935", "role": "Budget Monitoring & Alert Threshold Logic (Assigned Focus)"},
    {"name": "SRISHTHI", "id": "S26CSEU1939", "role": "Visual Analytics & UI/UX Design"},
]

# ==============================================================================
# 2. FILE SYSTEM & STORAGE PATHS
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUPS_DIR = os.path.join(DATA_DIR, "backups")

TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.json")

# Ensure essential directories exist upon loading
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)

# Standard CSV Headers for Transactions
TRANSACTION_CSV_HEADERS = [
    "id",
    "date",
    "type",           # 'Income' or 'Expense'
    "category",
    "amount",
    "payment_mode",
    "description"
]

# ==============================================================================
# 3. CATEGORIES & TAXONOMIES
# ==============================================================================
EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Education",
    "Entertainment",
    "Bills",
    "Others"
]

INCOME_CATEGORIES = [
    "Salary",
    "Allowance / Pocket Money",
    "Freelance / Gig",
    "Scholarship",
    "Gifts / Bonus",
    "Investments",
    "Others"
]

PAYMENT_MODES = [
    "UPI (GPay / PhonePe / Paytm)",
    "Debit Card",
    "Credit Card",
    "Net Banking",
    "Cash"
]

# ==============================================================================
# 4. BUDGET ALERT THRESHOLDS (CORRECTED: 70%, 90%, 100%)
# ==============================================================================
# These thresholds define the tier levels for category and monthly budgets:
#   - Safe: Utilization < 70%
#   - Caution / Warning: 70% <= Utilization < 90%
#   - Critical / Danger: 90% <= Utilization <= 100%
#   - Exceeded: Utilization > 100%
THRESHOLD_SAFE = 0.70      # 70%
THRESHOLD_WARNING = 0.90   # 90%
THRESHOLD_CRITICAL = 1.00  # 100%

# ==============================================================================
# 5. UI/UX COLOR PALETTE (Modern Luxury Fintech: Dark Violet & Electric Purple)
# ==============================================================================
COLORS = {
    "bg_main": "#100B20",        # Dark luxury navy-purple
    "sidebar_bg": "#171128",     # Purple-tinted dark sidebar
    "card_bg": "#211638",        # Elevated dark violet
    "card_border": "#2E2248",    # Muted violet border
    "primary_purple": "#9147FF", # Vibrant electric purple
    "accent_violet": "#B66DFF",  # Luminous violet accent
    "accent_green": "#10B981",   # Emerald Green (Safe / Growth)
    "accent_cyan": "#38BDF8",    # Sky Blue for secondary highlights
    "warning_yellow": "#F59E0B", # Warm Amber for 70% threshold
    "danger_orange": "#F97316",  # Dark Orange for 90% threshold
    "danger_red": "#EF4444",     # Crimson Red for 100%+ threshold
    "text_main": "#FFFFFF",      # Crisp White
    "text_muted": "#A69BBE",     # Muted violet-gray
}
