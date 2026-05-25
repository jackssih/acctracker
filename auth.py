import streamlit as st
import bcrypt
from database import connect_db
import base64
import tempfile
import os
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


def encode_image(path: Path) -> str | None:
    if not path.exists():
        return None
    suffix = path.suffix.lower()
    mime = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png",  ".webp": "image/webp",
    }.get(suffix, "image/jpeg")
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def login():
    if st.session_state.get("auth"):
        return True

    # ── CHECK QUERY PARAMS ──
    params = st.query_params
    if "login_user" in params and "login_pass" in params:
        username_input = params["login_user"]
        password_input = params["login_pass"]
        st.query_params.clear()  # wipe credentials from URL immediately

        user = get_user(username_input)
        if user and verify_password(password_input, user["password_hash"]):
            st.session_state.auth = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            st.session_state.login_error = False
            st.rerun()
        else:
            st.session_state.login_error = True
            st.rerun()

    # ── SLIDESHOW IMAGE FILES ──
    slideshow_files = [
        Path("slide1.jpg"),
        Path("slide2.jpg"),
        Path("slide3.jpg"),
        Path("slide4.jpg"),
        Path("slide5.jpg"),
    ]

    slide_uris = [u for f in slideshow_files if (u := encode_image(f))]
    n = len(slide_uris)

    # ── BUILD SLIDESHOW CSS ──
    HOLD   = 3
    FADE   = 1
    PERIOD = HOLD + FADE
    TOTAL  = PERIOD * n if n > 0 else 1

    slides_css     = ""
    slideshow_html = ""

    if n > 0:
        css_parts = []
        div_parts = []

        for i, uri in enumerate(slide_uris):
            start      = (i * PERIOD) / TOTAL * 100
            peak_start = (i * PERIOD + FADE) / TOTAL * 100
            peak_end   = ((i + 1) * PERIOD - FADE) / TOTAL * 100
            end        = min(((i + 1) * PERIOD) / TOTAL * 100, 100)

            kf = f"""@keyframes kf{i} {{
  0%            {{ opacity: 0; }}
  {start:.3f}%  {{ opacity: 0; }}
  {peak_start:.3f}% {{ opacity: 1; }}
  {peak_end:.3f}%   {{ opacity: 1; }}
  {end:.3f}%    {{ opacity: 0; }}
  100%          {{ opacity: 0; }}
}}"""
            css_parts.append(kf)
            css_parts.append(f"""
.slide-bg:nth-child({i + 1}) {{
  background-image: url('{uri}');
  animation: kf{i} {TOTAL}s linear 0s infinite;
}}""")
            div_parts.append('<div class="slide-bg"></div>')

        slides_css     = "\n".join(css_parts)
        slideshow_html = "\n    ".join(div_parts)

    # ── HIDE STREAMLIT CHROME ──
    st.markdown("""
    <style>
    #MainMenu, footer, header,
    [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"]
    { display: none !important; }
    html, body { margin: 0 !important; padding: 0 !important; }
    .stApp { background: #0d1f18 !important; margin: 0 !important; padding: 0 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
    section[data-testid="stMain"] { padding: 0 !important; }
    section[data-testid="stMain"] > div { padding: 0 !important; }
    iframe {
        display: block !important; position: fixed !important;
        top: 0 !important; left: 0 !important;
        width: 100vw !important; height: 100vh !important;
        border: none !important; z-index: 9999 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    show_error = st.session_state.get("login_error", False)
    error_display = "flex" if show_error else "none"

    dot_html = "".join(
        f'<div class="slide-dot{"  active" if i == 0 else ""}" data-i="{i}"></div>'
        for i in range(n)
    )

    # ── BUILD PARENT URL FOR JS (so the iframe can redirect the parent) ──
    # We pass the current app URL into the HTML so JS can append query params
    # without needing window.parent access (which st.iframe blocks too).
    # We use a placeholder that JS replaces at runtime using document.referrer
    # or a fallback to window.parent.location — st.iframe allows same-origin nav.

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --green-bright:  #3DFF9A;
    --green-mid:     #1DB86A;
    --green-deep:    #0A5C35;
    --orange-bright: #FF8C42;
    --orange-mid:    #E06820;
    --black-panel:   rgba(8, 18, 12, 0.38);
    --border-green:  rgba(61, 255, 154, 0.38);
    --border-orange: rgba(255, 140, 66, 0.55);
    --text-muted:    rgba(200, 255, 230, 0.65);
  }}

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 100%; height: 100%; font-family: 'DM Sans', sans-serif; }}

  .bg-stage {{ position: fixed; inset: 0; z-index: 0; background: #0d1f18; }}
  .slide-bg {{
    position: absolute; inset: 0;
    background-size: cover; background-position: center; opacity: 0;
  }}

  {slides_css}

  .bg-overlay {{
    position: fixed; inset: 0; z-index: 1;
    background: linear-gradient(135deg, rgba(8,18,12,0.65) 0%, rgba(10,30,18,0.48) 50%, rgba(15,12,8,0.65) 100%);
  }}

  .slide-dots {{
    position: fixed; bottom: 20px; left: 50%;
    transform: translateX(-50%); z-index: 10; display: flex; gap: 8px;
  }}
  .slide-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: rgba(255,255,255,0.3); transition: background 0.4s, transform 0.4s;
  }}
  .slide-dot.active {{
    background: var(--orange-bright); transform: scale(1.5);
    box-shadow: 0 0 8px rgba(255,140,66,0.8);
  }}

  .page {{
    position: relative; z-index: 2; min-height: 100vh;
    display: flex; align-items: center; justify-content: center; padding: 2rem;
  }}

  .glass-panel {{
    width: 100%; max-width: 420px;
    background: var(--black-panel);
    backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px);
    border-radius: 22px; overflow: hidden;
    border-top: 2px solid var(--orange-bright);
    border-left: 1px solid var(--border-green);
    border-right: 1px solid rgba(255,255,255,0.08);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    box-shadow:
      0 0 0 1px rgba(255,140,66,0.12), 0 12px 60px rgba(0,0,0,0.55),
      inset 0 1px 0 rgba(255,140,66,0.18), inset 1px 0 0 rgba(61,255,154,0.12);
  }}

  .slide-track {{
    display: flex; width: 200%;
    transition: transform 0.58s cubic-bezier(0.77, 0, 0.175, 1);
  }}
  .slide-track.show-form {{ transform: translateX(-50%); }}
  .slide-panel {{ width: 50%; flex-shrink: 0; padding: 42px 36px 38px; }}

  .accent-bar {{ display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }}
  .accent-dot {{
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--orange-bright); box-shadow: 0 0 10px rgba(255,140,66,0.7); flex-shrink: 0;
  }}
  .accent-line {{
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--orange-bright), transparent); opacity: 0.55;
  }}

  .system-name {{
    font-size: 23px; font-weight: 700; color: var(--green-bright);
    line-height: 1.38; margin-bottom: 5px;
    text-shadow: 0 0 24px rgba(61,255,154,0.38), 0 2px 8px rgba(0,0,0,0.7);
  }}
  .system-sub {{
    font-size: 10.5px; font-weight: 600; color: var(--orange-bright);
    letter-spacing: 0.13em; text-transform: uppercase; margin-bottom: 26px;
    text-shadow: 0 0 12px rgba(255,140,66,0.5);
  }}
  .divider {{
    border: none; height: 1px;
    background: linear-gradient(90deg, var(--border-orange), transparent 80%); margin-bottom: 22px;
  }}
  .welcome-body {{
    font-size: 13.5px; color: var(--text-muted); line-height: 1.78; margin-bottom: 32px;
  }}
  .welcome-body strong {{ color: #ffffff; font-weight: 600; }}

  .back-btn {{
    background: none; border: none; color: rgba(255,140,66,0.65);
    font-size: 12px; font-family: 'DM Sans', sans-serif;
    cursor: pointer; padding: 0; margin-bottom: 22px;
    display: flex; align-items: center; gap: 5px;
    letter-spacing: 0.04em; transition: color 0.2s;
  }}
  .back-btn:hover {{ color: var(--orange-bright); }}

  .form-heading {{
    font-size: 21px; font-weight: 700; color: var(--green-bright); margin-bottom: 4px;
    text-shadow: 0 0 20px rgba(61,255,154,0.32);
  }}
  .form-desc {{ font-size: 13px; color: var(--text-muted); margin-bottom: 26px; }}

  .field {{ margin-bottom: 18px; }}
  .field label {{
    display: block; font-size: 10.5px; font-weight: 700;
    color: var(--orange-bright); letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 7px;
    text-shadow: 0 0 10px rgba(255,140,66,0.4);
  }}
  .field input {{
    width: 100%; padding: 11px 14px;
    border: 1px solid rgba(61,255,154,0.28); border-radius: 10px;
    background: rgba(8,25,15,0.55); color: #ffffff;
    font-size: 14px; font-family: 'DM Sans', sans-serif; outline: none;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  }}
  .field input::placeholder {{ color: rgba(255,255,255,0.25); }}
  .field input:focus {{
    border-color: var(--green-bright);
    box-shadow: 0 0 0 3px rgba(61,255,154,0.15);
    background: rgba(10,30,18,0.65);
  }}

  .btn-primary {{
    width: 100%; padding: 13px;
    background: linear-gradient(135deg, var(--orange-mid) 0%, #8B3A0A 100%);
    color: #ffffff; border: none; border-radius: 10px;
    font-size: 14px; font-weight: 700; font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.08em; text-transform: uppercase; cursor: pointer;
    box-shadow: 0 4px 24px rgba(224,104,32,0.45), 0 0 0 1px rgba(255,140,66,0.25);
    transition: box-shadow 0.2s, transform 0.2s, opacity 0.2s; margin-top: 4px;
  }}
  .btn-primary:hover {{
    box-shadow: 0 8px 32px rgba(224,104,32,0.65), 0 0 0 1px rgba(255,140,66,0.5);
    transform: translateY(-2px);
  }}
  .btn-primary:disabled {{ opacity: 0.6; cursor: wait; transform: none; }}
  .btn-continue {{
    background: linear-gradient(135deg, var(--green-mid) 0%, var(--green-deep) 100%);
    box-shadow: 0 4px 24px rgba(29,184,106,0.4), 0 0 0 1px rgba(61,255,154,0.2);
  }}
  .btn-continue:hover {{
    box-shadow: 0 8px 32px rgba(29,184,106,0.62), 0 0 0 1px rgba(61,255,154,0.45);
  }}

  .error-box {{
    display: {error_display};
    align-items: center; gap: 8px;
    background: rgba(220,60,40,0.18); border: 1px solid rgba(220,80,50,0.5);
    border-radius: 10px; padding: 11px 14px;
    margin-bottom: 16px; color: #ffcfc8; font-size: 13px;
  }}

  .panel-footer {{
    text-align: center; font-size: 10.5px;
    color: rgba(255,140,66,0.28); margin-top: 28px; letter-spacing: 0.05em;
  }}
</style>
</head>
<body>

<div class="bg-stage">
  {slideshow_html}
</div>
<div class="bg-overlay"></div>
<div class="slide-dots" id="slideDots">{dot_html}</div>

<div class="page">
  <div class="glass-panel">
    <div class="slide-track" id="track">

      <!-- PANEL 1: WELCOME -->
      <div class="slide-panel">
        <div class="accent-bar"><div class="accent-dot"></div><div class="accent-line"></div></div>
        <div class="system-name">African Children's<br>Choir Archives</div>
        <div class="system-sub">Data Tracker &nbsp;&middot;&nbsp; v1.0</div>
        <div class="divider"></div>
        <div class="welcome-body">
          A living record of the <strong>children, choirs, and stories</strong>
          that have shaped this mission over the decades.<br><br>
          Sign in to explore, search, and contribute to the archive.
        </div>
        <button class="btn-primary btn-continue" onclick="goToForm()">Continue &rarr;</button>
        <div class="panel-footer">African Children's Choir Archives &middot; v1.0</div>
      </div>

      <!-- PANEL 2: LOGIN FORM -->
      <div class="slide-panel">
        <button class="back-btn" onclick="goToWelcome()">&#8592; Back</button>
        <div class="accent-bar"><div class="accent-dot"></div><div class="accent-line"></div></div>
        <div class="form-heading">Welcome back</div>
        <div class="form-desc">Sign in to your account to continue</div>

        <div class="error-box" id="errorBox">&#9888;&nbsp; Incorrect username or password</div>

        <div class="field">
          <label for="ui_username">Username</label>
          <input type="text" id="ui_username" placeholder="Enter your username" autocomplete="username">
        </div>
        <div class="field">
          <label for="ui_password">Password</label>
          <input type="password" id="ui_password" placeholder="Enter your password" autocomplete="current-password">
        </div>
        <button class="btn-primary" id="signInBtn" onclick="handleLogin()">Sign in</button>

        <div class="panel-footer">African Children's Choir Archives &middot; v1.0</div>
      </div>

    </div>
  </div>
</div>

<script>
  // ── CARD NAV — pure in-page JS, no parent access needed ──
  function goToForm() {{
    document.getElementById('track').classList.add('show-form');
    setTimeout(() => document.getElementById('ui_username').focus(), 600);
  }}
  function goToWelcome() {{
    document.getElementById('track').classList.remove('show-form');
  }}

  // ── AUTH: redirect parent via window.parent.location ──
  function handleLogin() {{
    const user = document.getElementById('ui_username').value.trim();
    const pass = document.getElementById('ui_password').value;
    if (!user || !pass) return;

    const btn = document.getElementById('signInBtn');
    btn.textContent = 'Signing in\u2026';
    btn.disabled = true;

    try {{
      const parentUrl = new URL(window.parent.location.href);
      parentUrl.searchParams.set('login_user', user);
      parentUrl.searchParams.set('login_pass', pass);
      window.parent.location.href = parentUrl.toString();
    }} catch(e) {{
      const base = document.referrer || window.location.href;
      const url = new URL(base);
      url.searchParams.set('login_user', user);
      url.searchParams.set('login_pass', pass);
      window.location.href = url.toString();
    }}
  }}

  document.getElementById('ui_password').addEventListener('keydown', e => {{
    if (e.key === 'Enter') handleLogin();
  }});
  document.getElementById('ui_username').addEventListener('keydown', e => {{
    if (e.key === 'Enter') document.getElementById('ui_password').focus();
  }});

  // Auto-show login panel if last attempt errored
  if ('{error_display}' === 'flex') {{
    document.getElementById('track').classList.add('show-form');
  }}

  // ── DOT SYNC ──
  const N      = {n};
  const PERIOD = {PERIOD * 1000};
  const TOTAL  = {TOTAL * 1000};

  if (N > 1) {{
    const dots  = document.querySelectorAll('.slide-dot');
    const start = performance.now();
    function syncDots(now) {{
      const elapsed = (now - start) % TOTAL;
      const active  = Math.floor(elapsed / PERIOD);
      dots.forEach((d, i) => d.classList.toggle('active', i === active));
      requestAnimationFrame(syncDots);
    }}
    requestAnimationFrame(syncDots);
  }}
</script>
</body>
</html>"""

    # ── WRITE TO TEMP FILE & SERVE VIA st.iframe ──
    # st.html() sandboxes JS completely — buttons, navigation, all broken.
    # st.iframe() serves a real file URL with full JS execution enabled.
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    )
    tmp.write(html_content)
    tmp.flush()
    tmp.close()

    st.iframe(tmp.name, height=800)

    # Clean up temp file after serving
    try:
        os.unlink(tmp.name)
    except Exception:
        pass

    return False
