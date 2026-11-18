"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/brand_logo.py
Description: Premium Custom Brand Logo Component.
             Features an elegant purple/violet gradient logo depicting a modern
             wallet combined with an upward financial growth arrow, bold typography,
             and the official tagline: "Smart Money. Better Future."
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import re
from datetime import datetime


def _clean_markup(markup: str) -> str:
    """
    Strips leading whitespace from every line so Streamlit's Markdown parser
    does not mistake 4-space indentation for code blocks.
    """
    return re.sub(r"^\s+", "", markup, flags=re.MULTILINE).strip()


def get_spendwise_icon_svg(size: int = 42, unique_id: str = "main") -> str:
    """
    Returns an optimized inline SVG string for the SpendWise brand icon.
    The icon depicts a sleek modern wallet integrated with a dynamic upward
    financial growth arrow in a glowing violet/purple gradient.
    """
    svg = f"""<svg width="{size}" height="{size}" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:inline-block; vertical-align:middle; flex-shrink:0; filter:drop-shadow(0 4px 10px rgba(139, 92, 246, 0.35));">
<defs>
<linearGradient id="purpleBg_{unique_id}" x1="0" y1="0" x2="44" y2="44" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#8B5CF6"/>
<stop offset="50%" stop-color="#7C3AED"/>
<stop offset="100%" stop-color="#4C1D95"/>
</linearGradient>
<linearGradient id="growthArrow_{unique_id}" x1="10" y1="32" x2="35" y2="11" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#C084FC"/>
<stop offset="50%" stop-color="#E879F9"/>
<stop offset="100%" stop-color="#38BDF8"/>
</linearGradient>
<linearGradient id="cardGrad_{unique_id}" x1="13" y1="11" x2="27" y2="17" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#EDE9FE"/>
<stop offset="100%" stop-color="#A78BFA"/>
</linearGradient>
<filter id="violetGlow_{unique_id}" x="-20%" y="-20%" width="140%" height="140%">
<feGaussianBlur stdDeviation="1.6" result="blur"/>
<feMerge>
<feMergeNode in="blur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>
<rect x="1.5" y="1.5" width="41" height="41" rx="11" fill="url(#purpleBg_{unique_id})" stroke="rgba(255, 255, 255, 0.25)" stroke-width="1.2"/>
<rect x="14" y="10.5" width="13" height="6.5" rx="2" fill="url(#cardGrad_{unique_id})" opacity="0.95"/>
<rect x="8" y="15" width="28" height="20" rx="4" fill="#0B132B" stroke="rgba(196, 181, 253, 0.4)" stroke-width="1.2"/>
<path d="M25 21H36V29H25C23.6 29 22.5 27.9 22.5 26.5V23.5C22.5 22.1 23.6 21 25 21Z" fill="#1C2541" stroke="#A855F7" stroke-width="1"/>
<circle cx="30.5" cy="25" r="1.6" fill="#A855F7"/>
<circle cx="30.5" cy="25" r="0.75" fill="#FFFFFF"/>
<path d="M11 31L18 24L23.5 27.5L34 12" stroke="url(#growthArrow_{unique_id})" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" filter="url(#violetGlow_{unique_id})"/>
<path d="M27 12H34V19" stroke="url(#growthArrow_{unique_id})" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" filter="url(#violetGlow_{unique_id})"/>
<circle cx="34" cy="12" r="1.8" fill="#FFFFFF"/>
</svg>"""
    return _clean_markup(svg)


def render_main_header_logo(show_meta: bool = True, user_info: dict = None) -> str:
    """
    Generates clean HTML for the prominent brand logo displayed at the top-left of the
    main dashboard header across every application page.
    """
    svg_icon = get_spendwise_icon_svg(size=42, unique_id="main_hdr")
    now_str = datetime.now().strftime("%B %Y")

    meta_html = ""
    if show_meta:
        user_badge_html = ""
        if user_info:
            user_name = user_info.get("full_name", "Member")
            user_role = "Admin" if user_info.get("role") == "admin" else "Member"
            role_color = "#B66DFF" if user_role == "Admin" else "#35D49A"
            user_badge_html = f"""<div style="background:rgba(33, 22, 56, 0.85); border:1px solid #2E2248; padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; color:#FFFFFF; display:flex; align-items:center; gap:6px; box-sizing:border-box;">
<span>👤 {user_name}</span>
<span style="color:{role_color}; font-size:0.68rem; font-weight:700;">({user_role})</span>
</div>"""

        meta_html = f"""<div style="display:flex; align-items:center; gap:8px; margin-left:auto; flex-wrap:wrap;">
{user_badge_html}
<div style="display:flex; align-items:center; gap:6px; background:rgba(145, 71, 255, 0.15); border:1px solid rgba(182, 109, 255, 0.35); padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:700; color:#B66DFF; box-sizing:border-box;">
<span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981; flex-shrink:0;"></span>
<span>FINANCIAL INTELLIGENCE</span>
</div>
<div style="background:rgba(33, 22, 56, 0.8); border:1px solid #2E2248; padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; color:#A69BBE; box-sizing:border-box;">
📅 {now_str}
</div>
</div>"""

    html = f"""<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; padding:0.75rem 1.15rem; margin-bottom:1.5rem; background:linear-gradient(145deg, rgba(33, 22, 56, 0.75) 0%, rgba(23, 17, 40, 0.85) 100%); border:1px solid #2E2248; border-radius:14px; box-shadow:0 4px 20px rgba(0, 0, 0, 0.35); backdrop-filter:blur(8px); width:100%; max-width:100%; box-sizing:border-box; min-width:0;">
<div style="display:flex; align-items:center; gap:12px; min-width:0;">
{svg_icon}
<div style="min-width:0;">
<div style="display:flex; align-items:baseline; gap:8px;">
<span style="font-size:1.45rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em; line-height:1.1;">
Spend<span style="background:linear-gradient(135deg, #9147FF 0%, #B66DFF 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Wise</span>
</span>
<span style="font-size:0.7rem; padding:2px 7px; border-radius:6px; background:rgba(145, 71, 255, 0.18); border:1px solid rgba(182, 109, 255, 0.4); color:#B66DFF; font-weight:700; letter-spacing:0.05em;">
PRO
</span>
</div>
<div style="font-size:0.75rem; color:#A69BBE; font-weight:500; letter-spacing:0.02em; margin-top:2px;">
Smart Money. Better Future.
</div>
</div>
</div>
{meta_html}
</div>"""
    return _clean_markup(html)


def render_sidebar_logo() -> str:
    """
    Generates clean HTML for the compact brand logo displayed at the top of the sidebar.
    """
    svg_icon = get_spendwise_icon_svg(size=36, unique_id="sidebar_logo")
    html = f"""<div style="padding:0.25rem 0 0.85rem 0; border-bottom:1px solid #2E2248; margin-bottom:1.15rem; width:100%; max-width:100%; box-sizing:border-box;">
<div style="display:flex; align-items:center; gap:10px; width:100%; min-width:0; box-sizing:border-box;">
{svg_icon}
<div style="min-width:0; flex:1;">
<div style="font-size:1.3rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em; line-height:1.1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
Spend<span style="background:linear-gradient(135deg, #9147FF 0%, #B66DFF 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Wise</span>
</div>
<div style="font-size:0.7rem; color:#A69BBE; font-weight:600; letter-spacing:0.02em; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
Smart Money. Better Future.
</div>
</div>
</div>
</div>"""
    return _clean_markup(html)


def render_sidebar_bottom(
    total_txns: int,
    balance_str: str,
    balance_val: float,
    total_exp_str: str,
    now_str: str,
    user_info: dict = None
) -> str:
    """
    Renders the luxury bottom section of the sidebar:
    - User Profile Card (Dynamic authenticated team member)
    - Active Liquidity Status
    - Enterprise Version & Academic Footer
    """
    balance_color = "#35D49A" if balance_val >= 0 else "#FF5478"

    # Default to Harsh if not logged in (fallback)
    if not user_info:
        user_name = "Harsh Raj"
        enrollment_no = "S26CSEU1935"
        role_label = "Lead"
        initials = "HR"
    else:
        user_name = user_info.get("full_name", "Team Member")
        enrollment_no = user_info.get("enrollment_no", "S26CSEU1935")
        role = user_info.get("role", "member")
        role_label = "Admin" if role == "admin" else "Member"

        # Compute initials
        name_parts = user_name.strip().split()
        if len(name_parts) >= 2:
            initials = (name_parts[0][0] + name_parts[1][0]).upper()
        elif len(name_parts) == 1 and len(name_parts[0]) >= 2:
            initials = name_parts[0][:2].upper()
        else:
            initials = "SW"

    role_badge = f'<span style="background:rgba(145, 71, 255, 0.2); color:#B66DFF; border:1px solid rgba(182, 109, 255, 0.4); padding:1px 5px; border-radius:4px; font-size:0.62rem; font-weight:700;">{role_label}</span>'

    html = f"""<div style="margin-top: 1.25rem; display:flex; flex-direction:column; gap:10px; width:100%; max-width:100%; box-sizing:border-box;">
<!-- Active Liquidity Snapshot Card -->
<div style="background: linear-gradient(145deg, #211638 0%, #171128 100%); border: 1px solid #2E2248; border-radius: 12px; padding: 0.85rem; font-size: 0.85rem; box-shadow: 0 4px 14px rgba(0,0,0,0.35); width:100%; max-width:100%; box-sizing:border-box;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 4px; gap:4px;">
<span style="color: #A69BBE; font-weight: 700; font-size: 0.68rem; letter-spacing:0.06em; text-transform:uppercase;">Active Liquidity</span>
<span style="color: #B66DFF; font-size: 0.7rem; font-weight:600;">{now_str}</span>
</div>
<div style="font-size: 1.25rem; font-weight: 800; color: {balance_color}; font-family: monospace; letter-spacing:-0.02em; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
{balance_str}
</div>
<div style="display:flex; justify-content:space-between; color: #A69BBE; margin-top: 6px; font-size: 0.74rem; border-top: 1px solid rgba(182, 109, 255, 0.15); padding-top: 6px; gap:4px;">
<span>Txns: <strong style="color:#FFFFFF;">{total_txns}</strong></span>
<span>Exp: <strong style="color:#FF5478;">{total_exp_str}</strong></span>
</div>
</div>

<!-- User Profile Card -->
<div style="background: linear-gradient(145deg, rgba(33, 22, 56, 0.85) 0%, rgba(23, 17, 40, 0.95) 100%); border: 1px solid #2E2248; border-radius: 12px; padding: 0.7rem 0.8rem; display:flex; align-items:center; gap:9px; box-shadow: 0 4px 12px rgba(0,0,0,0.25); width:100%; max-width:100%; box-sizing:border-box;">
<div style="width:34px; height:34px; border-radius:50%; background: linear-gradient(135deg, #9147FF 0%, #B66DFF 100%); display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:800; color:#FFFFFF; box-shadow:0 0 10px rgba(145, 71, 255, 0.4); flex-shrink:0;">
{initials}
</div>
<div style="min-width:0; flex:1; overflow:hidden;">
<div style="display:flex; align-items:center; gap:5px;">
<span style="font-size:0.82rem; font-weight:700; color:#FFFFFF; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{user_name}</span>
<span style="width:6px; height:6px; border-radius:50%; background:#35D49A; box-shadow:0 0 6px #35D49A; display:inline-block; flex-shrink:0;"></span>
{role_badge}
</div>
<div style="font-size:0.68rem; color:#A69BBE; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
{enrollment_no} • Bennett Univ
</div>
</div>
</div>

<!-- Academic & Enterprise Version Tag -->
<div style="font-size: 0.68rem; color: #7B7192; border-top: 1px solid #2E2248; padding-top: 0.65rem; line-height: 1.35; display:flex; flex-direction:column; gap:2px; width:100%; box-sizing:border-box;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="font-weight:600; color:#A69BBE;">SpendWise Enterprise</span>
<span style="background:rgba(145, 71, 255, 0.15); border:1px solid rgba(182, 109, 255, 0.3); color:#B66DFF; padding:1px 5px; border-radius:5px; font-size:0.62rem; font-weight:700;">v3.0 Multi-User</span>
</div>
<div style="color:#6A6180;">Bennett Univ • 2026CSAE100</div>
</div>
</div>"""
    return _clean_markup(html)
