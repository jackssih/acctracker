import streamlit as st

def login():
    # Initialize session state
    if "auth" not in st.session_state:
        st.session_state.auth = False

    # If already logged in → don't show login UI again
    if st.session_state.auth:
        return True

    # --- Login UI ---
    st.title("🔐 Admin Login")

    # Wrap inputs in a form (VERY IMPORTANT FIX)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    return False