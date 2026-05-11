import streamlit as st
import bcrypt
import pandas as pd
import os
import shutil
from pathlib import Path
from database import connect_db
from choir_logic import load_full_dataset


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def render_settings():

    st.markdown("**Settings**")
    st.caption("System preferences and account management")
    st.markdown("---")

    # ── STAT CARDS ──
    conn = connect_db()
    total_students = pd.read_sql(
        "SELECT COUNT(*) as c FROM choir_data", conn
    ).iloc[0]["c"]
    total_graduated = pd.read_sql(
        "SELECT COUNT(*) as c FROM graduation_data", conn
    ).iloc[0]["c"]
    total_users = pd.read_sql(
        "SELECT COUNT(*) as c FROM users", conn
    ).iloc[0]["c"]
    db_size = os.path.getsize("data/choir.db") / 1024
    conn.close()

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, icon, bg, color in [
        (c1, "Total students", int(total_students), "ti-users",       "#E1F5EE", "#1D9E75"),
        (c2, "Graduates",      int(total_graduated),"ti-certificate", "#FAEEDA", "#EF9F27"),
        (c3, "System users",   int(total_users),    "ti-shield",      "#E6F1FB", "#378ADD"),
        (c4, "Database size",  f"{db_size:.1f} KB", "ti-database",    "#F3EEF8", "#8B5CF6"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                        padding:14px 16px; display:flex; align-items:center; gap:12px;
                        margin-bottom:12px;">
                <div style="width:36px; height:36px; border-radius:9px; background:{bg};
                            display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                    <i class="ti {icon}" style="font-size:18px; color:{color};"></i>
                </div>
                <div>
                    <div style="font-size:11px; color:#888780; margin-bottom:2px;">{label}</div>
                    <div style="font-size:18px; font-weight:500; color:#1a1a1a;">{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── TWO COLUMN LAYOUT ──
    left_col, right_col = st.columns(2)

    # ──────────────────────────────────────────
    # LEFT COLUMN
    # ──────────────────────────────────────────
    with left_col:

        # ── CHANGE PASSWORD ──
        st.markdown("**Change password**")
        with st.form("change_password_form"):
            current_pw = st.text_input(
                "Current password", type="password",
                placeholder="Enter current password"
            )
            new_pw = st.text_input(
                "New password", type="password",
                placeholder="Enter new password"
            )
            confirm_pw = st.text_input(
                "Confirm new password", type="password",
                placeholder="Confirm new password"
            )
            pw_submit = st.form_submit_button(
                "Update password", use_container_width=True
            )

        if pw_submit:
            if not current_pw or not new_pw or not confirm_pw:
                st.error("All fields are required")
            elif new_pw != confirm_pw:
                st.error("New passwords do not match")
            elif len(new_pw) < 6:
                st.error("Password must be at least 6 characters")
            else:
                conn = connect_db(row_factory=True)
                user = conn.execute(
                    "SELECT * FROM users WHERE username = ?",
                    (st.session_state.get("username"),)
                ).fetchone()
                conn.close()

                if user and bcrypt.checkpw(
                    current_pw.encode(), user["password_hash"].encode()
                ):
                    conn = connect_db()
                    conn.execute(
                        "UPDATE users SET password_hash = ? WHERE username = ?",
                        (hash_password(new_pw),
                         st.session_state.get("username"))
                    )
                    conn.commit()
                    conn.close()
                    st.success("Password updated successfully")
                else:
                    st.error("Current password is incorrect")

        st.markdown("---")

        
        

        # ── SYSTEM INFO ──
        st.markdown("**System info**")
        st.markdown(f"""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:14px 16px; font-size:13px;">
            <div style="display:flex; justify-content:space-between; padding:6px 0;
                        border-bottom:0.5px solid #F1EFE8;">
                <span style="color:#888780;">System name</span>
                <span style="font-weight:500;">ACC Archives</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0;
                        border-bottom:0.5px solid #F1EFE8;">
                <span style="color:#888780;">Version</span>
                <span style="font-weight:500;">v1.0</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0;
                        border-bottom:0.5px solid #F1EFE8;">
                <span style="color:#888780;">Database</span>
                <span style="font-weight:500;">SQLite · {db_size:.1f} KB</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0;
                        border-bottom:0.5px solid #F1EFE8;">
                <span style="color:#888780;">Logged in as</span>
                <span style="font-weight:500;">{st.session_state.get('username', '—')}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:6px 0;">
                <span style="color:#888780;">Role</span>
                <span style="font-weight:500; color:#1D9E75;">
                    {st.session_state.get('role', '—').capitalize()}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # RIGHT COLUMN
    # ──────────────────────────────────────────
    with right_col:

        # ── EXPORT ALL DATA ──
        st.markdown("**Export all data**")
        st.markdown("""
        <div style="background:#F7F8F6; border:0.5px solid #E0E0D8; border-radius:10px;
                    padding:10px 14px; font-size:12px; color:#5F5E5A; margin-bottom:10px;">
            Download all student and graduation records as a single CSV file.
        </div>
        """, unsafe_allow_html=True)

        data = load_full_dataset()
        if data.empty:
            st.info("No data to export yet.")
        else:
            export_cols = [
                "identification_no", "name", "choir", "gender",
                "status", "institute", "course_name",
                "year_of_graduation", "comment"
            ]
            export_cols = [c for c in export_cols if c in data.columns]
            csv_all = data[export_cols].to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download all data (CSV)",
                csv_all,
                "acc_archives_export.csv",
                "text/csv",
                use_container_width=True,
                key="export_all"
            )

            # export by choir
            st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
            choirs = sorted(data["choir"].dropna().unique().tolist())
            selected_choir = st.selectbox(
                "Or export by choir",
                ["All choirs"] + choirs,
                key="export_choir_select"
            )
            if selected_choir != "All choirs":
                choir_data = data[data["choir"] == selected_choir]
                csv_choir = choir_data[export_cols].to_csv(
                    index=False
                ).encode("utf-8")
                st.download_button(
                    f"Download {selected_choir}",
                    csv_choir,
                    f"{selected_choir.replace(' ', '_')}_export.csv",
                    "text/csv",
                    use_container_width=True,
                    key="export_choir"
                )

        st.markdown("---")

        # ── BACKUP DATABASE ──
        st.markdown("**💾 Backup database**")
        st.markdown("""
        <div style="background:#F7F8F6; border:0.5px solid #E0E0D8; border-radius:10px;
                    padding:10px 14px; font-size:12px; color:#5F5E5A; margin-bottom:10px;">
            Download a full backup of the raw database file.
            Keep this somewhere safe — it contains all your data.
        </div>
        """, unsafe_allow_html=True)

        db_path = Path("data/choir.db")
        if db_path.exists():
            with open(db_path, "rb") as f:
                db_bytes = f.read()
            st.download_button(
                "Download database backup (.db)",
                db_bytes,
                "choir_backup.db",
                "application/octet-stream",
                use_container_width=True,
                key="backup_db"
            )
        else:
            st.error("Database file not found")

        st.markdown("---")

        # ── RESET VIEWS ──
        st.markdown("**Reset views**")
        st.markdown("""
        <div style="background:#F7F8F6; border:0.5px solid #E0E0D8; border-radius:10px;
                    padding:10px 14px; font-size:12px; color:#5F5E5A; margin-bottom:10px;">
            Clear all cached session data and reset dashboard views.
            Your data is not affected.
        </div>
        """, unsafe_allow_html=True)

        with st.form("reset_form"):
            st.markdown("""
            <div style="background:#FAEEDA; border:0.5px solid #EF9F27; border-radius:8px;
                        padding:8px 12px; font-size:12px; color:#854F0B;
                        display:flex; align-items:center; gap:7px; margin-bottom:10px;">
                <i class="ti ti-alert-triangle" style="font-size:14px;"></i>
                This will clear all filters, search results and cached views.
            </div>
            """, unsafe_allow_html=True)

            confirm_reset = st.checkbox("I understand, reset everything")
            reset_submit = st.form_submit_button(
                "Reset views", use_container_width=True
            )

        if reset_submit:
            if not confirm_reset:
                st.error("Please check the confirmation box")
            else:
                keys_to_clear = [
                    "edited_df", "dashboard_view", "global_results",
                    "global_result_label", "search_menu_tracker",
                    "last_menu", "view"
                ]
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Views reset successfully")
                st.rerun()