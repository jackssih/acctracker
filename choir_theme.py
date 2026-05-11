def inject_theme():
    import streamlit as st
    st.markdown("""
    <style>

    /* ── FONTS ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=DM+Mono:wght@400&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── ROOT PALETTE ── */
    :root {
        --teal-50:  #E1F5EE;
        --teal-100: #9FE1CB;
        --teal-400: #1D9E75;
        --teal-600: #0F6E56;
        --teal-800: #085041;
        --amber-50: #FAEEDA;
        --amber-800: #854F0B;
        --gray-50:  #F1EFE8;
        --gray-200: #B4B2A9;
        --gray-600: #5F5E5A;
    }

    /* ── PAGE BACKGROUND ── */
    .stApp {
        background-color: #F7F8F6 !important;
    }

    /* ── SIDEBAR BOLD COLOURS ── */

    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0A5540 0%, #1D9E75 60%, #2DBF8A 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0 20px rgba(10, 85, 64, 0.3) !important;
    }

    /* brand block */
    .brand-block {
        border-bottom: 0.5px solid rgba(255,255,255,0.2) !important;
    }
    .brand-name {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    .brand-sub {
        color: rgba(255,255,255,0.7) !important;
    }

    /* brand logo border */
    .brand-logo {
        border: 2px solid rgba(255,255,255,0.3) !important;
    }

    /* nav section label */
    section[data-testid="stSidebar"] .menu-title,
    section[data-testid="stSidebar"] [style*="font-size:10px"] {
        color: rgba(255,255,255,0.6) !important;
        font-weight: 600 !important;
    }

    /* nav items — default */
    section[data-testid="stSidebar"] .nav-link {
        color: rgba(255,255,255,0.85) !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .nav-link:hover {
        background: rgba(255,255,255,0.15) !important;
        color: #FFFFFF !important;
    }

    /* nav icons — default */
    section[data-testid="stSidebar"] .nav-link svg,
    section[data-testid="stSidebar"] .nav-link i {
        color: rgba(255,255,255,0.7) !important;
    }

    /* nav active item */
    section[data-testid="stSidebar"] .nav-link-selected {
        background: rgba(255,255,255,0.22) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.3) !important;
    }

    /* active icon */
    section[data-testid="stSidebar"] .nav-link-selected svg,
    section[data-testid="stSidebar"] .nav-link-selected i {
        color: #FFFFFF !important;
    }

    /* system section label */
    section[data-testid="stSidebar"] hr {
        border-top: 0.5px solid rgba(255,255,255,0.2) !important;
    }

    /* settings item */
    section[data-testid="stSidebar"] div[style*="color:#5F5E5A"] {
        color: rgba(255,255,255,0.85) !important;
    }
    section[data-testid="stSidebar"] i[style*="color:#B4B2A9"] {
        color: rgba(255,255,255,0.6) !important;
    }

    /* profile section */
    section[data-testid="stSidebar"] div[style*="color:#1a1a1a"] {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] div[style*="color:#888780"] {
        color: rgba(255,255,255,0.65) !important;
    }

    /* avatar */
    section[data-testid="stSidebar"] div[style*="border-radius:50%"] {
        background: rgba(255,255,255,0.2) !important;
        color: #FFFFFF !important;
        border: 1.5px solid rgba(255,255,255,0.4) !important;
    }

    /* role badge */
    section[data-testid="stSidebar"] div[style*="border-radius:20px"] {
        background: rgba(255,255,255,0.2) !important;
        color: #FFFFFF !important;
    }

    /* logout button */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.12) !important;
        color: #FFFFFF !important;
        border: 0.5px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(220, 53, 53, 0.4) !important;
        border-color: rgba(255,100,100,0.5) !important;
    }

    /* menu title text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] small {
        color: rgba(255,255,255,0.75) !important;
    }
    /* ── MAIN CONTENT AREA ── */
    .main .block-container {
        padding: 1.5rem 2rem 2rem !important;
        max-width: 1200px !important;
    }

    /* ── HEADINGS ── */
    h1 { font-size: 20px !important; font-weight: 500 !important; color: #1a1a1a !important; }
    h2 { font-size: 16px !important; font-weight: 500 !important; color: #1a1a1a !important; }
    h3 { font-size: 14px !important; font-weight: 500 !important; color: #1a1a1a !important; }

    /* ── METRIC CARDS (st.metric) ── */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 0.5px solid #E0E0D8 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 500 !important;
        color: #888780 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 500 !important;
        color: #1a1a1a !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
        color: var(--teal-400) !important;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background-color: transparent !important;
        color: var(--teal-600) !important;
        border: 1px solid var(--teal-400) !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    

    .stButton > button:active {
        background-color: transparent !important;
        transform: scale(0.98) !important;
    }

    /* secondary/outline buttons — any button whose label starts with ⬇ or Download */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: var(--teal-600) !important;
        border: 1px solid var(--teal-400) !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stDownloadButton > button:hover {
        background-color: var(--teal-50) !important;
    }

    /* ── TEXT INPUTS ── */
    .stTextInput > div > div > input {
        background: #FFFFFF !important;
        border: 0.5px solid #D3D1C7 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        color: #1a1a1a !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 8px 12px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--teal-400) !important;
        box-shadow: 0 0 0 2px rgba(29, 158, 117, 0.15) !important;
    }

    .stTextInput > label {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #5F5E5A !important;
    }

    /* ── SELECTBOX ── */
    .stSelectbox > div > div {
        background: #FFFFFF !important;
        border: 0.5px solid #D3D1C7 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stSelectbox > div > div:focus-within {
        border-color: var(--teal-400) !important;
        box-shadow: 0 0 0 2px rgba(29, 158, 117, 0.15) !important;
    }

    .stSelectbox > label {
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #5F5E5A !important;
    }

    /* ── FILE UPLOADER ── */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        border: 1px dashed #9FE1CB !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--teal-400) !important;
        background: var(--teal-50) !important;
    }

    /* ── DATAFRAME / TABLE ── */
    [data-testid="stDataFrame"] {
        border: 0.5px solid #E0E0D8 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] th {
        background-color: #F7F8F6 !important;
        color: #888780 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        border-bottom: 0.5px solid #E0E0D8 !important;
    }

    [data-testid="stDataFrame"] td {
        font-size: 13px !important;
        color: #1a1a1a !important;
        border-bottom: 0.5px solid #F1EFE8 !important;
    }

    [data-testid="stDataFrame"] tr:hover td {
        background-color: var(--teal-50) !important;
    }

    /* ── DATA EDITOR ── */
    [data-testid="stDataEditor"] {
        border: 0.5px solid #E0E0D8 !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* ── FORMS ── */
    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 0.5px solid #E0E0D8 !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
    }

    /* ── ALERTS ── */
    .stSuccess {
        background-color: var(--teal-50) !important;
        border-left: 3px solid var(--teal-400) !important;
        color: var(--teal-800) !important;
        border-radius: 0 8px 8px 0 !important;
        font-size: 13px !important;
    }

    .stWarning {
        background-color: var(--amber-50) !important;
        border-left: 3px solid #EF9F27 !important;
        color: var(--amber-800) !important;
        border-radius: 0 8px 8px 0 !important;
        font-size: 13px !important;
    }

    .stError {
        border-left: 3px solid #E24B4A !important;
        border-radius: 0 8px 8px 0 !important;
        font-size: 13px !important;
    }

    .stInfo {
        background-color: #E6F1FB !important;
        border-left: 3px solid #378ADD !important;
        border-radius: 0 8px 8px 0 !important;
        font-size: 13px !important;
    }

    /* ── DIVIDER ── */
    hr {
        border: none !important;
        border-top: 0.5px solid #E0E0D8 !important;
        margin: 1rem 0 !important;
    }

    /* ── CHECKBOX ── */
    .stCheckbox > label {
        font-size: 13px !important;
        color: #5F5E5A !important;
    }

    /* ── NUMBER INPUT ── */
    .stNumberInput > div > div > input {
        border: 0.5px solid #D3D1C7 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stNumberInput > div > div > input:focus {
        border-color: var(--teal-400) !important;
        box-shadow: 0 0 0 2px rgba(29, 158, 117, 0.15) !important;
    }

    /* ── SPINNER / TOAST ── */
    [data-testid="stToast"] {
        background: #1a1a1a !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-size: 13px !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #D3D1C7; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #B4B2A9; }

    /* ── LINE CHART (st.line_chart) ── */
    [data-testid="stArrowVegaLiteChart"] canvas {
        border-radius: 10px !important;
    }

    /* ── CAPTION / SMALL TEXT ── */
    .stCaption, small {
        font-size: 11px !important;
        color: #888780 !important;
    }

    /* ── MARKDOWN ── */
    .stMarkdown p {
        font-size: 13px !important;
        color: #3a3a3a !important;
        line-height: 1.6 !important;
    }
    /* ── DASHBOARD VIEW BUTTONS (ghost style) ── */
    [data-testid="stButton"][key^="btn_"] > button,
    div[data-testid="column"] .stButton > button {
        background-color: transparent !important;
        color: #1D9E75 !important;
        border: 0.5px solid #9FE1CB !important;
        font-size: 12px !important;
        padding: 5px 10px !important;
        border-radius: 0 0 8px 8px !important;
    }

    div[data-testid="column"] .stButton > button:hover {
        background-color: #E1F5EE !important;
    }
    /* ── LOGOUT BUTTON ── */
    [data-testid="stButton"][key="logout_btn"] > button,
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #E24B4A !important;
        border: 0.5px solid #F09595 !important;
        font-size: 12px !important;
        padding: 6px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #FCEBEB !important;
    }

    /* ── SIDEBAR ENHANCED COLOUR ── */

    /* sidebar background — soft teal tint instead of flat white */
    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, #F0FAF6 0%, #FFFFFF 60%) !important;
        border-right: 0.5px solid #C8EDE0 !important;
    }

    /* brand tile stronger */
    .brand-tile {
        background: #1D9E75 !important;
    }
    .brand-tile i {
        color: #FFFFFF !important;
    }

    /* nav active item — deeper green */
    section[data-testid="stSidebar"] [aria-selected="true"],
    section[data-testid="stSidebar"] .nav-link-selected {
        background-color: #1D9E75 !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }

    /* active icon white */
    section[data-testid="stSidebar"] [aria-selected="true"] svg,
    section[data-testid="stSidebar"] .nav-link-selected svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* inactive nav items slightly darker */
    section[data-testid="stSidebar"] .nav-link {
        color: #3D3D3A !important;
    }

    section[data-testid="stSidebar"] .nav-link:hover {
        background-color: #D4F0E5 !important;
        color: #0F6E56 !important;
    }

    /* avatar circle — solid teal */
    .profile-row .avatar,
    section[data-testid="stSidebar"] .avatar {
        background: #1D9E75 !important;
        color: #FFFFFF !important;
    }

    /* logout button — tinted red */
    section[data-testid="stSidebar"] .stButton > button {
        background: #FCEBEB !important;
        color: #C0392B !important;
        border: 0.5px solid #F09595 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #F5C6C6 !important;
        color: #922B21 !important;
    }

    /* section labels — stronger */
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] .menu-title {
        color: #2E8B6A !important;
        font-weight: 600 !important;
    }

    /* divider lines — teal tint */
    section[data-testid="stSidebar"] hr {
        border-top: 0.5px solid #C8EDE0 !important;
    }

    /* system settings item */
    section[data-testid="stSidebar"] .nav-item {
        color: #3D3D3A !important;
    }
    /* ── AMBER ACCENT THROUGHOUT ── */

    /* ── PAGE BACKGROUND — subtle warm tint ── */
    .stApp {
        background-color: #F7F6F2 !important;
    }

    /* ── SIDEBAR — warm gradient ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(170deg, #F0FAF6 0%, #FDF8F0 100%) !important;
        border-right: 0.5px solid #E8E4D8 !important;
    }

    /* ── METRIC CARDS — amber active state ── */
    .metric-card.active {
        border: 1.5px solid #E8A020 !important;
        background: linear-gradient(135deg, #FDF3E0 0%, #FEF9F0 100%) !important;
    }
    .metric-card.active .metric-card-value {
        color: #B86E00 !important;
    }

    /* ── TOP SEARCH BAR — warm border ── */
    .search-card {
        border: 0.5px solid #E8E0CC !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #FDFAF4 100%) !important;
    }

    /* ── DATAFRAME HEADER — warm tint ── */
    [data-testid="stDataFrame"] th {
        background-color: #FDF8F0 !important;
    }

    /* ── CARDS — warm white ── */
    [data-testid="stForm"],
    .stDataFrame,
    [data-testid="stDataEditor"] {
        background: #FDFCF8 !important;
    }

    /* ── DIVIDERS — warm tone ── */
    hr {
        border-top: 0.5px solid #E8E0CC !important;
    }

    /* ── DOWNLOAD BUTTONS — amber outline ── */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: #B86E00 !important;
        border: 1px solid #E8A020 !important;
        border-radius: 8px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #FDF3E0 !important;
    }

    /* ── SELECTBOX FOCUS — amber ring ── */
    .stSelectbox > div > div:focus-within {
        border-color: #E8A020 !important;
        box-shadow: 0 0 0 2px rgba(232,160,32,0.15) !important;
    }

    /* ── ANALYTICS STAT CARDS — amber card ── */
    [data-testid="stMarkdownContainer"] div[style*="background:#FAEEDA"] {
        background: linear-gradient(135deg, #FDF3E0, #FEF9F0) !important;
    }

    /* ── SIDEBAR NAV HOVER — warm green ── */
    section[data-testid="stSidebar"] .nav-link:hover {
        background: linear-gradient(135deg, #E1F5EE, #FDF8F0) !important;
    }

    /* ── SECTION HEADERS — amber dot accent ── */
    .stMarkdown h1::before,
    .stMarkdown h2::before,
    .stMarkdown h3::before {
        content: '';
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #E8A020;
        margin-right: 8px;
        vertical-align: middle;
        margin-bottom: 2px;
    }

    /* ── TOAST NOTIFICATIONS — amber ── */
    [data-testid="stToast"] {
        background: #1a1a1a !important;
        border-left: 3px solid #E8A020 !important;
    }

    /* ── SUCCESS ALERTS — keep teal ── */
    .stSuccess {
        background: linear-gradient(135deg, #E1F5EE, #F0FAF6) !important;
        border-left: 3px solid #1D9E75 !important;
    }

    /* ── WARNING ALERTS — amber ── */
    .stWarning {
        background: linear-gradient(135deg, #FDF3E0, #FEF9F0) !important;
        border-left: 3px solid #E8A020 !important;
        color: #854F0B !important;
    }

    /* ── INFO ALERTS — warm blue ── */
    .stInfo {
        background: linear-gradient(135deg, #EEF4FC, #F5F8FE) !important;
        border-left: 3px solid #378ADD !important;
    }

    /* ── SCROLLBAR — warm tone ── */
    ::-webkit-scrollbar-thumb {
        background: #D4C9A8 !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #C4B48A !important;
    }

    /* ── LOGIN PAGE GRADIENT — include amber ── */
    /* this targets the teal gradient and adds warmth at the bottom */
    .stApp[data-testid="stAppViewContainer"] {
        background: linear-gradient(
            160deg,
            #0A5540 0%,
            #1D9E75 45%,
            #5DCAA5 75%,
            #A8D5A2 100%
        ) !important;
    }
                /* ── GLOBAL FONT SIZE INCREASE ── */

    /* base font */
    html, body, .stApp, [class*="css"] {
        font-size: 15px !important;
    }

    /* general text */
    p, div, span, label, td, th, li {
        font-size: 15px !important;
    }

    /* markdown text */
    .stMarkdown p {
        font-size: 15px !important;
    }

    /* inputs */
    .stTextInput > div > div > input {
        font-size: 15px !important;
    }

    /* selectbox */
    .stSelectbox > div > div {
        font-size: 15px !important;
    }

    /* number input */
    .stNumberInput > div > div > input {
        font-size: 15px !important;
    }

    /* buttons */
    .stButton > button {
        font-size: 14px !important;
    }

    .stDownloadButton > button {
        font-size: 14px !important;
    }

    .stFormSubmitButton > button {
        font-size: 15px !important;
    }

    /* dataframe */
    [data-testid="stDataFrame"] td {
        font-size: 14px !important;
    }

    [data-testid="stDataFrame"] th {
        font-size: 12px !important;
    }

    /* sidebar nav */
    section[data-testid="stSidebar"] .nav-link {
        font-size: 14px !important;
    }

    /* captions */
    .stCaption, small {
        font-size: 12px !important;
    }

    /* metric cards */
    .metric-card-label {
        font-size: 12px !important;
    }

    .metric-card-value {
        font-size: 30px !important;
    }

    /* alerts */
    .stSuccess, .stWarning, .stError, .stInfo {
        font-size: 14px !important;
    }

    /* checkbox */
    .stCheckbox > label {
        font-size: 14px !important;
    }

    /* table cells in custom HTML tables */
    .grad-table td, .analytics-table td, .user-table td {
        font-size: 13px !important;
    }

    .grad-table th, .analytics-table th, .user-table th {
        font-size: 11px !important;
    }
    /* ── SIDEBAR TEXT OVERRIDES — black items ── */

    /* ACC Archives brand name */
    .brand-name {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    .brand-sub {
        color: #5F5E5A !important;
    }

    /* logout button — dark text */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.9) !important;
        color: #1a1a1a !important;
        border: 0.5px solid rgba(255,255,255,0.5) !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #FCEBEB !important;
        color: #C0392B !important;
        border-color: #F09595 !important;
    }


    /* the sidebar collapse arrow button */
    button[data-testid="baseButton-headerNoPadding"] svg {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
        stroke: #1a1a1a !important;
    }

    /* username text in profile */
    section[data-testid="stSidebar"] div[style*="font-weight:500"][style*="color"] {
        color: #1a1a1a !important;
    }
    /* ── LOGOUT BUTTON — reset to original ── */
    section[data-testid="stSidebar"] .stButton > button {
        background: #FCEBEB !important;
        color: #C0392B !important;
        border: 0.5px solid #F09595 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        padding: 6px !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #F5C6C6 !important;
        color: #922B21 !important;
    }

    section[data-testid="stSidebar"] .stButton > button * {
        color: #C0392B !important;
    }
                
        </style>
    """, unsafe_allow_html=True)