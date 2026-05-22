import streamlit as st
import streamlit.components.v1 as components

from database import create_user


LANGUAGE_OPTIONS = ["English", "ไทย"]

TRANSLATIONS = {
    "English": {
        "language_setting": "Language / ภาษา",
        "create_account_title": "Create Account",
        "email_username": "Email / Username",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "sign_up": "Sign up",
        "sign_in": "Sign in",
        "guest_login": "Log in as Guest",
        "already_have_account": "Already have an account?",
        "passwords_do_not_match": "Passwords do not match.",
        "guest_username": "Guest",
        "username_required": "Username is required.",
        "password_too_short": "Password must be at least 6 characters.",
        "username_registered": "That username is already registered.",
    },
    "ไทย": {
        "language_setting": "ภาษา / Language",
        "create_account_title": "สมัครบัญชีผู้ใช้",
        "email_username": "อีเมล / ชื่อผู้ใช้",
        "password": "รหัสผ่าน",
        "confirm_password": "ยืนยันรหัสผ่าน",
        "sign_up": "สมัครสมาชิก",
        "sign_in": "เข้าสู่ระบบ",
        "guest_login": "เข้าใช้งานแบบผู้เยี่ยมชม",
        "already_have_account": "มีบัญชีอยู่แล้ว?",
        "passwords_do_not_match": "รหัสผ่านไม่ตรงกัน",
        "guest_username": "ผู้เยี่ยมชม",
        "username_required": "กรุณากรอกชื่อผู้ใช้",
        "password_too_short": "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร",
        "username_registered": "ชื่อผู้ใช้นี้ถูกสมัครไว้แล้ว",
    },
}


CREATE_USER_MESSAGE_KEYS = {
    "Username is required.": "username_required",
    "Password must be at least 6 characters.": "password_too_short",
    "That username is already registered.": "username_registered",
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


def translate_create_user_message(message):
    message_key = CREATE_USER_MESSAGE_KEYS.get(message)
    if message_key:
        return t(message_key)
    return message


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
            min-height: min(780px, 92vh) !important;
            max-height: 92vh !important;
            margin: 4vh auto !important;
            padding: 34px 58px 30px !important;
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
            overflow: hidden !important;
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
            margin-bottom: 20px !important;
          }

          div[data-baseweb="select"] > div {
            min-height: 42px !important;
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
            font-size: 31px !important;
            line-height: 1.25 !important;
            padding: 4px 0 2px !important;
            margin: 0 0 24px !important;
            overflow: visible !important;
            text-shadow: 0 8px 26px rgba(0,0,0,0.24);
          }

          label {
            display: none !important;
          }

          div[data-testid="stTextInput"] {
            margin-bottom: 16px !important;
            position: relative !important;
            z-index: 5 !important;
          }

          div[data-testid="stTextInput"] label {
            display: none !important;
          }

          div[data-baseweb="input"] {
            min-height: 54px !important;
            border: none !important;
            border-radius: 20px !important;
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
            min-height: 54px !important;
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
            min-height: 50px !important;
            width: min(280px, 76%) !important;
            margin: 16px auto 0 !important;
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
            min-height: 12px;
          }

          .auth-footer-text {
            color: rgba(248,250,252,0.86);
            font-size: 15px;
            white-space: nowrap;
            line-height: 22px;
          }

          div[data-testid="stButton"] button:not([kind="primary"]) {
            background: transparent !important;
            border: none !important;
            color: #ffffff !important;
            text-decoration: none !important;
            padding: 0 !important;
            min-height: 22px !important;
            height: 22px !important;
            box-shadow: none !important;
            font-weight: 800 !important;
          }

          div[data-testid="stButton"] button:not([kind="primary"]):hover {
            color: #c4b5fd !important;
            text-decoration: underline !important;
            background: transparent !important;
          }

          .stAlert {
            border-radius: 10px !important;
            margin: 12px 0 6px !important;
            padding: 8px 12px !important;
            font-size: 13px !important;
          }

          @media (max-height: 760px) {
            [data-testid="stMainBlockContainer"] {
              min-height: 94vh !important;
              max-height: 94vh !important;
              margin: 3vh auto !important;
              padding: 24px 48px 24px !important;
            }

            .auth-title {
              margin-bottom: 18px !important;
              font-size: 28px !important;
            }

            div[data-testid="stSelectbox"] {
              margin-bottom: 14px !important;
            }

            div[data-testid="stTextInput"] {
              margin-bottom: 12px !important;
            }

            div[data-baseweb="input"] {
              min-height: 48px !important;
            }

            div[data-baseweb="input"] input {
              min-height: 48px !important;
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
        f'<div class="auth-title">{t("create_account_title")}</div>',
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
    confirm_password = st.text_input(
        t("confirm_password"),
        placeholder=t("confirm_password"),
        type="password",
    )

    if st.button(t("sign_up"), type="primary", use_container_width=True):
        if password != confirm_password:
            st.error(t("passwords_do_not_match"))
        else:
            success, message, user_id = create_user(username, password)
            if success:
                st.session_state.is_authenticated = True
                st.session_state.is_guest = False
                st.session_state.user_id = user_id
                st.session_state.username = username.strip().lower()
                go_to("dashboard")
            else:
                st.error(translate_create_user_message(message))

    st.markdown('<div class="auth-spacer"></div>', unsafe_allow_html=True)

    left, right = st.columns([0.58, 0.42])

    with left:
        st.markdown(
            f'<div class="auth-footer-text">{t("already_have_account")}</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("sign_in"), key="go_login"):
            go_to("login")

    with right:
        if st.button(t("guest_login"), key="guest_register"):
            continue_as_guest()