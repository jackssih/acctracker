import streamlit as st
import bcrypt
import pandas as pd
from database import connect_db


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def load_users():
    conn = connect_db()
    users = pd.read_sql(
        "SELECT id, username, role, created_at, created_by FROM users",
        conn
    )
    conn.close()
    return users


def render_user_management():

    if st.session_state.get("role") != "admin":
        st.warning("You don't have permission to access this page.")
        st.stop()

    st.markdown("**User Management**")
    st.caption("Manage who can access the system and what they can do")
    st.markdown("---")

    users = load_users()

    # ── STAT CARDS ──
    total_users = len(users)
    admins = len(users[users["role"] == "admin"])
    viewers = len(users[users["role"] == "viewer"])

    c1, c2, c3 = st.columns(3)
    for col, label, value, icon, bg, color in [
        (c1, "Total users",  total_users, "ti-users",      "#E1F5EE", "#1D9E75"),
        (c2, "Admins",       admins,      "ti-shield",     "#FAEEDA", "#EF9F27"),
        (c3, "Viewers",      viewers,     "ti-eye",        "#E6F1FB", "#378ADD"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                        padding:14px 16px; display:flex; align-items:center; gap:12px;
                        margin-bottom:10px;">
                <div style="width:36px; height:36px; border-radius:9px; background:{bg};
                            display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                    <i class="ti {icon}" style="font-size:18px; color:{color};"></i>
                </div>
                <div>
                    <div style="font-size:11px; color:#888780; margin-bottom:3px;">{label}</div>
                    <div style="font-size:22px; font-weight:500; color:#1a1a1a;">{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── ADD USER ──
    left, right = st.columns([1, 2])

    with left:
        st.markdown("**Add new user**")
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            new_role = st.selectbox("Role", ["viewer", "admin"])

            st.markdown(f"""
            <div style="background:#F7F8F6; border:0.5px solid #E0E0D8; border-radius:8px;
                        padding:10px 12px; margin:8px 0; font-size:12px; color:#5F5E5A;">
                <strong>Role permissions</strong><br><br>
                <b>Admin</b> — full access: add, edit, delete, upload, manage users<br><br>
                <b>Viewer</b> — read only: search and view data, no edits
            </div>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("Add user", use_container_width=True)

        if submitted:
            if not new_username or not new_password:
                st.error("Username and password are required")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                try:
                    conn = connect_db()
                    conn.execute("""
                        INSERT INTO users (username, password_hash, role, created_by)
                        VALUES (?, ?, ?, ?)
                    """, (
                        new_username,
                        hash_password(new_password),
                        new_role,
                        st.session_state.get("username", "admin")
                    ))
                    conn.commit()
                    conn.close()
                    st.success(f"User '{new_username}' added as {new_role}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Username already exists")

    # ── USER TABLE ──
    with right:
        st.markdown("**All users**")

        search = st.text_input(
            "Search users",
            placeholder="Search by username...",
            label_visibility="collapsed"
        )

        filtered_users = users.copy()
        if search:
            filtered_users = filtered_users[
                filtered_users["username"].str.contains(search, case=False)
            ]

        if filtered_users.empty:
            st.info("No users found")
        else:
            rows_html = ""
            for _, row in filtered_users.iterrows():
                role_badge = (
                    '<span style="background:#FAEEDA; color:#854F0B; font-size:10px; '
                    'font-weight:500; padding:2px 8px; border-radius:20px;">Admin</span>'
                    if row["role"] == "admin"
                    else
                    '<span style="background:#E6F1FB; color:#1A5FA8; font-size:10px; '
                    'font-weight:500; padding:2px 8px; border-radius:20px;">Viewer</span>'
                )
                ini = row["username"][:2].upper()
                created = str(row["created_at"])[:10] if row["created_at"] else "—"
                by = row["created_by"] if row["created_by"] else "—"

                rows_html += f"""
                <tr>
                    <td>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <div style="width:26px; height:26px; border-radius:50%;
                                        background:#E1F5EE; color:#0F6E56; font-size:10px;
                                        font-weight:500; display:flex; align-items:center;
                                        justify-content:center; flex-shrink:0;">{ini}</div>
                            {row['username']}
                        </div>
                    </td>
                    <td>{role_badge}</td>
                    <td style="color:#888780;">{created}</td>
                    <td style="color:#888780;">{by}</td>
                </tr>
                """

            st.markdown(f"""
            <style>
            .user-table {{ width:100%; border-collapse:collapse; }}
            .user-table th {{
                text-align:left; font-size:10px; font-weight:500; color:#B4B2A9;
                text-transform:uppercase; letter-spacing:0.06em;
                padding:0 10px 10px; border-bottom:0.5px solid #E0E0D8;
            }}
            .user-table td {{
                font-size:12px; color:#1a1a1a; padding:9px 10px;
                border-bottom:0.5px solid #F1EFE8; vertical-align:middle;
            }}
            .user-table tr:last-child td {{ border-bottom:none; }}
            .user-table tr:hover td {{ background:#F7F8F6; }}
            </style>
            <table class="user-table">
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Role</th>
                        <th>Created</th>
                        <th>Added by</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

        # ── DELETE USER ──
        st.markdown("---")
        st.markdown("**Remove user**")

        with st.form("delete_user_form"):
            usernames = users[users["username"] != "admin"]["username"].tolist()
            to_delete = st.selectbox(
                "Select user to remove",
                ["— select —"] + usernames
            )
            confirm = st.checkbox("I confirm I want to remove this user")
            delete_submitted = st.form_submit_button(
                "Remove user", use_container_width=True
            )

        if delete_submitted:
            if to_delete == "— select —":
                st.error("Please select a user")
            elif not confirm:
                st.error("Please confirm the deletion")
            else:
                conn = connect_db()
                conn.execute(
                    "DELETE FROM users WHERE username = ?", (to_delete,)
                )
                conn.commit()
                conn.close()
                st.success(f"User '{to_delete}' removed")
                st.rerun()