"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_settings.py
Description: Premium Fintech SaaS Settings & Configuration View.
             Enables workspace preferences, academic profile inspection,
             budget threshold validation, theme telemetry, and system diagnostics.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
import os
from config import (
    PROJECT_NAME,
    COURSE_NAME,
    COURSE_CODE,
    ACADEMIC_YEAR,
    THRESHOLD_SAFE,
    THRESHOLD_WARNING,
    THRESHOLD_CRITICAL,
    DATA_DIR,
    BACKUPS_DIR,
    TRANSACTIONS_FILE,
    BUDGET_FILE,
    COLORS
)
from modules.data_manager import load_transactions, load_budget, backup_data
from modules.calc_engine import format_inr, calculate_total_income, calculate_total_expenses, calculate_net_balance


def render():
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">System & Workspace Settings</h1>
        <div class="hero-subtitle">Manage preferences, fiscal parameters, academic credentials, and database telemetry.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_profile, tab_budget, tab_theme, tab_sys = st.tabs([
        "👤 User & Academic Profile",
        "🛡️ Thresholds & Limits",
        "🎨 Appearance & Theme",
        "⚙️ Diagnostics & Storage"
    ])

    # ==========================================================================
    # TAB 1: USER & ACADEMIC PROFILE
    # ==========================================================================
    with tab_profile:
        current_user = st.session_state.get("user", {})
        u_name = current_user.get("full_name", "Harsh")
        u_enroll = current_user.get("enrollment_no", "S26CSEU1935")
        u_role = "Team Lead / Admin" if current_user.get("role") == "admin" else "Team Member"
        u_contrib = current_user.get("contribution", "Budget Monitoring & Alert Logic")

        parts = u_name.strip().split()
        if len(parts) >= 2:
            initials = (parts[0][0] + parts[1][0]).upper()
        elif len(parts) == 1 and len(parts[0]) >= 2:
            initials = parts[0][:2].upper()
        else:
            initials = "SW"

        st.markdown(f"""
        <div class="content-card">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:1.25rem;">
                <div style="width:54px; height:54px; border-radius:50%; background:linear-gradient(135deg, #9147FF 0%, #B66DFF 100%); display:flex; align-items:center; justify-content:center; font-size:1.4rem; font-weight:800; color:#FFFFFF; box-shadow:0 0 16px rgba(145, 71, 255, 0.4);">
                    {initials}
                </div>
                <div>
                    <h3 style="margin:0; font-size:1.3rem; color:#FFFFFF;">{u_name}</h3>
                    <div style="font-size:0.85rem; color:#B66DFF; font-weight:600;">{u_role} • {u_contrib}</div>
                    <div style="font-size:0.78rem; color:#A69BBE;">Enrollment: <code>{u_enroll}</code> • School of CSE, Bennett University</div>
                </div>
            </div>
            <table style="width:100%; border-collapse:collapse; font-size:0.9rem; border-top:1px solid #283756; box-sizing:border-box;">
                <tr><td style="padding:10px 0; color:#A69BBE; width:35%; min-width:120px; max-width:180px;">Institution:</td><td style="word-break:break-word;"><strong>Bennett University</strong> (Times Group)</td></tr>
                <tr><td style="padding:10px 0; color:#A69BBE;">Course:</td><td style="word-break:break-word;"><strong>{COURSE_NAME}</strong></td></tr>
                <tr><td style="padding:10px 0; color:#A69BBE;">Course Code:</td><td><code>{COURSE_CODE}</code></td></tr>
                <tr><td style="padding:10px 0; color:#A69BBE;">Academic Year:</td><td><strong>{ACADEMIC_YEAR}</strong></td></tr>
                <tr><td style="padding:10px 0; color:#A69BBE;">Architecture Tier:</td><td style="word-break:break-word;"><strong>Multi-User Cryptographic Financial Architecture</strong> (SQLite Row-Isolation, PBKDF2)</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Team Collaboration Roster")
        roster_members = [
            ("Ridhima", "S26CSEU1925", "Expense Tracking & Input Validation"),
            ("Anoushka", "S26CSEU1922", "Data Persistence & Report Organization"),
            ("Aatirth", "S26CSEU1913", "Calculation Engine & Financial Logic"),
            ("Harsh", "S26CSEU1935", "Budget Monitoring & Alert Engine (Lead)"),
            ("Srishthi", "S26CSEU1939", "Visual Analytics & Reporting")
        ]

        roster_cards = ""
        for name, enroll, role_desc in roster_members:
            is_active = (u_enroll.upper() == enroll.upper())
            card_border = "rgba(182, 109, 255, 0.45)" if is_active else "#283756"
            glow = "box-shadow:0 0 10px rgba(145, 71, 255, 0.25);" if is_active else ""
            badge = '<span class="badge-safe" style="font-size:0.7rem; margin-left:6px;">You</span>' if is_active else ""
            name_color = "#B66DFF" if is_active else "#FFFFFF"
            roster_cards += f"""
            <div style="background:rgba(33, 22, 56, 0.6); border:1px solid {card_border}; border-radius:10px; padding:12px 14px; {glow}">
                <strong style="color:{name_color};">{name}</strong> <code style="color:#B66DFF;">{enroll}</code> {badge}
                <div style="font-size:0.78rem; color:#A69BBE; margin-top:3px;">{role_desc}</div>
            </div>
            """

        st.markdown(f"""
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-top:0.5rem;">
            {roster_cards}
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 2: THRESHOLDS & BUDGET LIMITS
    # ==========================================================================
    with tab_budget:
        st.markdown(f"""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">🛡️ Canonical Threshold Policy (Harsh's Module)</h3>
            <p style="color:#A69BBE; font-size:0.9rem;">
                SpendWise strictly enforces a deterministic 3-boundary, 4-tier spending classification scheme
                applied uniformly across all categories and aggregate monthly envelopes.
            </p>
            <div style="display:flex; flex-direction:column; gap:10px; margin-top:1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:rgba(16, 185, 129, 0.08); border-left:4px solid #10B981; border-radius:8px;">
                    <div>
                        <strong style="color:#10B981;">Tier 1: Normal Spending</strong>
                        <div style="font-size:0.78rem; color:#A69BBE;">Utilization below 70.0% of allocated budget limit.</div>
                    </div>
                    <span class="badge-safe">&lt; {int(THRESHOLD_SAFE*100)}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:rgba(245, 158, 11, 0.08); border-left:4px solid #F59E0B; border-radius:8px;">
                    <div>
                        <strong style="color:#F59E0B;">Tier 2: Spending Awareness</strong>
                        <div style="font-size:0.78rem; color:#A69BBE;">Utilization between 70.0% and 89.9%. Advises expense pacing.</div>
                    </div>
                    <span class="badge-warning">{int(THRESHOLD_SAFE*100)}% – {int(THRESHOLD_WARNING*100 - 1)}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:rgba(249, 115, 22, 0.08); border-left:4px solid #F97316; border-radius:8px;">
                    <div>
                        <strong style="color:#F97316;">Tier 3: High Spending Warning</strong>
                        <div style="font-size:0.78rem; color:#A69BBE;">Utilization between 90.0% and 99.9%. Critical ceiling proximity.</div>
                    </div>
                    <span style="background:rgba(249, 115, 22, 0.15); color:#F97316; padding:4px 10px; border-radius:6px; font-size:0.78rem; font-weight:600;">{int(THRESHOLD_WARNING*100)}% – {int(THRESHOLD_CRITICAL*100 - 1)}%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; background:rgba(239, 68, 68, 0.08); border-left:4px solid #EF4444; border-radius:8px;">
                    <div>
                        <strong style="color:#EF4444;">Tier 4: Budget Exceeded</strong>
                        <div style="font-size:0.78rem; color:#A69BBE;">Utilization at or exceeding 100.0%. Overdraft deficit alert triggered.</div>
                    </div>
                    <span class="badge-danger">≥ {int(THRESHOLD_CRITICAL*100)}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 3: APPEARANCE & THEME
    # ==========================================================================
    with tab_theme:
        st.markdown(f"""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">🎨 Luxury Fintech Purple & Deep Navy Design System</h3>
            <p style="color:#A69BBE; font-size:0.9rem;">
                Custom high-contrast dark theme with violet illumination, smooth Lucide vector icons,
                and micro-interactions calibrated for professional demonstration.
            </p>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-top:1.25rem;">
                <div style="padding:14px; background:#100B20; border:1px solid #283756; border-radius:10px;">
                    <div style="width:24px; height:24px; border-radius:6px; background:#100B20; border:1px solid #4C1D95; margin-bottom:8px;"></div>
                    <strong style="font-size:0.85rem; color:#FFFFFF;">Canvas Background</strong>
                    <div style="font-size:0.75rem; color:#A69BBE;"><code>#100B20</code></div>
                </div>
                <div style="padding:14px; background:#171128; border:1px solid #283756; border-radius:10px;">
                    <div style="width:24px; height:24px; border-radius:6px; background:#171128; border:1px solid #4C1D95; margin-bottom:8px;"></div>
                    <strong style="font-size:0.85rem; color:#FFFFFF;">Sidebar Container</strong>
                    <div style="font-size:0.75rem; color:#A69BBE;"><code>#171128</code></div>
                </div>
                <div style="padding:14px; background:#211638; border:1px solid #283756; border-radius:10px;">
                    <div style="width:24px; height:24px; border-radius:6px; background:#211638; border:1px solid #9147FF; margin-bottom:8px;"></div>
                    <strong style="font-size:0.85rem; color:#FFFFFF;">Card Elevated</strong>
                    <div style="font-size:0.75rem; color:#A69BBE;"><code>#211638</code></div>
                </div>
                <div style="padding:14px; background:#211638; border:1px solid rgba(145, 71, 255, 0.4); border-radius:10px;">
                    <div style="width:24px; height:24px; border-radius:6px; background:linear-gradient(135deg, #9147FF, #B66DFF); margin-bottom:8px; box-shadow:0 0 10px #9147FF;"></div>
                    <strong style="font-size:0.85rem; color:#B66DFF;">Electric Violet Accent</strong>
                    <div style="font-size:0.75rem; color:#A69BBE;"><code>#9147FF • #B66DFF</code></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 4: DIAGNOSTICS & STORAGE
    # ==========================================================================
    with tab_sys:
        txns = load_transactions()
        budget = load_budget()
        t_inc = calculate_total_income(txns)
        t_exp = calculate_total_expenses(txns)
        bal = calculate_net_balance(t_inc, t_exp)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Stored Transactions", f"{len(txns)} records")
        c2.metric("Cumulative Inflow", format_inr(t_inc))
        c3.metric("Cumulative Outflow", format_inr(t_exp))
        c4.metric("Net Liquidity", format_inr(bal))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">📁 Storage File Integrity</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.9rem;">
                <tr>
                    <td style="padding:8px 0; color:#A69BBE; width:220px;">Transactions Path:</td>
                    <td><code>{TRANSACTIONS_FILE}</code></td>
                    <td><span class="badge-safe">{'Ready' if os.path.exists(TRANSACTIONS_FILE) else 'Missing'}</span></td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#A69BBE;">Budget Settings Path:</td>
                    <td><code>{BUDGET_FILE}</code></td>
                    <td><span class="badge-safe">{'Ready' if os.path.exists(BUDGET_FILE) else 'Missing'}</span></td>
                </tr>
                <tr>
                    <td style="padding:8px 0; color:#A69BBE;">Backups Directory:</td>
                    <td><code>{BACKUPS_DIR}</code></td>
                    <td><span class="badge-info">Active</span></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📦 Create Instant Database Snapshot Now", use_container_width=True):
            res = backup_data()
            if res.get("status") == "success":
                st.success(f"✅ Created instant backup snapshot: `{res.get('backup_folder')}`")
            else:
                st.error("Backup snapshot generation failed.")
