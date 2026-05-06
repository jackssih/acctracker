import streamlit as st
from database import create_tables
from auth import login
from services import upload_choir_data, upload_graduation_data
import pandas as pd
from choir_logic import load_full_dataset
from streamlit_option_menu import option_menu
from database import connect_db

def refresh_data():
    st.session_state.edited_df = load_full_dataset()
create_tables()

st.set_page_config(page_title="Choir Graduation Tracker", layout="wide")
from choir_theme import inject_theme
inject_theme()
# LOGIN
if not login():
    st.stop()

# SIDEBAR NAVIGATION
with st.sidebar:
    # ── BRAND ──
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
    .brand-block {
        display: flex; align-items: center; gap: 10px;
        padding: 18px 16px 14px;
        border-bottom: 0.5px solid #E0E0D8;
        margin-bottom: 8px;
    }
    .brand-tile {
        width: 34px; height: 34px;
        background: #E1F5EE; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
    }
    .brand-tile i { font-size: 18px; color: #1D9E75; }
    .brand-name { font-size: 13px; font-weight: 500; color: #1a1a1a; line-height: 1.3; }
    .brand-sub  { font-size: 10px; color: #888780; }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
    <div class="brand-block">
        <div class="brand-tile"><i class="ti ti-music"></i></div>
        <div>
            <div class="brand-name">Choir Tracker</div>
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
    ],
    icons=[
        "speedometer2",        # Dashboard
        "cloud-upload",        # Manage Data  
        "bar-chart-line",      # Analytics
        "people",              # User Management
    ],
    default_index=0,
    styles={
        "container": {
            "padding": "0 10px",
            "background-color": "transparent",
        },
        "menu-title": {
            "font-size": "10px",
            "font-weight": "600",
            "color": "#5F5E5A",        # ← darker so it's visible
            "text-transform": "uppercase",
            "letter-spacing": "0.08em",
            "padding": "0 6px",
            "margin-bottom": "4px",
        },
        "icon": {
            "font-size": "16px",
            "color": "#888780",
        },
        "nav-link": {
            "font-size": "13px",
            "color": "#5F5E5A",
            "border-radius": "8px",
            "padding": "8px 10px",
            "margin-bottom": "1px",
        },
        "nav-link-selected": {
            "background-color": "#E1F5EE",
            "color": "#0F6E56",
            "font-weight": "500",
        },
        "icon-selected": {
            "color": "#1D9E75",
        },
    }
)
    # ── DIVIDER + SETTINGS ──
    st.markdown("""
    <hr style="border:none; border-top: 0.5px solid #E0E0D8; margin: 8px 10px;">
    <div style="padding: 0 10px;">
      <div style="font-size:10px; font-weight:500; color:#B4B2A9; text-transform:uppercase;
                  letter-spacing:0.08em; padding: 0 6px; margin-bottom:4px;">System</div>
      <div style="display:flex; align-items:center; gap:10px; padding:8px 10px;
                  border-radius:8px; font-size:13px; color:#5F5E5A; cursor:pointer;">
        <i class="ti ti-settings" style="font-size:17px; color:#B4B2A9;"></i> Settings
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PROFILE + LOGOUT AT BOTTOM ──
    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown("""
    <hr style="border:none; border-top: 0.5px solid #E0E0D8; margin: 8px 10px 0;">
    """, unsafe_allow_html=True)

    role = st.session_state.get('role', 'Admin')
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px;
                padding: 12px 10px; border-radius:8px; cursor:pointer;">
        <div style="width:30px; height:30px; border-radius:50%; background:#E1F5EE;
                    color:#0F6E56; font-size:11px; font-weight:500;
                    display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            JK
        </div>
        <div style="flex:1;">
            <div style="font-size:12px; font-weight:500; color:#1a1a1a;">Jackson K.</div>
            <div style="font-size:10px; color:#888780;">{role}</div>
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
data = load_full_dataset()


search_col1, search_col2, search_col3, search_col4, search_col5 = st.columns([3, 0.5, 1, 1, 1])

with search_col1:
    search_query = st.text_input(
        "Search by name or ID",
        placeholder="Search...",
        key="global_search",
        label_visibility="collapsed"
    )

with search_col2:
    search_clicked = st.button("⌕", key="global_search_btn", use_container_width=True)

with search_col3:
    choir_filter = st.selectbox(
        "Choir",
        ["All Choirs"] + sorted(data["choir"].dropna().unique().tolist()),
        key="global_choir_filter"
    )

with search_col4:
    gender_filter = st.selectbox(
        "Gender",
        ["All", "M", "F"],
        key="global_gender_filter"
    )

with search_col5:
    status_filter = st.selectbox(
        "Status",
        ["All", "Graduated", "Not Graduated", "Deceased"],
        key="global_status_filter"
    )

# ---------------- SEARCH ACTIVE FLAG ----------------
is_searching = search_clicked and (
    search_query or
    choir_filter != "All Choirs" or
    gender_filter != "All" or
    status_filter != "All"
)

if is_searching:
    results = data.copy()

    if search_query:
        results = results[
            results["name"].fillna("").str.contains(search_query, case=False) |
            results["identification_no"].astype(str).str.contains(search_query, case=False)
        ]

    if choir_filter != "All Choirs":
        results = results[results["choir"] == choir_filter]

    if gender_filter != "All":
        results = results[results["gender"] == gender_filter]

    if status_filter == "Graduated":
        results = results[results["graduated"] == True]
    elif status_filter == "Not Graduated":
        results = results[results["graduated"] == False]
    elif status_filter == "Deceased":
        results = results[results["status"] == "deceased"]

    # ---------------- FULL PAGE TAKEOVER ----------------
    st.markdown("---")
    st.markdown(f"### 📋 Results &nbsp;&nbsp; <span style='font-size:0.9rem; color:gray;'>{len(results)} student(s) found</span>", unsafe_allow_html=True)

    display_cols = [c for c in [
        "name", "choir", "gender", "status",
        "institute", "course_name", "year_of_graduation"
    ] if c in results.columns]

    if results.empty:
        st.warning("No students match your search.")
    else:
        st.dataframe(
            results[display_cols],
            use_container_width=True,
            height=500  # tall table to fill the page
        )

        csv = results.to_csv(index=False).encode("utf-8")
        

    # ---- STOP rendering the rest of the page ----
    st.stop()

st.divider()  # clean separator before page content when not searching


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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        active = "active" if st.session_state.dashboard_view == "all" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="metric-card-label">Total students</div>
            <div class="metric-card-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View all", key="btn_all", use_container_width=True):
            st.session_state.dashboard_view = "all"

    with col2:
        active = "active" if st.session_state.dashboard_view == "graduated" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="metric-card-label">Graduated</div>
            <div class="metric-card-value">{graduated}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View graduated", key="btn_grad", use_container_width=True):
            st.session_state.dashboard_view = "graduated"

    with col3:
        active = "active" if st.session_state.dashboard_view == "not_graduated" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="metric-card-label">Not graduated</div>
            <div class="metric-card-value">{not_graduated}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View pending", key="btn_not_grad", use_container_width=True):
            st.session_state.dashboard_view = "not_graduated"

    with col4:
        active = "active" if st.session_state.dashboard_view == "deceased" else ""
        st.markdown(f"""
        <div class="metric-card {active}">
            <div class="metric-card-label">Deceased</div>
            <div class="metric-card-value">{deceased}</div>
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
        ]]

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
                        if not institute or not course or not year:
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
            column_config={
                "comment": st.column_config.TextColumn("Comment")
            }
        )

        # persist changes back to session state
        for idx, row in edited_deceased.iterrows():
            st.session_state.edited_df.loc[idx, "comment"] = row["comment"]
    # ---------------- ONLY SHOW TABLE IF EXISTS ----------------
    if filtered is not None and st.session_state.dashboard_view != "not_graduated":
     if filtered is not None and st.session_state.dashboard_view != "deceased":
        display_df = filtered.drop(columns=["identification_no"], errors="ignore")
        edited_filtered = st.data_editor(
            filtered,
            use_container_width=True,
            key=f"editor_{st.session_state.dashboard_view}",  # UNIQUE KEY FIX
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
    if st.button(" Save Changes"):

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
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8; border-radius:12px; padding:16px 18px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span style="font-size:13px; font-weight:500; color:#1a1a1a;">📊 Graduation trend</span>
                <span style="font-size:11px; color:#888780; margin-left:auto;">by year</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        trend = data[data["graduated"] == True].copy()
        trend_grouped = (
            trend.groupby("year_of_graduation")
            .size()
            .reset_index(name="Graduates")
            .sort_values("year_of_graduation")
            .rename(columns={"year_of_graduation": "Year"})
        )
        trend_grouped["Year"] = trend_grouped["Year"].astype(int).astype(str)

        import altair as alt
        chart = alt.Chart(trend_grouped).mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
            color="#9FE1CB"
        ).encode(
            x=alt.X("Year:N", axis=alt.Axis(
                labelColor="#B4B2A9",
                tickColor="#E0E0D8",
                domainColor="#E0E0D8",
                labelFontSize=11,
                title=None
            )),
            y=alt.Y("Graduates:Q", axis=alt.Axis(
                labelColor="#B4B2A9",
                gridColor="#F1EFE8",
                domainOpacity=0,
                tickOpacity=0,
                labelFontSize=11,
                title=None
            )),
            tooltip=["Year", "Graduates"],
            color=alt.condition(
                alt.datum.Year == str(int(trend_grouped["Year"].max())),
                alt.value("#1D9E75"),
                alt.value("#9FE1CB")
            )
        ).properties(
            height=180,
            background="transparent"
        ).configure_view(
            strokeOpacity=0
        )

        st.altair_chart(chart, use_container_width=True)

    with choir_col:
        st.markdown("""
        <div style="background:#FFFFFF; border:0.5px solid #E0E0D8;
                    border-radius:12px; padding:16px 18px; height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="font-size:13px; font-weight:500; color:#1a1a1a;">🎵 By choir</span>
            </div>
        """, unsafe_allow_html=True)

        choir_stats = data.groupby("choir").agg(
            total=("identification_no", "count"),
            graduated=("graduated", "sum")
        ).reset_index()
        choir_stats["pct"] = (choir_stats["graduated"] / choir_stats["total"] * 100).round(1)
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

        st.markdown("</div>", unsafe_allow_html=True)

    # ── RECENT GRADUATES TABLE ──
    st.markdown("""
    <div style="background:#FFFFFF; border:0.5px solid #E0E0D8;
                border-radius:12px; padding:16px 18px; margin-top:10px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
            <span style="font-size:13px; font-weight:500; color:#1a1a1a;">⭐ Recent graduates</span>
            <span style="font-size:11px; color:#888780; margin-left:auto;">last 10</span>
        </div>
    """, unsafe_allow_html=True)

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

    # initials helper
    def initials(name):
        parts = str(name).split()
        return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else str(name)[:2].upper()

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
                    <th>Name</th>
                    <th>Choir</th>
                    <th>Institute</th>
                    <th>Course</th>
                    <th>Year</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)                       
# ---------------- UPLOAD ----------------
if st.session_state.get("deleted_count"):

    st.success(
        f"Deleted {st.session_state.deleted_count} record(s) "
        f"for '{st.session_state.deleted_name}' "
    )

    st.toast(" Student(s) removed successfully", icon="⚠️")

    # clear after showing once
    st.session_state.deleted_count = None
    st.session_state.deleted_name = None
if st.session_state.get("student_added"):
    st.success("Student has been added successfully ")
    st.info("Check the Dashboard for updated figures")
    st.toast("🎉 New student added successfully!")

    # clear after showing once
    st.session_state.student_added = False
elif menu == "Manage Data":
    col_left, col_main = st.columns([1, 3])
    with col_left:
        st.subheader("Download Templates")

        choir_template = pd.DataFrame(columns=[
            "name",
            "choir",
            "gender",
            "status"
        ])

        st.download_button(
            "Choir Template",
            choir_template.to_csv(index=False),
            "choir_template.csv",
            "text/csv"
        )
        grad_template = pd.DataFrame(columns=[
            "name",
            "institute",
            "course_name",
            'duration',
            "year_of_graduation"
        ])

        st.download_button(
            "Graduation Template",
            grad_template.to_csv(index=False),
            "graduation_template.csv",
            "text/csv"
        )
        st.subheader("Bulk Upload")

        choir_file = st.file_uploader("Upload Choir Data", type=["csv", "xlsx"])
        grad_file = st.file_uploader("Upload Graduation Data", type=["csv", "xlsx"])

        if choir_file:
            upload_choir_data(choir_file)
            st.success("Choir uploaded")
            st.rerun()

        if grad_file:
            upload_graduation_data(grad_file)
            st.session_state.edited_df = load_full_dataset()

            st.success("Graduation data uploaded")
            st.info("Dashboard updated")

            st.rerun()
            
    with col_main:
        st.subheader("Add New Student")

        with st.form("add_student"):

            name = st.text_input("Full Name")
            choir = st.text_input("Choir")
            gender = st.selectbox("Gender", ["M", "F"])
            status = st.selectbox("Status", ["alive", "deceased"])
         
            submit = st.form_submit_button("Add Student")
        
            if submit:

                from services import generate_id
                student_id = generate_id()

                conn = connect_db()
                conn.execute("""
                    INSERT INTO choir_data 
                    (identification_no, name, choir, gender, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    student_id,
                    name,
                    choir,
                    gender,
                    status
                ))
                conn.commit()
                conn.close()

                # ✅ STORE MESSAGE
                st.session_state.student_added = True

                st.rerun()
                
        st.subheader(" Delete Student ")

        name_to_delete = st.text_input("Enter Student Name")

        confirm = st.checkbox("Confirm delete")

        if st.button("Delete Student") and confirm:

            conn = connect_db()

            matches = pd.read_sql(
                "SELECT identification_no FROM choir_data WHERE name = ?",
                conn,
                params=(name_to_delete,)
            )

            if matches.empty:
                st.error("No student found with that name")
                conn.close()

            else:
                ids = matches["identification_no"].tolist()

                # delete from choir
                conn.executemany(
                    "DELETE FROM choir_data WHERE identification_no = ?",
                    [(i,) for i in ids]
                )

                # delete from graduation
                conn.executemany(
                    "DELETE FROM graduation_data WHERE identification_no = ?",
                    [(i,) for i in ids]
                )

                conn.commit()
                conn.close()

                # ✅ STORE MESSAGE BEFORE RERUN
                st.session_state.deleted_count = len(ids)
                st.session_state.deleted_name = name_to_delete

                st.rerun()

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.title("Choir Analytics")

    data = st.session_state.edited_df.copy()

    choir_stats = data.groupby("choir").agg({
        "graduated": ["count", "sum"]
    })

    st.dataframe(choir_stats)
