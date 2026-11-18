"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_about.py
Description: Academic & Team Documentation View.
Institution: Bennett University
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
from config import (
    PROJECT_NAME,
    COURSE_NAME,
    COURSE_CODE,
    ACADEMIC_YEAR,
    TEAM_MEMBERS,
    THRESHOLD_SAFE,
    THRESHOLD_WARNING,
    THRESHOLD_CRITICAL,
    COLORS
)


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">About SpendWise</h1>
        <div class="hero-subtitle">Academic project details, team member contributions, and architectural notes.</div>
    </div>
    """, unsafe_allow_html=True)

    # --- SECTION 1: BENNETT UNIVERSITY & COURSE METADATA ---
    st.markdown(f"""
    <div class="content-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom: 1rem;">
            <div>
                <h3 style="margin:0; font-size:1.35rem; color:#FFFFFF;">🏛️ Bennett University</h3>
                <span style="color:#10B981; font-weight:600; font-size:0.85rem;">School of Computer Science Engineering and Technology</span>
            </div>
            <div>
                <span class="badge-safe">{ACADEMIC_YEAR}</span>
            </div>
        </div>
        <table style="width:100%; border-collapse: collapse; font-size: 0.92rem; box-sizing: border-box;">
            <tr><td style="padding: 7px 0; color: #94A3B8; width: 35%; min-width: 120px; max-width: 180px;">Project Title:</td><td style="word-break: break-word;"><strong>{PROJECT_NAME}</strong></td></tr>
            <tr><td style="padding: 7px 0; color: #94A3B8;">Course:</td><td style="word-break: break-word;"><strong>{COURSE_NAME}</strong></td></tr>
            <tr><td style="padding: 7px 0; color: #94A3B8;">Course Code:</td><td><code>{COURSE_CODE}</code></td></tr>
            <tr><td style="padding: 7px 0; color: #94A3B8;">Tech Stack:</td><td style="word-break: break-word;">Python 3.10+, Streamlit, Plotly, CSV & JSON Persistence</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # --- SECTION 2: PROJECT OBJECTIVES ---
    st.subheader("🎯 Project Objectives & Philosophy")
    st.markdown("""
    1. **Democratize Financial Awareness**: Provide college students with an intuitive, self-hosted tool to track pocket money, stipends, and expenses.
    2. **Transparent Computational Intelligence**: Replace opaque machine learning with mathematically provable formulas (safe daily spending, burn rates, and run-rate projections).
    3. **Zero-Vendor Lock-In**: Store transactions locally in transparent CSV format and budget configurations in JSON, requiring zero paid external APIs or database servers.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 3: TEAM MEMBERS & ASSIGNED CONTRIBUTIONS ---
    st.subheader("👥 Project Team & Core Responsibilities")

    for member in TEAM_MEMBERS:
        is_user = "HARSH" in member["name"].upper()
        card_border = "#10B981" if is_user else "#283756"
        badge = "⭐ Primary Assigned Contribution" if is_user else "Team Member"
        badge_class = "badge-safe" if is_user else "badge-info"

        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1C2541 0%, #151D33 100%); border: 1.5px solid {card_border}; border-radius: 12px; padding: 1.1rem 1.35rem; margin-bottom: 0.75rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            <div style="display:flex; justify-content: space-between; align-items:center; flex-wrap:wrap; gap:6px;">
                <div>
                    <strong style="font-size: 1.15rem; color: #FFFFFF;">{member['name']}</strong>
                    <span style="color: #00B4D8; margin-left: 10px; font-family:monospace; font-weight:600;">{member['id']}</span>
                </div>
                <span class="{badge_class}">{badge}</span>
            </div>
            <div style="margin-top: 0.45rem; color: #94A3B8; font-size: 0.92rem;">
                <strong>Assigned Contribution:</strong> {member['role']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 4: PYTHON CONCEPTS DEMONSTRATED (VIVA PREPARATION) ---
    st.subheader("🐍 Computational Concepts Demonstrated")
    with st.expander("📖 View Computational Thinking & Python Language Constructs (Viva Guide)", expanded=True):
        st.markdown("""
        - **File I/O & Serialization:** Context-managed atomic reading/writing using Python's standard `csv.DictReader`, `csv.DictWriter`, and `json.dump` / `json.load`.
        - **Defensive Error Handling:** Systematic `try/except` blocks handling `ZeroDivisionError`, `ValueError`, and file missing scenarios.
        - **Data Structures & Collections:** Nested dictionaries for category budgets, lists of dictionaries for tabular records, and set comprehensions for available months.
        - **Functional Programming & Lambdas:** Pure functions with explicit type signatures, deterministic returns, and lambda functions for multi-level sorting.
        - **Date Arithmetic & Calendars:** Dynamic calculation of month lengths, leap year adjustments, and elapsed days using Python's `calendar` and `datetime` libraries.
        - **Automated Unit Testing:** Full test suite implemented with Python's built-in `unittest` framework ensuring regression-free execution.
        """)
