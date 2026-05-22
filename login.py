import streamlit as st
import streamlit.components.v1 as components

from database import verify_user


LANGUAGE_OPTIONS = ["English", "ไทย"]

TRANSLATIONS = {
    "English": {
        "language_setting": "Language / ภาษา",
        "sign_in_title": "Sign In",
        "email_username": "Email / Username",
        "password": "Password",
        "sign_in": "Sign in",
        "invalid_login": "Invalid username or password.",
        "no_account": "Don't have an account?",
        "sign_up": "Sign up",
        "guest_login": "Log in as Guest",
        "guest_username": "Guest",
    },
    "ไทย": {
        "language_setting": "ภาษา / Language",
        "sign_in_title": "เข้าสู่ระบบ",
        "email_username": "อีเมล / ชื่อผู้ใช้",
        "password": "รหัสผ่าน",
        "sign_in": "เข้าสู่ระบบ",
        "invalid_login": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
        "no_account": "ยังไม่มีบัญชี?",
        "sign_up": "สมัครสมาชิก",
        "guest_login": "เข้าใช้งานแบบผู้เยี่ยมชม",
        "guest_username": "ผู้เยี่ยมชม",
    },
}


def init_language_state():
    if "language" not in st.session_state:
        st.session_state.language = "English"


def current_language():
    language = st.session_state.get("language", "English")
    if language not in LANGUAGE_OPTIONS:
        return "English"
    return language


def t(key):
    language = current_language()
    return TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(
        key,
        TRANSLATIONS["English"].get(key, key),
    )


def go_to(page):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


def continue_as_guest():
    st.session_state.is_authenticated = True
    st.session_state.is_guest = True
    st.session_state.user_id = None
    st.session_state.username = t("guest_username")
    st.session_state.page = "dashboard"
    st.query_params["page"] = "dashboard"
    st.rerun()


def render_ripples():
    components.html(
        """
        <script>
          const doc = window.parent.document;

          if (window.parent.__taxaraRippleCleanup) {
            window.parent.__taxaraRippleCleanup();
          }

          let canvas = doc.getElementById("auth-ripple-canvas");
          if (!canvas) {
            canvas = doc.createElement("canvas");
            canvas.id = "auth-ripple-canvas";
            doc.body.appendChild(canvas);
          }

          const ctx = canvas.getContext("2d");
          let ripples = [];

          function resize() {
            const dpr = window.parent.devicePixelRatio || 1;
            canvas.width = window.parent.innerWidth * dpr;
            canvas.height = window.parent.innerHeight * dpr;
            canvas.style.width = window.parent.innerWidth + "px";
            canvas.style.height = window.parent.innerHeight + "px";
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
          }

          function addRipple(x, y) {
            ripples.push({ x, y, r: 0, alpha: 0.26, width: 2.1 });
            if (ripples.length > 34) ripples.shift();
          }

          function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ripples.forEach((r) => {
              r.r += 2.1;
              r.alpha *= 0.965;

              ctx.beginPath();
              ctx.arc(r.x, r.y, r.r, 0, Math.PI * 2);
              ctx.strokeStyle = `rgba(196,181,253,${r.alpha})`;
              ctx.lineWidth = r.width;
              ctx.stroke();

              ctx.beginPath();
              ctx.arc(r.x, r.y, r.r * 0.58, 0, Math.PI * 2);
              ctx.strokeStyle = `rgba(147,197,253,${r.alpha * 0.82})`;
              ctx.lineWidth = 1.2;
              ctx.stroke();
            });

            ripples = ripples.filter((r) => r.alpha > 0.015);
            window.parent.__taxaraRippleFrame = requestAnimationFrame(animate);
          }

          let lastMove = 0;
          function onMove(e) {
            const now = Date.now();
            if (now - lastMove < 45) return;
            lastMove = now;
            addRipple(e.clientX, e.clientY);
          }

          resize();
          doc.addEventListener("mousemove", onMove);
          doc.addEventListener("click", (e) => addRipple(e.clientX, e.clientY));
          window.parent.addEventListener("resize", resize);

          window.parent.__taxaraRippleCleanup = function () {
            doc.removeEventListener("mousemove", onMove);
            if (window.parent.__taxaraRippleFrame) {
              cancelAnimationFrame(window.parent.__taxaraRippleFrame);
            }
            const oldCanvas = doc.getElementById("auth-ripple-canvas");
            if (oldCanvas) oldCanvas.remove();
          };

          animate();
        </script>
        """,
        height=0,
    )


def render_styles():
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Syne:wght@700;800&family=Noto+Sans+Thai:wght@300;400;500;600;700;800&display=swap');

          #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
          [data-testid="stSidebarCollapsedControl"], section[data-testid="stSidebar"] {
            display: none !important;
          }

          html, body, .stApp {
            height: 100vh !important;
            overflow: hidden !important;
          }

          .stApp {
            background:
              radial-gradient(circle at 48% 42%, rgba(139,92,246,0.34), transparent 24%),
              radial-gradient(circle at 22% 22%, rgba(124,58,237,0.22), transparent 28%),
              radial-gradient(circle at 78% 22%, rgba(59,130,246,0.18), transparent 30%),
              linear-gradient(180deg, #030305 0%, #080810 48%, #030305 100%) !important;
            font-family: 'Noto Sans Thai', 'DM Sans', sans-serif;
          }

          .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
            opacity: 0.04;
            pointer-events: none;
            z-index: 0;
          }

          .stApp::after {
            content: "";
            position: fixed;
            left: 50%;
            top: 50%;
            width: 920px;
            height: 620px;
            transform: translate(-50%, -50%);
            border-radius: 999px;
            background: radial-gradient(ellipse, rgba(139,92,246,0.42) 0%, rgba(59,130,246,0.22) 34%, transparent 70%);
            filter: blur(88px);
            opacity: 0.92;
            pointer-events: none;
            z-index: 0;
            animation: auth-glow-pulse 8s ease-in-out infinite alternate;
          }

          @keyframes auth-glow-pulse {
            from { opacity: 0.72; transform: translate(-50%, -50%) scale(1); }
            to { opacity: 1; transform: translate(-50%, -50%) scale(1.08); }
          }

          [data-testid="stMainBlockContainer"] {
            position: relative;
            z-index: 2;
            width: min(430px, 92vw) !important;
            height: min(780px, 92vh) !important;
            margin: 4vh auto !important;
            padding: 52px 58px 40px !important;
            border-radius: 14px !important;
            background:
              linear-gradient(135deg, rgba(255,255,255,0.22), rgba(255,255,255,0.08)) !important;
            border: 1px solid rgba(255,255,255,0.26) !important;
            box-shadow:
              0 36px 110px rgba(0,0,0,0.46),
              inset 0 1px 0 rgba(255,255,255,0.22);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            display: flex !important;
            flex-direction: column !important;
          }

          #auth-ripple-canvas {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 1;
            mix-blend-mode: screen;
          }

          .language-label {
            color: rgba(248,250,252,0.82);
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 8px;
          }

          div[data-testid="stSelectbox"] {
            margin-bottom: 28px !important;
          }

          div[data-baseweb="select"] > div {
            min-height: 44px !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 14px !important;
            background: rgba(255,255,255,0.16) !important;
            color: #ffffff !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.12) !important;
          }

          div[data-baseweb="select"] span {
            color: #ffffff !important;
            font-weight: 800 !important;
          }

          div[data-baseweb="select"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
          }

          .auth-title {
            text-align: center;
            font-family: 'Noto Sans Thai', 'Syne', sans-serif !important;
            color: #f8fafc !important;
            font-size: 34px !important;
            line-height: 1.25 !important;
            padding: 4px 0 2px !important;
            margin: 0 0 44px !important;
            overflow: visible !important;
            text-shadow: 0 8px 26px rgba(0,0,0,0.24);
          }

          label {
            display: none !important;
          }

          div[data-testid="stTextInput"] {
            margin-bottom: 26px !important;
            position: relative !important;
            z-index: 5 !important;
          }

          div[data-testid="stTextInput"] label {
            display: none !important;
          }

          div[data-baseweb="input"] {
            min-height: 64px !important;
            border: none !important;
            border-radius: 22px !important;
            background: rgba(255,255,255,0.88) !important;
            box-shadow: 0 18px 42px rgba(0,0,0,0.14) !important;
            overflow: hidden !important;
            pointer-events: auto !important;
            transition: box-shadow 0.2s ease, transform 0.2s ease, background 0.2s ease !important;
          }

          div[data-baseweb="input"]:focus-within {
            transform: translateY(-1px);
            background: rgba(255,255,255,0.96) !important;
            box-shadow:
              0 20px 46px rgba(0,0,0,0.18),
              0 0 0 2px rgba(196,181,253,0.28) !important;
          }

          div[data-baseweb="input"] > div {
            background: transparent !important;
            border: none !important;
            pointer-events: auto !important;
          }

          div[data-baseweb="input"] input {
            min-height: 64px !important;
            border: none !important;
            outline: none !important;
            background: transparent !important;
            color: #3f1745 !important;
            caret-color: #7c3aed !important;
            font-size: 16px !important;
            font-weight: 800 !important;
            padding-left: 28px !important;
            padding-right: 44px !important;
            pointer-events: auto !important;
            cursor: text !important;
          }

          div[data-baseweb="input"] input::placeholder {
            color: rgba(63,23,69,0.46) !important;
            font-weight: 800 !important;
          }

          div[data-baseweb="input"] button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #3f1745 !important;
          }

          div[data-baseweb="input"] button svg {
            color: #3f1745 !important;
            fill: #3f1745 !important;
            stroke: #3f1745 !important;
            opacity: 0.78 !important;
          }

          div[data-baseweb="input"] button:hover svg {
            opacity: 1 !important;
          }

          div[data-testid="stButton"] button[kind="primary"] {
            min-height: 54px !important;
            width: min(280px, 78%) !important;
            margin: 24px auto 0 !important;
            display: block !important;
            border: none !important;
            border-radius: 999px !important;
            background: linear-gradient(135deg, #c04fd7, #b956dc) !important;
            color: #ffffff !important;
            font-size: 15px !important;
            font-weight: 900 !important;
            letter-spacing: 0 !important;
            text-transform: none !important;
            box-shadow: 0 18px 38px rgba(192,79,215,0.30) !important;
          }

          .auth-spacer {
            flex: 1;
            min-height: 92px;
          }

          .auth-footer-text {
            color: rgba(248,250,252,0.86);
            font-size: 15px;
            white-space: nowrap;
            line-height: 24px;
          }

          div[data-testid="stButton"] button:not([kind="primary"]) {
            background: transparent !important;
            border: none !important;
            color: #ffffff !important;
            text-decoration: none !important;
            padding: 0 !important;
            min-height: 24px !important;
            height: 24px !important;
            box-shadow: none !important;
            font-weight: 800 !important;
          }

          div[data-testid="stButton"] button:not([kind="primary"]):hover {
            color: #c4b5fd !important;
            text-decoration: underline !important;
            background: transparent !important;
          }

          .stAlert {
            border-radius: 16px !important;
            margin-top: 14px !important;
          }

          @media (max-height: 760px) {
            [data-testid="stMainBlockContainer"] {
              height: 94vh !important;
              margin: 3vh auto !important;
              padding-top: 34px !important;
              padding-bottom: 28px !important;
            }

            .auth-title {
              margin-bottom: 28px !important;
            }

            div[data-testid="stSelectbox"] {
              margin-bottom: 20px !important;
            }

            div[data-baseweb="input"] {
              min-height: 56px !important;
            }

            div[data-baseweb="input"] input {
              min-height: 56px !important;
            }

            .auth-spacer {
              min-height: 44px;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_language_selector():
    st.markdown(f'<div class="language-label">{t("language_setting")}</div>', unsafe_allow_html=True)
    language_index = LANGUAGE_OPTIONS.index(current_language())

    st.selectbox(
        t("language_setting"),
        LANGUAGE_OPTIONS,
        index=language_index,
        key="language",
        label_visibility="collapsed",
    )


def show_page():
    init_language_state()
    render_styles()
    render_ripples()

    render_language_selector()

    st.markdown(
        f'<div class="auth-title">{t("sign_in_title")}</div>',
        unsafe_allow_html=True,
    )

    username = st.text_input(
        t("email_username"),
        placeholder=t("email_username"),
    )
    password = st.text_input(
        t("password"),
        placeholder=t("password"),
        type="password",
    )

    if st.button(t("sign_in"), type="primary", use_container_width=True):
        success, user = verify_user(username, password)
        if success:
            st.session_state.is_authenticated = True
            st.session_state.is_guest = False
            st.session_state.user_id = user["id"]
            st.session_state.username = user["username"]
            go_to("dashboard")
        else:
            st.error(t("invalid_login"))

    st.markdown('<div class="auth-spacer"></div>', unsafe_allow_html=True)

    left, right = st.columns([0.58, 0.42])

    with left:
        st.markdown(
            f'<div class="auth-footer-text">{t("no_account")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("sign_up"), key="go_register"):
            go_to("register")

    with right:
        if st.button(t("guest_login"), key="guest_login"):
            continue_as_guest()