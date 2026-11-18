"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: views/view_login.py
Description: Premium Glassmorphism Authentication View for Multi-User Personal
             Finance Platform. Enforces strict verification against the official
             5-member Bennett University team roster with PBKDF2 cryptography.
Institution: Bennett University
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st
from datetime import datetime
from modules.database import validate_login_credentials, OFFICIAL_TEAM_ROSTER
from modules.brand_logo import get_spendwise_icon_svg, _clean_markup


def render_login_page():
    """
    Renders the luxury fintech authentication screen.
    Only authorized Bennett University team members can log in.
    """
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <div style="display:inline-block; filter: drop-shadow(0 6px 20px rgba(145, 71, 255, 0.45)); margin-bottom: 0.75rem;">
    """ + get_spendwise_icon_svg(size=56, unique_id="login_hero") + """
        </div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1;">
            Spend<span style="background: linear-gradient(135deg, #9147FF 0%, #B66DFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Wise</span>
        </div>
        <div style="font-size: 0.88rem; color: #B66DFF; font-weight: 600; letter-spacing: 0.05em; margin-top: 4px;">
            MULTI-USER PERSONAL FINANCE PLATFORM
        </div>
        <div style="font-size: 0.78rem; color: #A69BBE; margin-top: 2px;">
            Bennett University • School of Computer Science Engineering • 2026CSAE100
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered Glassmorphism Login Container
    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        st.markdown("""
        <div style="background: linear-gradient(145deg, rgba(29, 23, 51, 0.9) 0%, rgba(21, 16, 38, 0.95) 100%); border: 1px solid rgba(145, 71, 255, 0.35); border-radius: 16px; padding: 1.5rem 1.75rem; box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(145, 71, 255, 0.15); backdrop-filter: blur(16px); margin-bottom: 1.25rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid rgba(46, 34, 72, 0.8); padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                <span style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF;">Authorized Team Login</span>
                <span style="background: rgba(53, 212, 154, 0.15); color: #35D49A; border: 1px solid rgba(53, 212, 154, 0.3); font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: 6px;">PBKDF2 Secured</span>
            </div>
        """, unsafe_allow_html=True)

        # Team member selection shortcut
        roster_options = ["-- Select Registered Member --"] + [
            f"{m['full_name']} ({m['enrollment_no']})" for m in OFFICIAL_TEAM_ROSTER
        ] + ["Manual / Custom Entry"]

        selected_member = st.selectbox(
            "Quick Select Member",
            options=roster_options,
            index=0,
            key="quick_select_member",
            help="Select your registered profile to auto-fill credentials."
        )

        default_name = ""
        default_enrollment = ""
        if selected_member and selected_member != "-- Select Registered Member --" and selected_member != "Manual / Custom Entry":
            for m in OFFICIAL_TEAM_ROSTER:
                if m["enrollment_no"] in selected_member:
                    default_name = m["full_name"]
                    default_enrollment = m["enrollment_no"]
                    break

        # Password visibility toggle outside the form for immediate response
        show_pwd = st.checkbox("Show Password / PIN", value=False, key="login_show_pwd")

        with st.form("spendwise_login_form", clear_on_submit=False):
            full_name = st.text_input(
                "Full Name",
                value=default_name,
                placeholder="e.g., Harsh Raj",
                help="Your full name as registered in the course project report."
            )

            enrollment_no = st.text_input(
                "Enrollment Number",
                value=default_enrollment,
                placeholder="e.g., S26CSEU1935",
                help="Your Bennett University enrollment ID."
            )

            password = st.text_input(
                "Password / Personal PIN",
                type="text" if show_pwd else "password",
                placeholder="••••••••••••",
                help="Your secure personal account password or PIN."
            )

            remember_session = st.checkbox(
                "Remember my session on this device",
                value=True,
                help="Maintains authentication state during your active browser tab."
            )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            submit_login = st.form_submit_button("🔐 Sign In to SpendWise", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if submit_login:
            # Validate credentials with clear feedback
            is_valid, message, user_dict = validate_login_credentials(
                enrollment_no=enrollment_no,
                password=password,
                full_name=full_name
            )

            if is_valid and user_dict:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_dict
                st.session_state["login_timestamp"] = datetime.now().isoformat()
                st.session_state["remember_session"] = remember_session
                st.success(f"{message} Loading personal dashboard...")
                st.rerun()
            else:
                st.error(f"⚠️ Authentication Error: {message}")

        # Academic Evaluation Credential Helper Expander
        with st.expander("🎓 Project Evaluation Roster & Credentials", expanded=False):
            st.markdown("""
            <div style="font-size: 0.8rem; color: #A69BBE; line-height: 1.5;">
                <p>This application is restricted to the 5 official Bennett University team members from the project report. Initial evaluation credentials for university testing:</p>
                <table style="width:100%; border-collapse:collapse; margin-top:8px; font-size:0.78rem;">
                    <tr style="border-bottom:1px solid #2E2248; color:#B66DFF;">
                        <th style="text-align:left; padding:4px 0;">Member</th>
                        <th style="text-align:left; padding:4px 0;">Enrollment</th>
                        <th style="text-align:left; padding:4px 0;">Role</th>
                        <th style="text-align:left; padding:4px 0;">Default PIN</th>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(46,34,72,0.5);">
                        <td style="padding:4px 0; color:#FFFFFF;">Ridhima</td>
                        <td><code>S26CSEU1925</code></td>
                        <td><span class="badge-safe">Member</span></td>
                        <td><code>Ridhima@1925</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(46,34,72,0.5);">
                        <td style="padding:4px 0; color:#FFFFFF;">Anoushka</td>
                        <td><code>S26CSEU1922</code></td>
                        <td><span class="badge-safe">Member</span></td>
                        <td><code>Anoushka@1922</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(46,34,72,0.5);">
                        <td style="padding:4px 0; color:#FFFFFF;">AATIRTH</td>
                        <td><code>S26CSEU1913</code></td>
                        <td><span class="badge-safe">Member</span></td>
                        <td><code>Aatirth@1913</code></td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(46,34,72,0.5);">
                        <td style="padding:4px 0; color:#FFFFFF;">HARSH</td>
                        <td><code>S26CSEU1935</code></td>
                        <td><span class="badge-warning">Team Admin</span></td>
                        <td><code>Harsh@1935</code></td>
                    </tr>
                    <tr>
                        <td style="padding:4px 0; color:#FFFFFF;">SRISHTHI</td>
                        <td><code>S26CSEU1939</code></td>
                        <td><span class="badge-safe">Member</span></td>
                        <td><code>Srishthi@1939</code></td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
