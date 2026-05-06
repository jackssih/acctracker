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

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 0.5px solid #E0E0D8 !important;
    }

    section[data-testid="stSidebar"] * {
        font-family: 'DM Sans', sans-serif !important;
    }

    /* sidebar nav menu active item */
    section[data-testid="stSidebar"] .nav-link.active,
    section[data-testid="stSidebar"] [aria-selected="true"] {
        background-color: var(--teal-50) !important;
        color: var(--teal-600) !important;
        border-right: 2px solid var(--teal-400) !important;
        border-radius: 0 !important;
        font-weight: 500 !important;
    }

    /* sidebar nav item hover */
    section[data-testid="stSidebar"] .nav-link:hover {
        background-color: var(--teal-50) !important;
        color: var(--teal-600) !important;
    }

    /* sidebar icons */
    section[data-testid="stSidebar"] .nav-link .icon {
        color: var(--teal-400) !important;
    }

    /* sidebar header text */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #888780 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
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
        background-color: var(--teal-400) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 18px !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: background 0.15s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--teal-600) !important;
    }

    .stButton > button:active {
        background-color: var(--teal-800) !important;
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
        </style>
    """, unsafe_allow_html=True)