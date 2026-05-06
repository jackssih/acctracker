import streamlit as st
import bcrypt 
from database import connect_db


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def get_user(username: str):
    conn = connect_db(row_factory=True)  # ← dict access
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def login():
    if st.session_state.get("auth"):
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap');
    * { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #F7F8F6; }
    .login-wrap {
        max-width: 380px;
        margin: 6vh auto 0;
        background: #FFFFFF;
        border: 0.5px solid #E0E0D8;
        border-radius: 16px;
        padding: 36px 32px;
    }
    .login-brand {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 28px;
    }
    .login-tile {
        width: 36px; height: 36px; border-radius: 9px;
        background: #E1F5EE;
        display: flex; align-items: center; justify-content: center;
    }
    .login-tile i { font-size: 19px; color: #1D9E75; }
    .login-name { font-size: 15px; font-weight: 500; color: #1a1a1a; }
    .login-sub  { font-size: 11px; color: #888780; }
    .login-title { font-size: 18px; font-weight: 500; color: #1a1a1a; margin-bottom: 4px; }
    .login-desc  { font-size: 12px; color: #888780; margin-bottom: 24px; }
    </style>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">

    <div class="login-wrap">
        <div class="login-brand">
            <div class="login-tile"><i class="ti ti-music"></i></div>
            <div>
                <div class="login-name">Choir Tracker</div>
                <div class="login-sub">African Children's Choir</div>
            </div>
        </div>
        <div class="login-title">Welcome back</div>
        <div class="login-desc">Sign in to your account to continue</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)

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