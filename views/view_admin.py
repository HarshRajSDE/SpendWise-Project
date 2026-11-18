"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_admin.py
Description: Restricted Team Administration & Security Console.
             Provides user management, status toggling, PBKDF2 password resets,
             and security audit logs without exposing private user financial ledgers.
Institution: Bennett University (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
from datetime import datetime
from modules.database import (
    get_all_users,
    update_user_password,
    set_user_active_status,
    get_audit_logs,
    get_db_connection
)
from modules.calc_engine import format_inr


def render():
    current_user = st.session_state.get("user", {})
    if current_user.get("role") != "admin":
        st.error("⛔ Access Denied: This administrative panel is restricted to authorized project leads.")
        st.info("Your current account role does not have administrative privileges.")
        return

    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h1 class="hero-title">Team Administration Console</h1>
        <div class="hero-subtitle">Authorized team roster management, account credential resets, and system security telemetry.</div>
    </div>
    """, unsafe_allow_html=True)

    users = get_all_users()
    active_count = sum(1 for u in users if u["is_active"])

    # --- TOP TELEMETRY CARDS ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title"><span>TEAM ROSTER</span><span>👥</span></div>
            <div class="kpi-value purple">{len(users)}</div>
            <div class="kpi-subtext">Bennett University CSAE100</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title"><span>ACTIVE ACCOUNTS</span><span>✅</span></div>
            <div class="kpi-value green">{active_count}</div>
            <div class="kpi-subtext">Authorized to sign in</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>CRYPTO CIPHER</span><span>🛡️</span></div>
            <div class="kpi-value" style="font-size:1.1rem; color:#B66DFF; margin-top:8px;">PBKDF2-260K</div>
            <div class="kpi-subtext">HMAC-SHA256 Salted</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>DATA PRIVACY</span><span>🔒</span></div>
            <div class="kpi-value" style="font-size:1.1rem; color:#35D49A; margin-top:8px;">Row-Level Zero-Leak</div>
            <div class="kpi-subtext">Strict Owner Isolation</div>
        </div>
        """, unsafe_allow_html=True)

    tab_roster, tab_reset, tab_audit, tab_legacy = st.tabs([
        "👥 Team Member Roster",
        "🔑 Password Reset Workflow",
        "🛡️ System Audit Logs",
        "📦 Legacy Data Quarantine"
    ])

    # ==========================================================================
    # TAB 1: TEAM MEMBER ROSTER
    # ==========================================================================
    with tab_roster:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">Official Project Team Roster</h3>
            <p style="color:#A69BBE; font-size:0.88rem;">
                Manage authorized student team accounts extracted from the course project report.
                Toggle account status or verify enrollment credentials.
            </p>
        </div>
        """, unsafe_allow_html=True)

        for member in users:
            uid = member["id"]
            name = member["full_name"]
            enroll = member["enrollment_no"]
            role = member["role"]
            is_active = member["is_active"]
            contrib = member.get("contribution") or "Team Member"
            last_log = member.get("last_login") or "Never"
            if last_log != "Never":
                try:
                    last_log = datetime.fromisoformat(last_log).strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    pass

            status_badge = '<span class="badge-safe">Active</span>' if is_active else '<span class="badge-danger">Deactivated</span>'
            role_badge = '<span class="badge-warning">Lead / Admin</span>' if role == "admin" else '<span class="badge-info">Member</span>'

            col_m1, col_m2 = st.columns([3.5, 1.2])
            with col_m1:
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #1D1733 0%, #171128 100%); border: 1px solid #2E2248; border-radius: 12px; padding: 0.95rem 1.15rem; margin-bottom: 0.75rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px;">
                        <strong style="color:#FFFFFF; font-size:1rem;">{name}</strong>
                        <div style="display:flex; gap:6px;">
                            {role_badge}
                            {status_badge}
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:#B66DFF; font-family:monospace; margin-bottom: 4px;">
                        Enrollment: {enroll} • Bennett University
                    </div>
                    <div style="font-size:0.78rem; color:#A69BBE;">
                        <strong>Role:</strong> {contrib}
                    </div>
                    <div style="font-size:0.72rem; color:#7B7192; margin-top:4px;">
                        Last Login: {last_log}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_m2:
                # Prevent admin from deactivating themselves
                if uid == current_user.get("id"):
                    st.caption("Current User (Admin)")
                else:
                    action_label = "Deactivate" if is_active else "Reactivate"
                    btn_type = "secondary" if is_active else "primary"
                    if st.button(f"{action_label} Account", key=f"btn_toggle_status_{uid}", type=btn_type, use_container_width=True):
                        set_user_active_status(uid, not is_active, current_user.get("id"))
                        st.success(f"Updated status for {name} to {'Active' if not is_active else 'Deactivated'}.")
                        st.rerun()

    # ==========================================================================
    # TAB 2: PASSWORD RESET WORKFLOW
    # ==========================================================================
    with tab_reset:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">Admin-Controlled Password Reset</h3>
            <p style="color:#A69BBE; font-size:0.88rem;">
                Securely reset passwords for team members using PBKDF2-HMAC-SHA256 with 260,000 iterations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        user_map = {f"{u['full_name']} ({u['enrollment_no']})": u["id"] for u in users}
        selected_user_label = st.selectbox("Select Team Member to Reset:", options=list(user_map.keys()))
        target_uid = user_map[selected_user_label]

        with st.form("admin_pwd_reset_form"):
            new_pwd = st.text_input("New Secure Password / PIN", type="password", placeholder="At least 6 characters")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            submit_reset = st.form_submit_button("🔑 Reset Password Now", use_container_width=True)

        if submit_reset:
            if not new_pwd or len(new_pwd) < 6:
                st.error("Password must be at least 6 characters long.")
            elif new_pwd != confirm_pwd:
                st.error("Passwords do not match.")
            else:
                success = update_user_password(target_uid, new_pwd, admin_user_id=current_user.get("id"))
                if success:
                    st.success(f"Password reset successfully for {selected_user_label}!")
                else:
                    st.error("Failed to update password. Please check database logs.")

    # ==========================================================================
    # TAB 3: SYSTEM AUDIT LOGS
    # ==========================================================================
    with tab_audit:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">Security & Authentication Audit Trail</h3>
            <p style="color:#A69BBE; font-size:0.88rem;">
                Immutable log of login attempts, password changes, and account administrative actions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        logs = get_audit_logs(limit=30)
        if not logs:
            st.info("No audit logs recorded yet.")
        else:
            for l in logs:
                ts = l.get("timestamp", "")
                try:
                    ts = datetime.fromisoformat(ts).strftime("%d %b %Y, %I:%M:%S %p")
                except Exception:
                    pass

                user_tag = f"{l['full_name']} ({l['enrollment_no']})" if l.get("full_name") else "System / Anonymous"
                action = l["action"]

                color = "#35D49A" if "SUCCESS" in action else ("#FF5478" if "FAILED" in action or "REJECTED" in action else "#B66DFF")

                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0.85rem; background:rgba(33, 22, 56, 0.6); border:1px solid #2E2248; border-radius:8px; margin-bottom:6px; font-size:0.82rem;">
                    <div>
                        <strong style="color:{color};">{action}</strong> • <span style="color:#FFFFFF;">{user_tag}</span>
                        <div style="font-size:0.75rem; color:#A69BBE; margin-top:2px;">{l.get('details', '')}</div>
                    </div>
                    <div style="color:#7B7192; font-size:0.72rem; white-space:nowrap; font-family:monospace;">
                        {ts}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================================================
    # TAB 4: LEGACY DATA QUARANTINE
    # ==========================================================================
    with tab_legacy:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top:0; color:#FFFFFF; font-size:1.15rem;">Legacy Data Quarantine & Privacy Boundary</h3>
            <p style="color:#A69BBE; font-size:0.88rem;">
                Historical demo and single-user transactions are isolated in a quarantine area.
                In strict accordance with project security guidelines, administrators cannot view or
                unilaterally inspect other members' private ledgers.
            </p>
        </div>
        """, unsafe_allow_html=True)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM legacy_transactions;")
        row = cursor.fetchone()
        legacy_count = row["cnt"] if row else 0
        conn.close()

        st.metric("Quarantined Legacy Records", f"{legacy_count} records", help="Historical records safely archived before multi-user migration.")
