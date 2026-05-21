import streamlit as st
from database import create_tables
from auth import login
from services import upload_choir_data, upload_graduation_data
import pandas as pd
from choir_logic import load_full_dataset
from streamlit_option_menu import option_menu
from database import connect_db
from user_management import render_user_management
from settings import render_settings
import base64
from pathlib import Path
import re
from database import create_tables, verify_database, get_db_size

# Initialize database with session state to prevent multiple initializations
if 'db_initialized' not in st.session_state:
    try:
        create_tables()
        st.session_state.db_initialized = True
        st.session_state.db_size = get_db_size()
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        st.stop()

# Verify database on each session
if not verify_database():
    st.error("Database verification failed. Please contact administrator.")
    st.stop()
def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', s)]
def is_admin():
    return st.session_state.get("role") == "admin"

def refresh_data():
    st.session_state.edited_df = load_full_dataset()
create_tables()

st.set_page_config(
    page_title="African Children's Choir Archives",
    layout="wide"
)
from choir_theme import inject_theme
inject_theme()
# LOGIN
if not login():
    st.stop()

# BAR NAVIGATION
with st.sidebar:
    # ── BRAND + LOGO ──
    logo_path = Path("logo one.jpg")
    
    
    
    if logo_path.exists():
        img_b64 = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(f"""
            <style>
            section[data-testid="stSidebar"] > div {{ padding-top: 0 !important; }}
            .brand-block {{
                display: flex; align-items: center; gap: 10px;
                padding: 14px 16px;
                border-bottom: 0.5px solid #C8EDE0;
            }}
            .brand-logo {{
                width: 60px; height: 60px; border-radius: 8px;
                overflow: hidden; flex-shrink: 0;
                border: 1px solid #E1F5EE;
            }}
            .brand-logo img {{
                width: 100%; height: 100%; object-fit: contain;
            }}
            .brand-name {{ font-size: 13px; font-weight: 500; color: #1a1a1a; line-height: 1.3; }}
            .brand-sub  {{ font-size: 10px; color: #888780; }}
            </style>
            <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
            <div class="brand-block">
                <div class="brand-logo">
                    <img src="data:image/jpeg;base64,{img_b64}" alt="ACC Logo">
                </div>
                <div>
                    <div class="brand-name">ACC Archives</div>
                    <div class="brand-sub">African Children's Choir</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
        .brand-block {
            display: flex; align-items: center; gap: 10px;
            padding: 14px 16px;
            border-bottom: 0.5px solid #C8EDE0;
        }
        .brand-tile {
            width: 36px; height: 36px; border-radius: 8px;
            background: #1D9E75;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .brand-tile i { font-size: 18px; color: #FFFFFF; }
        .brand-name { font-size: 18px; font-weight: 500; color: #1a1a1a; }
        .brand-sub  { font-size: 10px; color: #888780; }
        </style>
        <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <div class="brand-block">
            <div class="brand-tile"><i class="ti ti-music"></i></div>
            <div>
                <div class="brand-name">ACC Archives</div>
                <div class="brand-sub">African Children's Choir</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── NAV MENU ──
    menu = option_menu(
    menu_title="Menu",
    options=[
    "Dashboard",
    "Manage Data",
    "Analytics",
    "User Management",
    "Settings",
    ],
    icons=[
        "speedometer2",
        "cloud-upload",
        "bar-chart-line",
        "people",
        "gear",
    ],
    default_index=0,
styles={
    "container": {
        "padding": "0 10px",
        "background-color": "#F5F5F0",
        "border-radius": "20px",
        "transition": "all 0.3s ease",
        "position": "relative",
        "margin": "4px 0",
    },
    "menu-title": {
        "font-size": "19px",
        "font-weight": "600",
        "color": "#1C180A",
        "text-transform": "uppercase",
        "letter-spacing": "0.08em",
        "padding": "0 6px",
        "margin-bottom": "4px",
    },
    "icon": {
        "font-size": "16px",
        "color": "#161406",
    },
    "nav-link": {
        "font-size": "18px",
        "color": "#0A0F08",
        "border-radius": "8px",
        "padding": "8px 10px",
        "margin-bottom": "1px",
    },
    "nav-link-selected": {
        "background-color": "#B65112",
        "color": "#FFFFFF",
        "font-weight": "500",
    },
    "icon-selected": {
        "color": "#35E1AB",
    },
}
)
    # ── DIVIDER + SETTINGS ──
    

    # ── PROFILE + LOGOUT AT BOTTOM ──
 # ── PROFILE + LOGOUT AT BOTTOM ──
    # Replace the existing profile+logout block in app.py with this:

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown("""
    <hr style="border:none; border-top: 1px solid rgba(61,255,154,0.12); margin: 8px 10px 0;">
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "user")
    role = st.session_state.get("role", "viewer")
    ini = username[:2].upper()

    # role badge class
    badge_class = "admin" if role == "admin" else "viewer"

    st.markdown(f"""
    <div class="sidebar-profile" style="display:flex; align-items:center; gap:10px;">
        <div class="sidebar-avatar">{ini}</div>
        <div style="flex:1;">
            <div class="sidebar-username">{username}</div>
            <span class="role-badge {badge_class}">{role.capitalize()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True, key="logout_btn"):
        st.session_state.auth = False
        st.rerun()
if "last_menu" not in st.session_state:
    st.session_state.last_menu = None

if st.session_state.last_menu != menu:
    refresh_data()   # refresh every time you change page
    st.session_state.last_menu = menu


# detect page switch
if st.session_state.last_menu != menu:
    st.session_state.search_results = None
    st.session_state.last_menu = menu
# ---------------- LOAD DATA FIRST ----------------
if "edited_df" not in st.session_state:
    st.session_state.edited_df = load_full_dataset()


# ---------------- INIT SESSION STATE ----------------
if "view" not in st.session_state:
    st.session_state.view = "all"

if "edited_df" not in st.session_state:
    st.session_state.edited_df = load_full_dataset()
# ---------------- RESET SEARCH ON PAGE CHANGE ----------------
if "search_menu_tracker" not in st.session_state:
    st.session_state.search_menu_tracker = menu

if st.session_state.search_menu_tracker != menu:
    st.session_state.search_menu_tracker = menu
    for key in ["global_search", "global_choir_filter", "global_gender_filter", "global_status_filter", "global_search_btn"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
# ---------------- GLOBAL SEARCH BAR ----------------
# ---------------- SEARCH ONLY ON DASHBOARD ----------------
if menu == "Dashboard":
    data = load_full_dataset()
    st.session_state.edited_df = data

    # ── SEARCH + SORT ROW ──
    space, search_col, sort_col = st.columns([2,1.5, 1])

    with search_col:
        left, right = st.columns([6, 0.8])
        with left:
            search_query = st.text_input(
                "search",
                placeholder="  Search student by name or ID...",
                label_visibility="collapsed"
            )
        with right:
            search_clicked = st.button("⌕", use_container_width=True)

    with sort_col:
        choirs = sorted(
            data["choir"].dropna().unique().tolist(),
            key=natural_sort_key
        )
        sort_options = (
            ["All students"]
            + [f"Choir · {c}" for c in choirs]
            + ["Gender · Male", "Gender · Female"]
            + ["Status · Graduated", "Status · Not Graduated", "Status · Deceased"]
        )
        sort_by = st.selectbox(
            "Sort by",
            sort_options,
            key="dashboard_sort"
        )
    with space:
        st.title("**Dashboard**")
        st.caption("Track and edit all your choir data")
    # ── SEARCH LOGIC ──
    if search_clicked:
        results = data.copy()

        if search_query:
            results = results[
                results["name"].fillna("").str.contains(search_query, case=False) |
                results["identification_no"].astype(str).str.contains(search_query, case=False)
            ]

        # apply sort_by filter on top of search
        if sort_by != "All students":
            if sort_by.startswith("Choir · "):
                choir_val = sort_by.replace("Choir · ", "")
                results = results[results["choir"] == choir_val]
            elif sort_by == "Gender · Male":
                results = results[results["gender"] == "M"]
            elif sort_by == "Gender · Female":
                results = results[results["gender"] == "F"]
            elif sort_by == "Status · Graduated":
                results = results[results["graduated"] == True]
            elif sort_by == "Status · Not Graduated":
                results = results[results["graduated"] == False]
            elif sort_by == "Status · Deceased":
                results = results[results["status"] == "deceased"]

        st.session_state.global_results = results
        st.session_state.global_result_label = (
            f"{len(results)} result(s)"
            + (f" · {search_query}" if search_query else "")
            + (f" · {sort_by}" if sort_by != "All students" else "")
        )

    # ── SHOW RESULTS ──
    if "global_results" not in st.session_state:
        st.session_state.global_results = None

    if st.session_state.global_results is not None:
        results = st.session_state.global_results
        label = st.session_state.get("global_result_label", "")

        r_col, c_col = st.columns([5, 1])
        with r_col:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px;
                        background:#FFFFFF; border:0.5px solid #E0E0D8;
                        border-radius:10px; padding:9px 14px; margin:8px 0;">
                <span style="background:#E1F5EE; color:#0F6E56; font-size:12px;
                             font-weight:500; padding:2px 10px; border-radius:20px;">
                    {len(results)}
                </span>
                <span style="font-size:12px; color:#888780;">{label}</span>
            </div>
            """, unsafe_allow_html=True)
        with c_col:
            if st.button("✕ Clear", use_container_width=True, key="clear_search"):
                st.session_state.global_results = None
                st.session_state.global_result_label = ""
                st.rerun()

        display_cols = [c for c in [
            "name", "choir", "gender", "status",
            "institute", "course_name", "year_of_graduation"
        ] if c in results.columns]

        if results.empty:
            st.warning("No students match your search.")
        else:
            st.dataframe(results[display_cols], use_container_width=True, height=500)
            csv = results.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download results", csv,
                "search_results.csv", "text/csv",
                key="download_search_results"
            )

        st.stop()

    st.divider()


# ---------------- DASHBOARD ----------------
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = None

if menu == "Dashboard":
    data = load_full_dataset()
    st.session_state.edited_df = data
    

    data = st.session_state.edited_df.copy()
    total = data["identification_no"].nunique()
    graduated = data[data["graduated"] == True]["identification_no"].nunique()
    not_graduated = total - graduated
    deceased = int((data["status"] == "deceased").sum()) if "status" in data else 0

    # ── METRIC CARDS WITH BUTTONS INSIDE ──
    st.markdown("""
    <style>
    .metric-card {
        background: #FFFFFF;
        border: 0.5px solid #E0E0D8;
        border-radius: 12px;
        padding: 16px 20px 10px;
        margin-bottom: 4px;
    }
    .metric-card.active {
        border: 1.5px solid #1D9E75;
        background: #E1F5EE;
    }
    .metric-card-label {
        font-size: 11px;
        font-weight: 500;
        color: #888780;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 4px;
        font-family: 'DM Sans', sans-serif;
    }
    .metric-card-value {
        font-size: 28px;
        font-weight: 500;
        color: #1a1a1a;
        font-family: 'DM Sans', sans-serif;
        margin-bottom: 10px;
    }
    .metric-card.active .metric-card-value {
        color: #0F6E56;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── METRIC CARDS WITH ICONS ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        active = "active" if st.session_state.dashboard_view == "all" else ""
        st.markdown(f"""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <div class="metric-card {active}">
            <div class="mc-icon teal"><i class="ti ti-users"></i></div>
            <div class="metric-card-label">Total students</div>
            <div class="metric-card-value">{total}</div>
            <div class="metric-card-hint">across all choirs</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View all", key="btn_all", use_container_width=True):
            st.session_state.dashboard_view = "all"

    with col2:
        active = "active" if st.session_state.dashboard_view == "graduated" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="mc-icon amber"><i class="ti ti-school"></i></div>
            <div class="metric-card-label">Graduated</div>
            <div class="metric-card-value">{graduated}</div>
            <div class="metric-card-hint">{round(graduated/total*100, 1) if total else 0}% rate</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View graduated", key="btn_grad", use_container_width=True):
            st.session_state.dashboard_view = "graduated"

    with col3:
        active = "active" if st.session_state.dashboard_view == "not_graduated" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="mc-icon blue"><i class="ti ti-clock-hour-4"></i></div>
            <div class="metric-card-label">Not graduated</div>
            <div class="metric-card-value">{not_graduated}</div>
            <div class="metric-card-hint">pending follow-up</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View pending", key="btn_not_grad", use_container_width=True):
            st.session_state.dashboard_view = "not_graduated"

    with col4:
        active = "active" if st.session_state.dashboard_view == "deceased" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="mc-icon red"><i class="ti ti-heart-broken"></i></div>
            <div class="metric-card-label">Deceased</div>
            <div class="metric-card-value">{deceased}</div>
            <div class="metric-card-hint">in archive</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View deceased", key="btn_deceased", use_container_width=True):
            st.session_state.dashboard_view = "deceased"

    # ---------------- FILTER LOGIC ----------------
    filtered = None
    
    if st.session_state.dashboard_view == "all":
        filtered = data[[
            'identification_no',
            "name",
            "choir",
            "gender",
            "status"
        ]].sort_values(
            "choir",
            key=lambda col: col.map(natural_sort_key),
            ignore_index=True
        )
    # right after st.data_editor(filtered, ...)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download",
            csv,
            "students.csv",
            "text/csv",
            key=f"download_{st.session_state.dashboard_view}"
        )
    elif st.session_state.dashboard_view == "graduated":
        filtered = data[data["graduated"] == True][[
            "name",
            "choir",
            "gender",
            "status",
            "institute",
            "course_name",
            "year_of_graduation"
        ]]
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download",
            csv,
            "students.csv",
            "text/csv",
            key=f"download_{st.session_state.dashboard_view}"
        )
    elif st.session_state.dashboard_view == "not_graduated":
        filtered = data[data["graduated"] == False].copy()
        # remove ID columns
        filtered = filtered.drop(columns=["identification_no", "id_grad"], errors="ignore")
        display_cols = [
            "name",
            "choir",
            "gender",
            "status",
            
        ]
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download",
            csv,
            "students.csv",
            "text/csv",
            key=f"download_{st.session_state.dashboard_view}"
        )
        # keep only existing ones
        display_cols = [c for c in display_cols if c in filtered.columns]

        filtered = filtered[display_cols]
        filtered["mark_graduated"] = False
        edited = st.data_editor(filtered, use_container_width=True)
        
        for idx, row in edited.iterrows():
            if row.get("mark_graduated") == True:

                st.warning(f"Enter graduation details for {row['name']}")

                with st.form(f"grad_form_{idx}"):

                    institute = st.text_input("Institute", key=f"inst_{idx}")
                    course = st.text_input("Course", key=f"course_{idx}")
                    year = st.number_input("Year", min_value=2000, max_value=2100, key=f"year_{idx}")

                    submit = st.form_submit_button("Save Graduation")

                    if submit:
                        if not is_admin():
                           st.error("You don't have permission to save changes.")
                        elif not institute or not course or not year:
                            st.error("All fields required")
                        else:
                            conn = connect_db()
                            conn.execute("""
                                INSERT INTO graduation_data 
                                (identification_no, institute, course_name, year_of_graduation)
                                VALUES (?, ?, ?, ?)
                            """, (
                                data.loc[idx, "identification_no"],
                                institute,
                                course,
                                year
                            ))
                            conn.commit()
                            conn.close()

                            st.success("Graduation saved")
                            st.rerun()

    elif st.session_state.dashboard_view == "deceased":
        filtered = data[data["status"] == "deceased"].copy()
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download",
            csv,
            "students.csv",
            "text/csv",
            key=f"download_{st.session_state.dashboard_view}"
        )
    # keep only required columns
        display_cols = ["name", "choir", "gender", "comment"]

        for col in display_cols:
            if col not in filtered.columns:
                filtered[col] = ""

        filtered = filtered[display_cols]
    
        edited_deceased = st.data_editor(
            filtered,
            use_container_width=True,
            key="deceased_editor",
            disabled=not is_admin(),
            column_config={
                "comment": st.column_config.TextColumn("Comment")
            }
        )

        # persist changes back to session state
        for idx, row in edited_deceased.iterrows():
            if "comment" in row.index:
                st.session_state.edited_df.loc[idx, "comment"] = row["comment"]
    # ---------------- ONLY SHOW TABLE IF EXISTS ----------------
    if filtered is not None and st.session_state.dashboard_view != "not_graduated":
     if filtered is not None and st.session_state.dashboard_view != "deceased":
        display_df = filtered.drop(columns=["identification_no"], errors="ignore")
    
        edited_filtered = st.data_editor(
            filtered,
            use_container_width=True,
            key=f"editor_{st.session_state.dashboard_view}",  # UNIQUE KEY FIX
            disabled=not is_admin(),
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["alive", "deceased"]
                )
            }
        )

        # sync edits back
        # Fix NaN in graduated column BEFORE saving
        for idx in edited_filtered.index:
            for col in edited_filtered.columns:
                st.session_state.edited_df.loc[idx, col] = edited_filtered.loc[idx, col]

    # ---------------- SAVE ----------------
    
    if is_admin() and st.button(" Save Changes"):

        conn = connect_db()

        for _, row in st.session_state.edited_df.iterrows():

            conn.execute("""
                UPDATE choir_data
                SET status = ?, comment = ?
                WHERE identification_no = ?
            """, (
                row["status"],
                row.get("comment", ""),
                row["identification_no"]
            ))

        conn.commit()
        conn.close()

        st.session_state.edited_df = load_full_dataset()

        st.session_state.dashboard_view = None

        st.success("Saved successfully")
        st.rerun()
    st.divider()  # clean separator before page content when not searching
    # ── CHART + BY CHOIR ROW ──
    chart_col, choir_col = st.columns([2, 1])

    with chart_col:
        st.markdown("**Graduation trend**")

        trend = data[data["graduated"] == True].copy()
        trend = trend.dropna(subset=["year_of_graduation"])

        if not trend.empty:
            trend_grouped = (
                trend.groupby("year_of_graduation")
                .size()
                .reset_index(name="Graduates")
                .sort_values("year_of_graduation")
                .rename(columns={"year_of_graduation": "Year"})
            )
            trend_grouped["Year"] = trend_grouped["Year"].astype(int).astype(str)
            max_year = trend_grouped["Year"].max()

            # ── GRADUATION TREND CHART ── (replace the color encoding block)

        import altair as alt

        trend = data[data["graduated"] == True].copy()
        trend = trend.dropna(subset=["year_of_graduation"])

        if not trend.empty:
            trend_grouped = (
                trend.groupby("year_of_graduation")
                .size()
                .reset_index(name="Graduates")
                .sort_values("year_of_graduation")
                .rename(columns={"year_of_graduation": "Year"})
            )
            trend_grouped["Year"] = trend_grouped["Year"].astype(int).astype(str)
            max_year = trend_grouped["Year"].max()
            second_year = sorted(trend_grouped["Year"].tolist())[-2] if len(trend_grouped) >= 2 else max_year
            third_year  = sorted(trend_grouped["Year"].tolist())[-3] if len(trend_grouped) >= 3 else max_year

            # Add a colour category column — no nested conditions needed
            def bar_color_cat(year):
                if year == max_year:
                    return "latest"
                elif year in (second_year, third_year):
                    return "recent"
                else:
                    return "past"

            trend_grouped["ColorCat"] = trend_grouped["Year"].apply(bar_color_cat)

            color_scale = alt.Scale(
                domain=["latest", "recent", "past"],
                range=["#E8A020", "#1D9E75", "rgba(29,158,117,0.35)"]
            )

            chart = alt.Chart(trend_grouped).mark_bar(
                cornerRadiusTopLeft=4,
                cornerRadiusTopRight=4,
            ).encode(
                x=alt.X("Year:N", axis=alt.Axis(
                    labelColor="#B0A48E",
                    tickColor="#E0D8CC",
                    domainColor="#E0D8CC",
                    labelFontSize=11,
                    title=None
                )),
                y=alt.Y("Graduates:Q", axis=alt.Axis(
                    labelColor="#B0A48E",
                    gridColor="#EDE8DE",
                    domainOpacity=0,
                    tickOpacity=0,
                    labelFontSize=11,
                    title=None
                )),
                color=alt.Color(
                    "ColorCat:N",
                    scale=color_scale,
                    legend=None
                ),
                tooltip=["Year", "Graduates"]
            ).properties(
                height=180,
                background="transparent"
            ).configure_view(
                strokeOpacity=0
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No graduation data yet.")

    with choir_col:
        st.markdown("**By choir**")

        choir_stats = data.groupby("choir").agg(
            total=("identification_no", "count"),
            graduated=("graduated", "sum")
        ).reset_index()
        choir_stats["pct"] = (
            choir_stats["graduated"] / choir_stats["total"] * 100
        ).round(1)
        choir_stats = choir_stats.sort_values("pct", ascending=False).head(6)

        for _, row in choir_stats.iterrows():
            pct = row["pct"]
            bar_color = "#5DCAA5" if pct >= 60 else "#B4B2A9"
            num_color = "#0F6E56" if pct >= 60 else "#888780"
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:12px; font-weight:500; color:#1a1a1a;">{row['choir']}</span>
                    <span style="font-size:11px; color:{num_color}; font-weight:500;">
                        {int(row['graduated'])}/{int(row['total'])} · {pct}%
                    </span>
                </div>
                <div style="height:6px; background:#F1EFE8; border-radius:3px; overflow:hidden;">
                    <div style="height:100%; width:{pct}%; background:{bar_color}; border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── RECENT GRADUATES TABLE ──
    st.markdown("**Recent graduates**")

    recent = data[data["graduated"] == True].copy()
    required_cols = ["name", "choir", "institute", "course_name", "year_of_graduation"]
    for col in required_cols:
        if col not in recent.columns:
            recent[col] = None

    recent_display = (
        recent[required_cols]
        .sort_values("year_of_graduation", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    def initials(name):
        parts = str(name).split()
        return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else str(name)[:2].upper()

    if recent_display.empty:
        st.info("No graduates yet.")
    else:
        rows_html = ""
        for _, row in recent_display.iterrows():
            ini = initials(row["name"])
            year = int(row["year_of_graduation"]) if pd.notna(row["year_of_graduation"]) else "—"
            institute = row["institute"] if pd.notna(row["institute"]) else "—"
            course = row["course_name"] if pd.notna(row["course_name"]) else "—"
            rows_html += f"""
            <tr>
                <td>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:26px; height:26px; border-radius:50%; background:#E1F5EE;
                                    color:#0F6E56; font-size:10px; font-weight:500;
                                    display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                            {ini}
                        </div>
                        {row['name']}
                    </div>
                </td>
                <td>{row['choir']}</td>
                <td>{institute}</td>
                <td>{course}</td>
                <td><span style="background:#F1EFE8; color:#5F5E5A; font-size:11px;
                                padding:2px 8px; border-radius:6px; font-weight:500;">{year}</span></td>
                <td><span style="background:#E1F5EE; color:#0F6E56; font-size:10px;
                                font-weight:500; padding:2px 8px; border-radius:20px;">Graduated</span></td>
            </tr>
            """

        st.markdown(f"""
            <style>
            .grad-table {{ width:100%; border-collapse:collapse; }}
            .grad-table th {{
                text-align:left; font-size:10px; font-weight:500; color:#B4B2A9;
                text-transform:uppercase; letter-spacing:0.06em; padding:0 10px 10px;
                border-bottom: 0.5px solid #E0E0D8;
            }}
            .grad-table td {{
                font-size:12px; color:#1a1a1a;
                padding:9px 10px; border-bottom:0.5px solid #F1EFE8;
                vertical-align:middle;
            }}
            .grad-table tr:last-child td {{ border-bottom:none; }}
            .grad-table tr:hover td {{ background:#F7F8F6; }}
            </style>
            <table class="grad-table">
                <thead>
                    <tr>
                        <th>Name</th><th>Choir</th><th>Institute</th>
                        <th>Course</th><th>Year</th><th>Status</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        """, unsafe_allow_html=True)

        csv_recent = recent_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download recent graduates",
            csv_recent,
            "recent_graduates.csv",
            "text/csv",
            key="download_recent"
        )
                        
# ---------------- UPLOAD ----------------
elif menu == "Manage Data":
    if not is_admin():
        st.markdown("""
        <div style="background:#FAEEDA; border:0.5px solid #EF9F27; border-radius:10px;
                    padding:14px 16px; display:flex; align-items:center; gap:10px;
                    font-size:13px; color:#854F0B;">
            <i class="ti ti-lock" style="font-size:18px;"></i>
            You have view-only access. Contact an admin to make changes.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    st.title("**Manage Data**")
    st.caption("Upload, add and remove student records")
    st.markdown("---")

    # ── ROW 1: TEMPLATES + UPLOAD ──
    tmpl_col, upload_col = st.columns(2)

    with tmpl_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:16px 18px;">
            <div style="font-size:13px; font-weight:500; color:#1a1a1a;
                        display:flex; align-items:center; gap:7px; margin-bottom:14px;">
                <i class="ti ti-file-download" style="font-size:16px; color:#1D9E75;"></i>
                Download templates
            </div>
        </div>
        """, unsafe_allow_html=True)

        choir_template = pd.DataFrame(columns=["name", "choir", "gender", "status"])
        st.download_button(
            "Choir data template",
            choir_template.to_csv(index=False),
            "choir_template.csv",
            "text/csv",
            use_container_width=True,
            key="dl_choir_template"
        )

        grad_template = pd.DataFrame(columns=[
            "identification_no", "name", "institute",
            "course_name", "duration", "year_of_graduation"
        ])
        st.download_button(
            "Graduation data template",
            grad_template.to_csv(index=False),
            "graduation_template.csv",
            "text/csv",
            use_container_width=True,
            key="dl_grad_template"
        )

        st.markdown("""
        <div style="background:#E6F1FB; border-left:3px solid #378ADD;
                    border-radius:0 8px 8px 0; padding:8px 12px;
                    font-size:11px; color:#1A5FA8; margin-top:8px;">
            Download a template first, fill it in, then upload it.
            Column names must match exactly.
        </div>
        """, unsafe_allow_html=True)

    with upload_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:16px 18px 4px;">
            <div style="font-size:13px; font-weight:500; color:#1a1a1a;
                        display:flex; align-items:center; gap:7px; margin-bottom:14px;">
                <i class="ti ti-cloud-upload" style="font-size:16px; color:#1D9E75;"></i>
                Bulk upload
            </div>
        </div>
        """, unsafe_allow_html=True)

        choir_file = st.file_uploader(
            "Upload choir data",
            type=["csv", "xlsx"],
            key="choir_upload"
        )
        if choir_file:
            upload_choir_data(choir_file)
            st.success("Choir data uploaded successfully")
            st.session_state.edited_df = load_full_dataset()
            st.rerun()

        grad_file = st.file_uploader(
            "Upload graduation data",
            type=["csv", "xlsx"],
            key="grad_upload"
        )
        if grad_file:
            upload_graduation_data(grad_file)
            st.session_state.edited_df = load_full_dataset()
            st.success("Graduation data uploaded successfully")
            st.rerun()

    st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

    # ── ROW 2: ADD + DELETE ──
    add_col, del_col = st.columns(2)

    with add_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:16px 18px 4px;">
            <div style="font-size:13px; font-weight:500; color:#1a1a1a;
                        display:flex; align-items:center; gap:7px; margin-bottom:14px;">
                <i class="ti ti-user-plus" style="font-size:16px; color:#1D9E75;"></i>
                Add new student
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("add_student"):
            name = st.text_input("Full name", placeholder="e.g. Sarah Nalwoga")
            choir = st.text_input("Choir", placeholder="e.g. ACC 32")
            g_col, s_col = st.columns(2)
            with g_col:
                gender = st.selectbox("Gender", ["M", "F"])
            with s_col:
                status = st.selectbox("Status", ["alive", "deceased"])

            submit = st.form_submit_button(
                "Add student", use_container_width=True
            )

            if submit:
                if not name or not choir:
                    st.error("Name and choir are required")
                else:
                    from services import generate_id
                    student_id = generate_id()
                    conn = connect_db()
                    conn.execute("""
                        INSERT INTO choir_data
                        (identification_no, name, choir, gender, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (student_id, name, choir, gender, status))
                    conn.commit()
                    conn.close()
                    st.session_state.student_added = True
                    st.rerun()

    with del_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:16px 18px 4px;">
            <div style="font-size:13px; font-weight:500; color:#1a1a1a;
                        display:flex; align-items:center; gap:7px; margin-bottom:14px;">
                <i class="ti ti-user-minus" style="font-size:16px; color:#E24B4A;"></i>
                Remove student
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("delete_student"):
            name_to_delete = st.text_input(
                "Student name",
                placeholder="Enter exact name to remove..."
            )

            st.markdown("""
            <div style="background:#FAEEDA; border:0.5px solid #EF9F27; border-radius:8px;
                        padding:8px 12px; font-size:11px; color:#854F0B;
                        display:flex; align-items:center; gap:7px; margin:6px 0 10px;">
                <i class="ti ti-alert-triangle" style="font-size:14px; flex-shrink:0;"></i>
                This will permanently delete the student and all their graduation records.
            </div>
            """, unsafe_allow_html=True)

            confirm = st.checkbox(
                "I confirm I want to permanently remove this student"
            )

            delete_submit = st.form_submit_button(
                "Remove student", use_container_width=True
            )

            if delete_submit:
                if not name_to_delete:
                    st.error("Please enter a student name")
                elif not confirm:
                    st.error("Please check the confirmation box")
                else:
                    conn = connect_db()
                    matches = pd.read_sql(
                        "SELECT identification_no FROM choir_data WHERE name = ?",
                        conn,
                        params=(name_to_delete,)
                    )
                    if matches.empty:
                        st.error(f"No student found with name '{name_to_delete}'")
                        conn.close()
                    else:
                        ids = matches["identification_no"].tolist()
                        conn.executemany(
                            "DELETE FROM choir_data WHERE identification_no = ?",
                            [(i,) for i in ids]
                        )
                        conn.executemany(
                            "DELETE FROM graduation_data WHERE identification_no = ?",
                            [(i,) for i in ids]
                        )
                        conn.commit()
                        conn.close()
                        st.session_state.deleted_count = len(ids)
                        st.session_state.deleted_name = name_to_delete
                        st.rerun()

    # ── SUCCESS / DELETE TOASTS ──
    if st.session_state.get("deleted_count"):
        st.success(
            f"Removed {st.session_state.deleted_count} record(s) "
            f"for '{st.session_state.deleted_name}'"
        )
        st.toast("Student removed successfully", icon="⚠️")
        st.session_state.deleted_count = None
        st.session_state.deleted_name = None

    if st.session_state.get("student_added"):
        st.success("Student added successfully")
        st.toast("🎉 New student added!")
        st.session_state.student_added = False

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    data = st.session_state.edited_df.copy()

    st.title("**Analytics**")
    st.caption("Graduation insights across all choirs")
    st.markdown("---")

    # ── DERIVED STATS ──
    total = data["identification_no"].nunique()
    graduated = data[data["graduated"] == True]["identification_no"].nunique()
    deceased = int((data["status"] == "deceased").sum())
    grad_rate = round((graduated / total * 100), 1) if total > 0 else 0

    choir_stats = data.groupby("choir").agg(
        total=("identification_no", "count"),
        graduated=("graduated", "sum"),
        deceased=("status", lambda x: (x == "deceased").sum())
    ).reset_index()
    choir_stats["pending"] = choir_stats["total"] - choir_stats["graduated"] - choir_stats["deceased"]
    choir_stats["rate"] = (choir_stats["graduated"] / choir_stats["total"] * 100).round(1)
    choir_stats = choir_stats.sort_values("rate", ascending=False)

    top_choir = choir_stats.iloc[0]["choir"] if not choir_stats.empty else "—"
    top_rate = choir_stats.iloc[0]["rate"] if not choir_stats.empty else 0

    grad_by_year = (
        data[data["graduated"] == True]
        .groupby("year_of_graduation")
        .size()
        .reset_index(name="Graduates")
        .sort_values("year_of_graduation")
    )
    grad_by_year["Year"] = grad_by_year["year_of_graduation"].astype(int).astype(str)

    male = int((data["gender"] == "M").sum())
    female = int((data["gender"] == "F").sum())

    # ── STAT CARDS ──
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:14px 16px; display:flex; align-items:center; gap:12px;">
            <div style="width:36px; height:36px; border-radius:9px; background:#E1F5EE;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="ti ti-chart-pie" style="font-size:18px; color:#1D9E75;"></i>
            </div>
            <div>
                <div style="font-size:11px; color:#888780; margin-bottom:3px;">Graduation rate</div>
                <div style="font-size:22px; font-weight:500; color:#1a1a1a;">{grad_rate}%</div>
                <div style="font-size:11px; color:#1D9E75;">{graduated} of {total} students</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        total_safe = total if total > 0 else 1
        st.markdown(f"""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                    padding:14px 16px; display:flex; align-items:center; gap:12px;">
            <div style="width:36px; height:36px; border-radius:9px; background:#FAEEDA;
                        display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="ti ti-venus-mars" style="font-size:18px; color:#EF9F27;"></i>
            </div>
            <div>
                <div style="font-size:11px; color:#888780; margin-bottom:3px;">Gender split</div>
                <div style="font-size:22px; font-weight:500; color:#1a1a1a;">{male}M · {female}F</div>
                <div style="font-size:11px; color:#888780;">
                    {round(male/total_safe*100)}% male · {round(female/total_safe*100)}% female
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px;
                        padding:14px 16px; display:flex; align-items:center; gap:12px;">
                <div style="width:36px; height:36px; border-radius:9px; background:#E6F1FB;
                            display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                    <i class="ti ti-trophy" style="font-size:18px; color:#378ADD;"></i>
                </div>
                <div>
                    <div style="font-size:11px; color:#888780; margin-bottom:3px;">Top choir</div>
                    <div style="font-size:18px; font-weight:500; color:#1a1a1a;">{top_choir}</div>
                    <div style="font-size:11px; color:#888780;">{top_rate}% graduation rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)

    # ── CHARTS ROW ──
    chart_col, gender_col = st.columns([2, 1])

    with chart_col:
        st.markdown("Graduation rate by choir")
        import altair as alt

        choir_chart = alt.Chart(choir_stats).mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
        ).encode(
            x=alt.X("choir:N", sort="-y", axis=alt.Axis(
                labelColor="#B4B2A9", tickColor="#E0E0D8",
                domainColor="#E0E0D8", labelFontSize=11, title=None
            )),
            y=alt.Y("rate:Q", axis=alt.Axis(
                labelColor="#B4B2A9", gridColor="#F1EFE8",
                domainOpacity=0, tickOpacity=0,
                labelFontSize=11, title=None
            ), scale=alt.Scale(domain=[0, 100])),
            color=alt.condition(
                alt.datum.rate >= 60,
                alt.value("#1D9E75"),
                alt.value("#B4B2A9")
            ),
            tooltip=["choir", "rate", "graduated", "total"]
        ).properties(
            height=180, background="transparent"
        ).configure_view(strokeOpacity=0)

        st.altair_chart(choir_chart, use_container_width=True)

    with gender_col:
        st.markdown("Gender breakdown")

        total_safe = total if total > 0 else 1
        male_pct = round(male / total_safe * 100)
        female_pct = round(female / total_safe * 100)
        deceased_pct = round(deceased / total_safe * 100)

        for label, value, pct, color in [
            ("Male", male, male_pct, "#1D9E75"),
            ("Female", female, female_pct, "#9FE1CB"),
            ("Deceased", deceased, deceased_pct, "#E0E0D8"),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:12px; font-weight:500; color:#1a1a1a;">{label}</span>
                    <span style="font-size:11px; color:#888780;">{value} · {pct}%</span>
                </div>
                <div style="height:8px; background:#F1EFE8; border-radius:4px; overflow:hidden;">
                    <div style="height:100%; width:{pct}%; background:{color}; border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── YEARLY TREND ──
    st.markdown("Graduation trend by year")

    if not grad_by_year.empty:
        max_year = grad_by_year["Year"].max()
        year_chart = alt.Chart(grad_by_year).mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
        ).encode(
            x=alt.X("Year:N", axis=alt.Axis(
                labelColor="#B4B2A9", tickColor="#E0E0D8",
                domainColor="#E0E0D8", labelFontSize=11, title=None
            )),
            y=alt.Y("Graduates:Q", axis=alt.Axis(
                labelColor="#B4B2A9", gridColor="#F1EFE8",
                domainOpacity=0, tickOpacity=0,
                labelFontSize=11, title=None
            )),
            color=alt.condition(
                alt.datum.Year == max_year,
                alt.value("#1D9E75"),
                alt.value("#9FE1CB")
            ),
            tooltip=["Year", "Graduates"]
        ).properties(
            height=180, background="transparent"
        ).configure_view(strokeOpacity=0)

        st.altair_chart(year_chart, use_container_width=True)

    st.markdown("---")

        # ── CHOIR BREAKDOWN TABLE ──
    st.markdown("**Choir breakdown**")

    def rate_badge(rate):
        if rate >= 80:
            return '<span style="background:#E1F5EE; color:#0F6E56; font-size:10px; font-weight:500; padding:2px 8px; border-radius:20px;">Excellent</span>'
        elif rate >= 60:
            return '<span style="background:#E1F5EE; color:#1D9E75; font-size:10px; font-weight:500; padding:2px 8px; border-radius:20px;">Good</span>'
        elif rate >= 40:
            return '<span style="background:#FAEEDA; color:#854F0B; font-size:10px; font-weight:500; padding:2px 8px; border-radius:20px;">Average</span>'
        else:
            return '<span style="background:#F1EFE8; color:#5F5E5A; font-size:10px; font-weight:500; padding:2px 8px; border-radius:20px;">Needs attention</span>'

    rows_html = ""
    for _, row in choir_stats.iterrows():
        pct = row["rate"]
        bar_color = "#1D9E75" if pct >= 80 else "#5DCAA5" if pct >= 60 else "#B4B2A9"
        rows_html += f"""
        <tr>
            <td><strong>{row['choir']}</strong></td>
            <td>{int(row['total'])}</td>
            <td>{int(row['graduated'])}</td>
            <td>{int(row['pending'])}</td>
            <td>{int(row['deceased'])}</td>
            <td>
                <div style="display:flex; align-items:center; gap:6px;">
                    <div style="width:70px; height:6px; background:#F1EFE8; border-radius:3px; overflow:hidden;">
                        <div style="height:100%; width:{pct}%; background:{bar_color}; border-radius:3px;"></div>
                    </div>
                    <span style="font-size:12px; color:#1a1a1a; font-weight:500;">{pct}%</span>
                </div>
            </td>
            <td>{rate_badge(pct)}</td>
        </tr>
        """

    st.markdown(f"""
        <style>
        .analytics-table {{ width:100%; border-collapse:collapse; }}
        .analytics-table th {{
            text-align:left; font-size:10px; font-weight:500; color:#B4B2A9;
            text-transform:uppercase; letter-spacing:0.06em;
            padding:0 10px 10px; border-bottom:0.5px solid #E0E0D8;
        }}
        .analytics-table td {{
            font-size:12px; color:#1a1a1a;
            padding:9px 10px; border-bottom:0.5px solid #F1EFE8;
            vertical-align:middle;
        }}
        .analytics-table tr:last-child td {{ border-bottom:none; }}
        .analytics-table tr:hover td {{ background:#F7F8F6; }}
        </style>
        <table class="analytics-table">
            <thead>
                <tr>
                    <th>Choir</th>
                    <th>Total</th>
                    <th>Graduated</th>
                    <th>Pending</th>
                    <th>Deceased</th>
                    <th>Rate</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
    csv_analytics = choir_stats.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download analytics",
        csv_analytics,
        "choir_analytics.csv",
        "text/csv",
        key="download_analytics"
    )
#-------user management----------------
elif menu == "User Management":
    render_user_management()
elif menu == "Settings":
    render_settings()
