def inject_theme():
    import streamlit as st
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ════════════════════════════════════════
       MAIN BACKGROUND — LIGHT GREY
    ════════════════════════════════════════ */
    
    .stApp {
        background-color: #F5F5F0 !important;
    }

    /* ════════════════════════════════════════
       SIDEBAR — GLASSY DARK (matches login card)
    ════════════════════════════════════════ */

    section[data-testid="stSidebar"] {
        background: rgba(8, 18, 12, 0.92) !important;
        border-right: 1px solid rgba(61, 255, 154, 0.18) !important;
        box-shadow: 4px 0 32px rgba(0,0,0,0.55) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border-top: 2px solid var(--orange-bright);
        border-left: 1px solid var(--border-green);
        border-right: 1px solid rgba(255,255,255,0.08);
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    /* Transparent inner wrappers */
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div,
    section[data-testid="stSidebar"] section,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] .element-container,
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Orange top accent bar on sidebar (mirrors login card) */
    section[data-testid="stSidebar"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 3px !important;
        background: linear-gradient(90deg, #FF8C42, #E06820) !important;
        z-index: 10 !important;
        pointer-events: none !important;
    }

    /* ── Brand block (ENLARGED) ── */
    .brand-block {
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
        padding: 24px 16px 20px !important;
        border-bottom: 1px solid rgba(61, 255, 154, 0.18) !important;
        margin-bottom: 10px !important;
    }

    .brand-logo {
        width: 60px !important;
        height: 60px !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        flex-shrink: 0 !important;
        border: 2px solid rgba(61, 255, 154, 0.35) !important;
        background: rgba(8, 25, 15, 0.8) !important;
    }

    .brand-logo img {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
    }

    .brand-tile {
        width: 60px !important;
        height: 60px !important;
        border-radius: 14px !important;
        background: rgba(61, 255, 154, 0.12) !important;
        border: 2px solid rgba(61, 255, 154, 0.35) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }

    .brand-tile i {
        font-size: 28px !important;
        color: #3DFF9A !important;
    }

    .brand-name {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #3DFF9A !important;
        line-height: 1.35 !important;
        text-shadow: 0 0 22px rgba(61, 255, 154, 0.45) !important;
        letter-spacing: -0.2px !important;
    }

    .brand-sub {
        font-size: 11px !important;
        color: rgba(255, 140, 66, 0.85) !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        margin-top: 4px !important;
    }

    /* ── All sidebar text ── */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: rgba(200, 255, 230, 0.80) !important;
    }

    /* ── Nav menu option_menu styles ── */
    section[data-testid="stSidebar"] ul,
    section[data-testid="stSidebar"] nav {
        background: transparent !important;
    }

    /* option_menu nav links */
    section[data-testid="stSidebar"] .nav-link {
        color: rgba(200, 255, 230, 0.65) !important;
        border-radius: 10px !important;
        padding: 9px 12px !important;
        margin: 2px 4px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        background: transparent !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] .nav-link:hover {
        background: rgba(61, 255, 154, 0.07) !important;
        color: rgba(200, 255, 230, 0.95) !important;
    }

    section[data-testid="stSidebar"] .nav-link-selected {
        background: rgba(255, 140, 66, 0.14) !important;
        color: #FF8C42 !important;
        font-weight: 600 !important;
        border-left: 3px solid #FF8C42 !important;
        border-radius: 0 10px 10px 0 !important;
        box-shadow: inset 0 1px 0 rgba(255, 140, 66, 0.15) !important;
    }

    section[data-testid="stSidebar"] .nav-link-selected .icon {
        color: #FF8C42 !important;
    }

    section[data-testid="stSidebar"] .nav-link .icon {
        color: rgba(200, 255, 230, 0.55) !important;
    }

    /* menu-title label */
    section[data-testid="stSidebar"] .menu-title {
        color: rgba(61, 255, 154, 0.45) !important;
        font-size: 10px !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        padding: 14px 14px 6px !important;
    }

    /* ── Divider ── */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid rgba(61, 255, 154, 0.12) !important;
        margin: 10px 14px !important;
    }

    /* ── Profile card at bottom ── */
    .sidebar-profile {
        background: rgba(8, 25, 15, 0.55) !important;
        border: 1px solid rgba(61, 255, 154, 0.18) !important;
        border-radius: 12px !important;
        margin: 6px 10px !important;
        padding: 10px 12px !important;
    }

    /* Username in profile */
    .sidebar-username {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: rgba(200, 255, 230, 0.95) !important;
    }

    /* ── Role badge — VISIBLE ── */
    .role-badge {
        display: inline-flex !important;
        align-items: center !important;
        margin-top: 3px !important;
        font-size: 9px !important;
        font-weight: 700 !important;
        padding: 2px 9px !important;
        border-radius: 20px !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
    }

    .role-badge.admin {
        background: rgba(61, 255, 154, 0.15) !important;
        border: 1px solid rgba(61, 255, 154, 0.35) !important;
        color: #3DFF9A !important;
    }

    .role-badge.viewer {
        background: rgba(255, 140, 66, 0.15) !important;
        border: 1px solid rgba(255, 140, 66, 0.35) !important;
        color: #FF8C42 !important;
    }

    /* Avatar initials circle */
    .sidebar-avatar {
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        background: rgba(255, 140, 66, 0.2) !important;
        border: 1px solid rgba(255, 140, 66, 0.4) !important;
        color: #FF8C42 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }

    /* ── LOGOUT BUTTON — light green hover shadow ── */
    section[data-testid="stSidebar"] .stButton > button {
        background: var(--green-deep) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.07em !important;
        text-transform: uppercase !important;
        padding: 10px 14px !important;
        width: calc(100% - 20px) !important;
        margin: 4px 10px 12px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(224, 104, 32, 0.4), 0 0 0 1px rgba(255, 140, 66, 0.2) !important;
        transition: box-shadow 0.2s, transform 0.15s !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        box-shadow: 0 8px 32px rgba(29, 184, 106, 0.62), 0 0 0 1px rgba(61, 255, 154, 0.45) !important;
        transform: translateY(-2px) !important;
        color: #ffffff !important;
    }

    /* Sidebar collapse arrow */
    button[data-testid="baseButton-headerNoPadding"] svg {
        color: rgba(61, 255, 154, 0.55) !important;
        fill: rgba(61, 255, 154, 0.55) !important;
    }

    button[data-testid="baseButton-headerNoPadding"]:hover svg {
        color: #3DFF9A !important;
    }

    /* ════════════════════════════════════════
       MAIN CONTENT — WHITE BACKGROUND (unchanged)
    ════════════════════════════════════════ */

    :root {
        --dash-bg:           #FFFFFF;
        --dash-surface:      rgba(248, 249, 250, 0.95);
        --dash-surface-hov:  #FFFFFF;
        --dash-border:       rgba(224, 224, 216, 0.80);
        --dash-text-primary: #1C1A14;
        --dash-text-second:  #3A3526;
        --dash-text-muted:   #9A927E;
        --dash-green:        #1D9E75;
        --dash-green-dark:   #0F6E56;
        --dash-amber:        #E8A020;
    }

    .main .block-container {
        padding: 1.5rem 2rem 2rem !important;
        max-width: 1200px !important;
    }

    h1 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: var(--dash-text-primary) !important;
    }

    h2 {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: var(--dash-text-primary) !important;
    }

    /* ── MAIN CONTENT BUTTONS — orange primary ── */
    .stButton > button {
        background: linear-gradient(135deg, #E06820 0%, #8B3A0A 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        padding: 9px 16px !important;
        cursor: pointer !important;
        box-shadow: 0 3px 16px rgba(224, 104, 32, 0.38), 0 0 0 1px rgba(255, 140, 66, 0.18) !important;
        transition: box-shadow 0.2s, transform 0.15s !important;
    }

    .stButton > button:hover {
        box-shadow: 0 6px 24px rgba(224, 104, 32, 0.55), 0 0 0 1px rgba(255, 140, 66, 0.4) !important;
        transform: translateY(-1px) !important;
        color: #ffffff !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Download buttons — green secondary */
    .stDownloadButton > button {
        background: rgba(29, 158, 117, 0.10) !important;
        color: #0F6E56 !important;
        border: 1px solid rgba(29, 158, 117, 0.35) !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        box-shadow: none !important;
        letter-spacing: 0.04em !important;
        transition: background 0.2s, border-color 0.2s !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(29, 158, 117, 0.18) !important;
        border-color: rgba(29, 158, 117, 0.55) !important;
        transform: translateY(-1px) !important;
        box-shadow: none !important;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: var(--dash-surface) !important;
        border: 0.5px solid var(--dash-border) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        transition: all 0.2s ease !important;
    }

    .metric-card:hover {
        transform: translateY(-2px) !important;
        background: var(--dash-surface-hov) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    .metric-card.active {
        background: rgba(255, 140, 66, 0.07) !important;
        border-color: rgba(224, 104, 32, 0.40) !important;
    }

    .metric-card-label {
        font-size: 10px !important;
        font-weight: 700 !important;
        color: var(--dash-text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.09em !important;
    }

    .metric-card-value {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: var(--dash-text-primary) !important;
    }

    .metric-card-hint {
        font-size: 11px !important;
        color: var(--dash-text-muted) !important;
    }

    /* Icon boxes */
    .mc-icon {
        width: 40px !important;
        height: 40px !important;
        border-radius: 11px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 12px !important;
    }

    .mc-icon i { font-size: 20px !important; }

    .mc-icon.teal  { background: rgba(29,158,117,0.10) !important; color: #0F9E6A !important; }
    .mc-icon.amber { background: rgba(232,160,32,0.10) !important; color: #C07A00 !important; }
    .mc-icon.blue  { background: rgba(55,138,221,0.10) !important; color: #1E78D4 !important; }
    .mc-icon.red   { background: rgba(226,75,74,0.10)  !important; color: #C0392B !important; }

    /* ── DASHBOARD metric card active state (button clicked) ── */
    .metric-card.active .metric-card-value {
        color: #E06820 !important;
    }

    /* Tables */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        background: #FFFFFF !important;
        border: 1px solid var(--dash-border) !important;
        border-radius: 16px !important;
    }

    [data-testid="stDataFrame"] th {
        background: #F8F9FA !important;
        color: var(--dash-text-muted) !important;
    }

    /* Forms */
    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid var(--dash-border) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: #FFFFFF !important;
        border: 1px solid var(--dash-border) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 3px; height: 3px; }
    ::-webkit-scrollbar-track { background: #F1F1F1; }
    ::-webkit-scrollbar-thumb { background: #D9D0C0; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #C8BC9E; }

    </style>
    """, unsafe_allow_html=True)
