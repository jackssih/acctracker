import streamlit as st
import bcrypt
from database import connect_db
import base64
from pathlib import Path


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def get_user(username: str):
    conn = connect_db(row_factory=True)
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def login():
    if st.session_state.get("auth"):
        return True

    # ── LOAD IMAGE AS BASE64 BACKGROUND ──
    logo_path = Path("logo one.jpg")
    bg_style = ""
    if logo_path.exists():
        img_b64 = base64.b64encode(logo_path.read_bytes()).decode()
        bg_style = f"""
        .stApp::before {{
            content: '';
            position: fixed;
            inset: 0;
            background-image: url("data:image/jpeg;base64,{img_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.12;
            z-index: 0;
        }}
        """

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap');

    * {{ font-family: 'DM Sans', sans-serif; box-sizing: border-box; }}

    html, body {{ margin: 0; padding: 0; }}

    .stApp {{
        background: linear-gradient(135deg, #0A5540 0%, #1D9E75 55%, #5DCAA5 100%) !important;
        min-height: 100vh;
    }}

    {bg_style}

    /* hide streamlit chrome */
    #MainMenu, footer, header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {{
        display: none !important;
    }}

    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
        margin: 0 !important;
    }}

    section[data-testid="stMain"] > div {{
        padding: 0 !important;
    }}

    /* ── FULL PAGE CENTER ── */
    .login-outer {{
        min-height: 100vh;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 1;
        padding: 2rem;
    }}

    /* ── CARD ── */
    .login-card {{
        background: rgba(255, 255, 255, 0.97);
        border-radius: 20px;
        padding: 40px 36px 32px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 24px 64px rgba(10, 85, 64, 0.3),
                    0 4px 16px rgba(0,0,0,0.1);
        position: relative;
        z-index: 2;
    }}

    /* ── HEADER ── */
    .login-header {{
        text-align: center;
        margin-bottom: 28px;
    }}
    .login-system-name {{
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        line-height: 1.3;
        margin-bottom: 5px;
    }}
    .login-system-sub {{
        font-size: 12px;
        color: #888780;
    }}
    .login-divider {{
        border: none;
        border-top: 0.5px solid #E0E0D8;
        margin: 20px 0 22px;
    }}
    .login-heading {{
        font-size: 16px;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 3px;
    }}
    .login-desc {{
        font-size: 12px;
        color: #888780;
        margin-bottom: 20px;
    }}

    /* ── INPUTS ── */
    .stTextInput > div > div > input {{
        border: 0.5px solid #D3D1C7 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        background: #FAFAF9 !important;
        transition: all 0.15s !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #1D9E75 !important;
        box-shadow: 0 0 0 3px rgba(29,158,117,0.15) !important;
        background: #FFFFFF !important;
    }}
    .stTextInput > label {{
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #5F5E5A !important;
    }}

    /* ── SIGN IN BUTTON ── */
    .stFormSubmitButton > button {{
        background: linear-gradient(135deg, #1D9E75, #0A5540) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 12px !important;
        width: 100% !important;
        margin-top: 6px !important;
        box-shadow: 0 4px 16px rgba(29,158,117,0.4) !important;
        transition: all 0.2s !important;
        letter-spacing: 0.02em !important;
    }}
    .stFormSubmitButton > button:hover {{
        box-shadow: 0 8px 24px rgba(29,158,117,0.5) !important;
        transform: translateY(-1px) !important;
    }}

    /* ── FOOTER ── */
    .login-footer {{
        text-align: center;
        font-size: 11px;
        color: #B4B2A9;
        margin-top: 20px;
    }}

    /* ── ERROR ── */
    [data-testid="stAlert"] {{
        border-radius: 10px !important;
        font-size: 13px !important;
        margin-top: 8px !important;
    }}
    </style>

    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">

    <div class="login-outer">
      <div class="login-card">
        <div class="login-header">
            <div class="login-system-name">African Children's<br>Choir Archives</div>
            <div class="login-system-sub">Data Tracker v1.0</div>
        </div>
        <hr class="login-divider">
        <div class="login-heading">Welcome back</div>
        <div class="login-desc">Sign in to your account to continue</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STREAMLIT FORM (rendered naturally, centered by block-container) ──
    _, center, _ = st.columns([2, 2 , 2])
    with center:
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            submitted = st.form_submit_button(
                "Sign in",
                use_container_width=True
            )

        st.markdown("""
        <div class="login-footer">
            African Children's Choir Archives · v1.0
        </div>
        """, unsafe_allow_html=True)

    # ── AUTH ──
    if submitted:
        user = get_user(username)
        if user and verify_password(password, user["password_hash"]):
            st.session_state.auth = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            st.rerun()
        else:
            st.error("Incorrect username or password")

    return False