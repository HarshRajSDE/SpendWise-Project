"""
================================================================================
SpendWise - Personal Expense and Budget Tracker
File: modules/styles.py
Description: Premium Modern Fintech SaaS Design System.
             Theme: Dark Luxury Navy-Purple (#100B20, #171128, #211638) with
             Vibrant Electric Purple (#9147FF) & Luminous Violet (#B66DFF)
             accents, subtle gradients, Lucide icon navigation, and polished cards.
             Fully responsive, zero horizontal overflow, fluid sidebar & dashboard layout.
Course: Computational Thinking and Programming (2026CSAE100)
Academic Year: 2026-27
================================================================================
"""

import streamlit as st


def apply_custom_styles():
    """
    Injects custom CSS styling for a modern, high-contrast, fintech-inspired dashboard
    with an advanced luxury SaaS sidebar navigation system and responsive layout.
    """
    custom_css = """
    <style>
        /* Google Fonts Import for Premium Typography */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Universal Box-Sizing & Global Reset */
        *, *::before, *::after {
            box-sizing: border-box !important;
        }

        /* Prevent Horizontal Overflow Globally */
        html, body, .stApp, .main, div[data-testid="stAppViewContainer"] {
            overflow-x: hidden !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
        }

        /* Global Application Background */
        .stApp {
            background: radial-gradient(circle at top left, #1E1238 0%, #100B20 40%, #0A0614 100%) !important;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        /* ============================================================
           1. HIDE DEPLOY BUTTON, MAIN MENU & TOP DECORATION STRIP
           ============================================================ */
        div[data-testid="stDecoration"] {
            display: none !important;
            height: 0px !important;
            visibility: hidden !important;
        }

        .stDeployButton,
        .stAppDeployButton,
        [data-testid="stAppDeployButton"],
        button[data-testid="stAppDeployButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        #MainMenu,
        [data-testid="stMainMenu"],
        button#MainMenu {
            display: none !important;
            visibility: hidden !important;
        }

        div[data-testid="stStatusWidget"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* ============================================================
           2. STYLE THE TOP HEADER BAR - DARK LUXURY NAVY-PURPLE
           ============================================================ */
        header[data-testid="stHeader"] {
            background-color: #100B20 !important;
            background: #100B20 !important;
            border-bottom: 1px solid #2E2248 !important;
            height: 3.5rem !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
            z-index: 999990 !important;
            box-sizing: border-box !important;
        }

        /* Sidebar collapse & expand controls */
        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stExpandSidebarButton"],
        button[data-testid="collapsedControl"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        header[data-testid="stHeader"] button {
            visibility: visible !important;
            display: inline-flex !important;
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            transition: all 0.2s ease !important;
        }
        button[data-testid="stSidebarCollapseButton"] svg,
        button[data-testid="stExpandSidebarButton"] svg,
        [data-testid="collapsedControl"] svg,
        header[data-testid="stHeader"] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        button[data-testid="stSidebarCollapseButton"]:hover,
        button[data-testid="stExpandSidebarButton"]:hover,
        [data-testid="collapsedControl"]:hover {
            background: rgba(145, 71, 255, 0.18) !important;
            border-radius: 8px !important;
            color: #B66DFF !important;
        }

        /* ============================================================
           3. MAIN DASHBOARD CONTAINER & RESPONSIVE MAX-WIDTH
           ============================================================ */
        .main div.block-container,
        div[data-testid="stMainBlockContainer"] {
            padding-top: 4.75rem !important;
            padding-bottom: 3.5rem !important;
            padding-left: clamp(1rem, 2.5vw, 2rem) !important;
            padding-right: clamp(1rem, 2.5vw, 2rem) !important;
            max-width: 1240px !important;
            width: 100% !important;
            margin: 0 auto !important;
            box-sizing: border-box !important;
            min-width: 0 !important;
        }

        /* ============================================================
           4. SIDEBAR CONTAINER (270px - 290px CONSISTENT WIDTH)
           ============================================================ */
        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 270px !important;
            max-width: 290px !important;
            box-sizing: border-box !important;
            background-color: #171128 !important;
            background: #171128 !important;
            border-right: 1px solid #2E2248 !important;
            transition: all 0.3s ease-in-out !important;
        }

        section[data-testid="stSidebar"][aria-expanded="false"] {
            margin-left: -290px !important;
        }

        section[data-testid="stSidebar"] div.block-container,
        div[data-testid="stSidebarUserContent"],
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0.85rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.95rem !important;
            padding-right: 0.95rem !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow-x: hidden !important;
        }

        /* ============================================================
           5. ADVANCED FINTECH SAAS NAVIGATION SYSTEM
           ============================================================ */
        section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] {
            gap: 4px !important;
            display: flex !important;
            flex-direction: column !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* Hide the native round radio button completely */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label > div:first-child {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Base Navigation Item Pill (Flexbox with min-width: 0) */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label {
            display: flex !important;
            align-items: center !important;
            padding: 0.55rem 0.75rem !important;
            margin: 0 0 3px 0 !important;
            border-radius: 10px !important;
            border: 1px solid transparent !important;
            background: transparent !important;
            color: #A69BBE !important;
            cursor: pointer !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative !important;
            font-weight: 500 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            min-width: 0 !important;
            user-select: none !important;
        }

        /* Text container inside label (min-width: 0 prevents flex overflow) */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label > div:last-child,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label > div {
            min-width: 0 !important;
            flex: 1 1 auto !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }

        /* Label Typography: Allow wrapping onto 2 lines, no clip */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label span,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label div {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.85rem !important;
            line-height: 1.25 !important;
            font-weight: 500 !important;
            color: #A69BBE !important;
            transition: color 0.2s ease !important;
            margin: 0 !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }

        /* Hover State with Micro-interaction */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:hover {
            background: rgba(145, 71, 255, 0.12) !important;
            border-color: rgba(182, 109, 255, 0.25) !important;
            transform: translateX(3px) !important;
        }
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:hover p,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:hover span {
            color: #FFFFFF !important;
        }

        /* Active Navigation Item (Selected Page) */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, rgba(145, 71, 255, 0.32) 0%, rgba(182, 109, 255, 0.14) 100%) !important;
            border: 1px solid rgba(182, 109, 255, 0.5) !important;
            box-shadow: 0 4px 16px rgba(145, 71, 255, 0.25), inset 0 0 10px rgba(182, 109, 255, 0.08) !important;
            color: #FFFFFF !important;
        }
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked) p,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked) span,
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked) div {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Left Glowing Active Indicator Bar */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked)::after {
            content: '' !important;
            position: absolute !important;
            left: 0 !important;
            top: 12% !important;
            bottom: 12% !important;
            width: 3.5px !important;
            background: linear-gradient(180deg, #B66DFF 0%, #9147FF 100%) !important;
            border-radius: 0 4px 4px 0 !important;
            box-shadow: 0 0 8px #B66DFF !important;
        }

        /* Fixed-Size Vector Icon Pseudo-Element (Never Shrinks) */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label::before {
            content: '' !important;
            display: inline-block !important;
            width: 18px !important;
            min-width: 18px !important;
            max-width: 18px !important;
            height: 18px !important;
            min-height: 18px !important;
            max-height: 18px !important;
            margin-right: 10px !important;
            background-color: #A69BBE !important;
            -webkit-mask-size: contain !important;
            mask-size: contain !important;
            -webkit-mask-repeat: no-repeat !important;
            mask-repeat: no-repeat !important;
            -webkit-mask-position: center !important;
            mask-position: center !important;
            transition: all 0.22s ease !important;
            flex-shrink: 0 !important;
            box-sizing: border-box !important;
        }

        /* Icon Hover State */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:hover::before {
            background-color: #B66DFF !important;
            filter: drop-shadow(0 0 5px rgba(182, 109, 255, 0.7)) !important;
        }

        /* Icon Active State */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:has(input:checked)::before {
            background-color: #FFFFFF !important;
            filter: drop-shadow(0 0 8px rgba(182, 109, 255, 0.9)) !important;
        }

        /* ------------------------------------------------------------
           Lucide Vector Icons Assigned to the 9 Navigation Items
           ------------------------------------------------------------ */
        /* 1. Overview Dashboard */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(1)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='7' height='9' x='3' y='3' rx='1'/%3E%3Crect width='7' height='5' x='14' y='3' rx='1'/%3E%3Crect width='7' height='9' x='14' y='12' rx='1'/%3E%3Crect width='7' height='5' x='3' y='16' rx='1'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='7' height='9' x='3' y='3' rx='1'/%3E%3Crect width='7' height='5' x='14' y='3' rx='1'/%3E%3Crect width='7' height='9' x='14' y='12' rx='1'/%3E%3Crect width='7' height='5' x='3' y='16' rx='1'/%3E%3C/svg%3E") !important;
        }

        /* 2. Add Transaction */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(2)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M8 12h8'/%3E%3Cpath d='M12 8v8'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M8 12h8'/%3E%3Cpath d='M12 8v8'/%3E%3C/svg%3E") !important;
        }

        /* 3. All Transactions */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(3)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z'/%3E%3Cpath d='M14 8H8'/%3E%3Cpath d='M16 12H8'/%3E%3Cpath d='M13 16H8'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z'/%3E%3Cpath d='M14 8H8'/%3E%3Cpath d='M16 12H8'/%3E%3Cpath d='M13 16H8'/%3E%3C/svg%3E") !important;
        }

        /* 4. Budget Management */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(4)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1'/%3E%3Cpath d='M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1'/%3E%3Cpath d='M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4'/%3E%3C/svg%3E") !important;
        }

        /* 5. Smart Budget Intelligence */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(5)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'/%3E%3Cpath d='M5 3v4'/%3E%3Cpath d='M19 17v4'/%3E%3Cpath d='M3 5h4'/%3E%3Cpath d='M17 19h4'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z'/%3E%3Cpath d='M5 3v4'/%3E%3Cpath d='M19 17v4'/%3E%3Cpath d='M3 5h4'/%3E%3Cpath d='M17 19h4'/%3E%3C/svg%3E") !important;
        }

        /* 6. Spending Analytics */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(6)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E") !important;
        }

        /* 7. Reports & Data */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(7)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/%3E%3Cpath d='M14 2v4a2 2 0 0 0 2 2h4'/%3E%3Cpath d='M8 18v-2'/%3E%3Cpath d='M12 18v-4'/%3E%3Cpath d='M16 18v-6'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z'/%3E%3Cpath d='M14 2v4a2 2 0 0 0 2 2h4'/%3E%3Cpath d='M8 18v-2'/%3E%3Cpath d='M12 18v-4'/%3E%3Cpath d='M16 18v-6'/%3E%3C/svg%3E") !important;
        }

        /* 8. About Project */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(8)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21.42 10.922a1 1 0 0 0-.019-.838L12.83 2.18a2 2 0 0 0-1.66 0L2.6 10.084a1 1 0 0 0 0 1.832l8.57 7.908a2 2 0 0 0 1.66 0l6.71-6.192V17a1 1 0 0 0 2 0v-4.578a1 1 0 0 0-.12-.5z'/%3E%3Cpath d='M6 12v5c0 2 3 3 6 3s6-1 6-3v-5'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21.42 10.922a1 1 0 0 0-.019-.838L12.83 2.18a2 2 0 0 0-1.66 0L2.6 10.084a1 1 0 0 0 0 1.832l8.57 7.908a2 2 0 0 0 1.66 0l6.71-6.192V17a1 1 0 0 0 2 0v-4.578a1 1 0 0 0-.12-.5z'/%3E%3Cpath d='M6 12v5c0 2 3 3 6 3s6-1 6-3v-5'/%3E%3C/svg%3E") !important;
        }

        /* 9. Settings */
        section[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] label:nth-child(9)::before {
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E") !important;
            mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E") !important;
        }

        /* Hero & Section Header Titles */
        .hero-title {
            margin-top: 0 !important;
            padding-top: 0 !important;
            font-size: clamp(1.6rem, 2.8vw, 2.1rem);
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #B66DFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
            line-height: 1.2;
            word-break: break-word;
        }
        .hero-subtitle {
            color: #A69BBE;
            font-size: clamp(0.85rem, 1.4vw, 0.95rem);
            margin-bottom: 1.25rem;
            font-weight: 400;
            line-height: 1.4;
            word-break: break-word;
        }

        h1, .stHeading, div[data-testid="stHeadingWithActionElements"] h1,
        div[data-testid="stHeading"] h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            color: #FFFFFF !important;
            word-break: break-word !important;
        }
        h2, h3, h4 {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            word-break: break-word !important;
        }

        /* ============================================================
           6. RESPONSIVE DASHBOARD COLUMNS & CARDS
           ============================================================ */
        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            gap: 0.85rem !important;
        }

        div[data-testid="column"] {
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        .kpi-card {
            background: linear-gradient(145deg, #1D1733 0%, #171128 100%);
            border: 1px solid #2E2248;
            border-radius: 14px;
            padding: 1rem 1.15rem;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), 0 0 1px 1px rgba(145, 71, 255, 0.12);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            margin-bottom: 0.75rem;
            min-height: 115px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, rgba(182, 109, 255, 0.5), transparent);
            opacity: 0;
            transition: opacity 0.25s ease;
        }
        .kpi-card:hover {
            border-color: #B66DFF;
            transform: translateY(-3px);
            box-shadow: 0 12px 30px -4px rgba(145, 71, 255, 0.25), 0 0 2px 1px rgba(182, 109, 255, 0.25);
        }
        .kpi-card:hover::before {
            opacity: 1;
        }
        .kpi-title {
            font-size: 0.74rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #A69BBE;
            margin-bottom: 0.35rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .kpi-value {
            font-size: clamp(1.2rem, 1.8vw, 1.75rem);
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.2;
            font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
            letter-spacing: -0.02em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .kpi-value.green {
            color: #35D49A;
            text-shadow: 0 0 20px rgba(53, 212, 154, 0.3);
        }
        .kpi-value.purple {
            color: #B66DFF;
            text-shadow: 0 0 20px rgba(182, 109, 255, 0.35);
        }
        .kpi-value.red {
            color: #FF5478;
            text-shadow: 0 0 20px rgba(255, 84, 120, 0.3);
        }
        .kpi-value.cyan {
            color: #38BDF8;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
        }
        .kpi-value.yellow {
            color: #FFB547;
            text-shadow: 0 0 20px rgba(255, 181, 71, 0.3);
        }
        .kpi-subtext {
            font-size: 0.76rem;
            color: #7B7192;
            margin-top: 0.35rem;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Native Streamlit Metrics Styling */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #1D1733 0%, #171128 100%) !important;
            border: 1px solid #2E2248 !important;
            border-radius: 14px !important;
            padding: 1rem 1.15rem !important;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.45), 0 0 1px 1px rgba(145, 71, 255, 0.12) !important;
            min-height: 110px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            transition: all 0.25s ease !important;
            width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #B66DFF !important;
            transform: translateY(-2px) !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #A69BBE !important;
            font-size: 0.74rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: clamp(1.2rem, 1.8vw, 1.65rem) !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* Content & Dashboard Container Cards */
        .content-card,
        .dashboard-card {
            background: linear-gradient(145deg, #1D1733 0%, #151026 100%);
            border: 1px solid #2E2248;
            border-radius: 14px;
            padding: 1.35rem;
            box-shadow: 0 8px 26px -4px rgba(0, 0, 0, 0.45), 0 0 1px 1px rgba(145, 71, 255, 0.12);
            margin-bottom: 1.25rem;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
            transition: all 0.25s ease;
        }
        .content-card:hover,
        .dashboard-card:hover {
            border-color: rgba(182, 109, 255, 0.35);
            box-shadow: 0 10px 30px -4px rgba(145, 71, 255, 0.18), 0 0 2px 1px rgba(182, 109, 255, 0.2);
        }

        /* Section Card Header */
        .card-header-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.65rem;
            border-bottom: 1px solid rgba(46, 34, 72, 0.7);
        }
        .card-header-title h3 {
            margin: 0 !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card-header-badge {
            font-size: 0.72rem;
            font-weight: 600;
            color: #B66DFF;
            background: rgba(145, 71, 255, 0.12);
            border: 1px solid rgba(182, 109, 255, 0.3);
            padding: 2px 8px;
            border-radius: 6px;
        }

        /* Badges */
        .badge-safe {
            background: rgba(16, 185, 129, 0.14);
            color: #10B981;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
            display: inline-block;
            white-space: nowrap;
        }
        .badge-warning {
            background: rgba(245, 158, 11, 0.14);
            color: #F59E0B;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(245, 158, 11, 0.3);
            display: inline-block;
            white-space: nowrap;
        }
        .badge-danger {
            background: rgba(239, 68, 68, 0.14);
            color: #EF4444;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(239, 68, 68, 0.3);
            display: inline-block;
            white-space: nowrap;
        }
        .badge-info {
            background: rgba(182, 109, 255, 0.14);
            color: #B66DFF;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid rgba(182, 109, 255, 0.3);
            display: inline-block;
            white-space: nowrap;
        }

        /* Modern Tabs */
        div[data-baseweb="tab-list"] {
            background-color: #171128 !important;
            padding: 5px !important;
            border-radius: 12px !important;
            border: 1px solid #2E2248 !important;
            gap: 6px !important;
            margin-bottom: 1.25rem !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow-x: auto !important;
        }
        button[data-baseweb="tab"] {
            border-radius: 8px !important;
            color: #A69BBE !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 8px 16px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
            white-space: nowrap !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #FFFFFF !important;
            background: rgba(145, 71, 255, 0.1) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #2A1B46 0%, #1E1236 100%) !important;
            color: #B66DFF !important;
            border: 1px solid rgba(182, 109, 255, 0.4) !important;
            box-shadow: 0 2px 10px rgba(145, 71, 255, 0.25) !important;
        }
        div[data-baseweb="tab-highlight"],
        div[data-baseweb="tab-border"] {
            display: none !important;
        }

        /* Modern Streamlit Expanders */
        div[data-testid="stExpander"] {
            background: #1B132E !important;
            border: 1px solid #2E2248 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        div[data-testid="stExpander"] summary {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            padding: 0.85rem 1.15rem !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: #B66DFF !important;
        }

        /* Polished Buttons */
        div.stButton > button,
        div.stFormSubmitButton > button,
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #9147FF 0%, #7C3AED 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            padding: 0.55rem 1.4rem !important;
            font-size: 0.95rem !important;
            box-shadow: 0 4px 16px rgba(145, 71, 255, 0.35) !important;
            transition: all 0.2s ease !important;
            box-sizing: border-box !important;
        }
        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover,
        div.stDownloadButton > button:hover {
            background: linear-gradient(135deg, #A855F7 0%, #8B5CF6 100%) !important;
            color: #FFFFFF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 22px rgba(145, 71, 255, 0.5) !important;
        }

        /* Secondary & Danger Buttons */
        div.stButton > button[kind="secondary"],
        div.stFormSubmitButton > button[kind="secondary"] {
            background: #211638 !important;
            color: #FFFFFF !important;
            border: 1px solid #2E2248 !important;
        }

        /* Form Inputs & Selectboxes */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            background-color: #171128 !important;
            border: 1px solid #2E2248 !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            box-sizing: border-box !important;
        }
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #B66DFF !important;
            box-shadow: 0 0 0 2px rgba(182, 109, 255, 0.25) !important;
        }
        div[data-baseweb="input"] input {
            color: #FFFFFF !important;
        }

        /* Streamlit Progress Bar */
        div.stProgress > div > div > div > div {
            background: linear-gradient(90deg, #9147FF 0%, #B66DFF 50%, #38BDF8 100%) !important;
            border-radius: 6px;
        }

        /* Plotly Charts Responsiveness (No horizontal overflow) */
        div[data-testid="stPlotlyChart"],
        .js-plotly-plot,
        .plot-container,
        .svg-container {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .js-plotly-plot .plotly svg {
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* Empty State Card */
        .empty-state-box {
            text-align: center;
            padding: 3rem 1.5rem;
            background: linear-gradient(145deg, #211638 0%, #171128 100%);
            border: 2px dashed #2E2248;
            border-radius: 16px;
            margin: 2rem 0;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .empty-state-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 0.5rem;
            word-break: break-word;
        }
        .empty-state-desc {
            font-size: 0.95rem;
            color: #A69BBE;
            max-width: 520px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.5;
            word-break: break-word;
        }

        /* Insight Box */
        .insight-box {
            background: rgba(145, 71, 255, 0.08);
            border-left: 4px solid #B66DFF;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            font-size: 0.92rem;
            color: #FFFFFF;
            width: 100% !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
        }

        /* Table & DataFrame Customizations */
        div[data-testid="stDataFrame"] {
            border: 1px solid #2E2248;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        /* ============================================================
           7. RESPONSIVE BREAKPOINTS (LAPTOPS, TABLETS & MOBILE)
           ============================================================ */
        /* Medium / Small Laptop Screens (<= 1100px) */
        @media (max-width: 1100px) {
            section[data-testid="stSidebar"] {
                width: 270px !important;
                min-width: 270px !important;
                max-width: 270px !important;
            }
            .main div.block-container,
            div[data-testid="stMainBlockContainer"] {
                padding-left: 1.25rem !important;
                padding-right: 1.25rem !important;
            }
            /* 4-column KPI cards wrap into 2x2 grid */
            div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
            }
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                flex: 1 1 calc(50% - 0.85rem) !important;
                min-width: 200px !important;
            }
        }

        /* Tablet / Mobile Screens (<= 768px) */
        @media (max-width: 768px) {
            .main div.block-container,
            div[data-testid="stMainBlockContainer"] {
                padding-top: 4.25rem !important;
                padding-left: 0.85rem !important;
                padding-right: 0.85rem !important;
            }
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
            .hero-title {
                font-size: 1.6rem !important;
            }
            .kpi-value {
                font-size: 1.45rem !important;
            }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
