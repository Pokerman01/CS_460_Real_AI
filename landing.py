import re

import streamlit as st
import streamlit.components.v1 as components


LANGUAGE_OPTIONS = ["English", "ไทย"]

TRANSLATIONS = {
    "English": {
        "language_setting": "Language / ภาษา",
        "nav_features": "Features",
        "nav_pricing": "Pricing",
        "nav_docs": "Docs",
        "nav_blog": "Blog",
        "nav_sign_in": "Sign In ->",
        "badge": "Multimodal AI · Built for Thai Tax Season 2026",
        "hero_title": "Next-Gen<br>Receipt Intelligence",
        "hero_subtitle": "Advancing expense tracking with multimodal AI,<br>automated deductions & Thai tax review support.",
        "start_free": "Start for Free",
        "watch_demo": "Watch Demo",
        "scan_accuracy": "Scan Accuracy",
        "receipts_processed": "Receipts Processed",
        "avg_tax_save": "Avg. Tax Save Find",
        "feature_ocr_title": "Smart OCR Scanning",
        "feature_ocr_desc": "Capture receipts via camera or upload. AI extracts line items instantly.",
        "feature_tax_title": "Thai Tax Review",
        "feature_tax_desc": "Helps classify expenses as deductible, non-deductible, or needing review.",
        "feature_analytics_title": "Expense Analytics",
        "feature_analytics_desc": "Real-time dashboards. Spot trends, categories, and savings opportunities at a glance.",
        "feature_secure_title": "Private Receipt History",
        "feature_secure_desc": "Each signed-in user sees only their own saved receipts and reports.",
    },
    "ไทย": {
        "language_setting": "ภาษา / Language",
        "nav_features": "ฟีเจอร์",
        "nav_pricing": "ราคา",
        "nav_docs": "คู่มือ",
        "nav_blog": "บทความ",
        "nav_sign_in": "เข้าสู่ระบบ ->",
        "badge": "AI วิเคราะห์ใบเสร็จ · สำหรับฤดูกาลภาษีไทย 2026",
        "hero_title": "ระบบวิเคราะห์<br>ใบเสร็จอัจฉริยะ",
        "hero_subtitle": "ช่วยจัดการรายจ่ายด้วย AI วิเคราะห์ใบเสร็จ<br>พร้อมแนะนำการหักค่าใช้จ่ายทางภาษีสำหรับผู้ใช้ในไทย",
        "start_free": "เริ่มใช้งานฟรี",
        "watch_demo": "ดูตัวอย่าง",
        "scan_accuracy": "ความแม่นยำในการสแกน",
        "receipts_processed": "ใบเสร็จที่ประมวลผล",
        "avg_tax_save": "เวลาประเมินภาษีเฉลี่ย",
        "feature_ocr_title": "สแกนใบเสร็จอัจฉริยะ",
        "feature_ocr_desc": "อัปโหลดหรือถ่ายภาพใบเสร็จ แล้วให้ AI ดึงข้อมูลสำคัญให้อัตโนมัติ",
        "feature_tax_title": "ช่วยตรวจสอบภาษีไทย",
        "feature_tax_desc": "ช่วยแยกรายการว่าอาจหักเป็นค่าใช้จ่ายได้ หักไม่ได้ หรือควรตรวจสอบเพิ่มเติม",
        "feature_analytics_title": "วิเคราะห์รายจ่าย",
        "feature_analytics_desc": "ดูแดชบอร์ดสรุปรายจ่าย หมวดหมู่ และโอกาสในการจัดการภาษีได้ง่ายขึ้น",
        "feature_secure_title": "ประวัติใบเสร็จส่วนตัว",
        "feature_secure_desc": "ผู้ใช้ที่เข้าสู่ระบบจะเห็นเฉพาะใบเสร็จและรายงานของตนเองเท่านั้น",
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


def render_language_selector():
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
    render_language_selector()

    html_content = """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Syne:wght@400;600;700;800&family=Inter:wght@400;500;600&family=Noto+Sans+Thai:wght@300;400;500;600;700;800&display=swap');

      #MainMenu, header, footer, [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stSidebarCollapsedControl"],
      section[data-testid="stSidebar"] {
        display: none !important;
      }

      .main, .block-container,
      [data-testid="stAppViewContainer"],
      [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
      }

      html, body {
        background: #030305 !important;
        overflow-x: hidden;
        font-family: 'Noto Sans Thai', 'DM Sans', sans-serif;
      }

      div[data-testid="stSelectbox"] {
        position: fixed !important;
        top: 18px !important;
        right: 160px !important;
        z-index: 200 !important;
        width: 132px !important;
      }

      div[data-testid="stSelectbox"] label {
        display: none !important;
      }

      div[data-baseweb="select"] > div {
        min-height: 38px !important;
        border-radius: 999px !important;
        border: 1px solid rgba(139,92,246,0.4) !important;
        background: rgba(139,92,246,0.14) !important;
        color: #ffffff !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18) !important;
      }

      div[data-baseweb="select"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-family: 'Noto Sans Thai', 'Inter', sans-serif !important;
      }

      div[data-baseweb="select"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
      }

      #cursor-glow {
        position: fixed;
        top: 0;
        left: 0;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.15) 0%, rgba(59, 130, 246, 0.05) 40%, transparent 70%);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        z-index: 1;
        filter: blur(40px);
        opacity: 0;
        transition: opacity 0.5s ease;
      }

      .landing-container {
        position: relative;
        min-height: 100vh;
        width: 100vw;
        background: #030305;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
      }

      .landing-container::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
        opacity: 0.04;
        pointer-events: none;
        z-index: 1;
      }

      .aura-bg {
        position: fixed;
        inset: 0;
        z-index: 2;
        pointer-events: none;
      }

      .glow-center {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 900px;
        height: 600px;
        background: radial-gradient(ellipse, rgba(139, 92, 246, 0.6) 0%, rgba(59, 130, 246, 0.4) 30%, transparent 70%);
        filter: blur(90px);
        animation: glow-pulse 8s ease-in-out infinite alternate;
      }

      .glow-outer {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 1400px;
        height: 800px;
        background: radial-gradient(ellipse, rgba(76, 29, 149, 0.3) 0%, transparent 60%);
        filter: blur(120px);
        animation: glow-pulse 12s ease-in-out infinite alternate-reverse;
      }

      @keyframes glow-pulse {
        0% { opacity: 0.7; transform: translate(-50%, -50%) scale(1); }
        100% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
      }

      .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 40px;
        background: linear-gradient(180deg, rgba(3,3,5,0.9) 0%, transparent 100%);
      }

      .nav-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        color: white;
      }

      .logo-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: linear-gradient(135deg, #7c3aed, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5);
      }

      .logo-text {
        font-family: 'Noto Sans Thai', 'Syne', sans-serif;
        font-weight: 700;
        font-size: 16px;
        color: #f1f5f9;
      }

      .nav-links {
        display: flex;
        gap: 30px;
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .nav-links a {
        color: rgba(203, 213, 225, 0.7) !important;
        text-decoration: none !important;
        border-bottom: none !important;
        font-family: 'Noto Sans Thai', 'Inter', sans-serif !important;
        font-size: 14px;
        font-weight: 500 !important;
        transition: color 0.2s;
      }

      .nav-links a:hover {
        color: #e2e8f0 !important;
      }

      .nav-signin {
        padding: 8px 20px;
        border-radius: 100px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.4) !important;
        color: #c4b5fd !important;
        text-decoration: none !important;
        border-bottom: none !important;
        font-family: 'Noto Sans Thai', 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px;
        transition: all 0.3s;
      }

      .nav-signin:hover {
        background: rgba(139,92,246,0.2);
        box-shadow: 0 0 20px rgba(139,92,246,0.3);
        color: white !important;
      }

      .hero-section {
        position: relative;
        z-index: 10;
        text-align: center;
        padding: 0 20px;
        max-width: 900px;
        animation: fade-in 1s ease-out;
      }

      @keyframes fade-in {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border-radius: 100px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.3);
        color: #a78bfa;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 30px;
      }

      .badge-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #7c3aed;
        box-shadow: 0 0 8px #7c3aed;
        animation: pulse-dot 2s ease-in-out infinite;
      }

      @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }

      .hero-title {
        font-family: 'Noto Sans Thai', 'Syne', sans-serif;
        font-weight: 800;
        font-size: clamp(3rem, 8vw, 5.5rem);
        line-height: 1.12;
        letter-spacing: 0;
        margin-bottom: 25px;
        background: linear-gradient(160deg, #ffffff 0%, #e0e7ff 30%, #c4b5fd 60%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }

      .hero-subtitle {
        font-family: 'Noto Sans Thai', 'Inter', sans-serif;
        font-size: clamp(1rem, 2vw, 1.2rem);
        font-weight: 300;
        font-style: italic;
        color: rgba(148, 163, 184, 0.8);
        line-height: 1.7;
        margin-bottom: 45px;
        max-width: 680px;
        margin-left: auto;
        margin-right: auto;
      }

      .cta-buttons {
        display: flex;
        gap: 15px;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 60px;
      }

      .btn-primary {
        padding: 15px 32px;
        border-radius: 100px;
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #3b82f6 100%);
        color: white !important;
        text-decoration: none !important;
        border-bottom: none !important;
        font-family: 'Noto Sans Thai', 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 16px;
        border: none !important;
        cursor: pointer;
        box-shadow: 0 0 30px rgba(124,58,237,0.5);
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }

      .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 40px rgba(124,58,237,0.7);
      }

      .btn-secondary {
        padding: 15px 32px;
        border-radius: 100px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.3) !important;
        color: rgba(196, 181, 253, 0.9) !important;
        text-decoration: none !important;
        border-bottom: none !important;
        font-family: 'Noto Sans Thai', 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }

      .btn-secondary:hover {
        background: rgba(139,92,246,0.15);
        border-color: rgba(139,92,246,0.5) !important;
        transform: translateY(-2px);
        color: white !important;
      }

      .stats-row {
        display: flex;
        gap: 25px;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
      }

      .stat-item {
        text-align: center;
      }

      .stat-number {
        font-family: 'Noto Sans Thai', 'Syne', sans-serif;
        font-size: 22px;
        font-weight: 700;
        background: linear-gradient(135deg, #c4b5fd, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }

      .stat-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: rgba(100, 116, 139, 0.8);
        margin-top: 5px;
      }

      .stat-divider {
        width: 1px;
        height: 25px;
        background: rgba(148,163,184,0.2);
      }

      .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        max-width: 1000px;
        margin: 80px auto 60px;
        padding: 0 40px;
        position: relative;
        z-index: 10;
      }

      .feature-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 25px;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
      }

      .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.5), transparent);
      }

      .feature-card:hover {
        background: rgba(139,92,246,0.05);
        border-color: rgba(139,92,246,0.3);
        transform: translateY(-4px);
      }

      .feature-icon {
        font-size: 24px;
        width: 45px;
        height: 45px;
        border-radius: 10px;
        background: rgba(139,92,246,0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
      }

      .feature-title {
        font-family: 'Noto Sans Thai', 'Syne', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 8px;
      }

      .feature-desc {
        font-family: 'Noto Sans Thai', 'Inter', sans-serif;
        font-size: 13px;
        color: rgba(148,163,184,0.7);
        line-height: 1.6;
      }

      .bottom-fade {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 150px;
        background: linear-gradient(0deg, #030305 0%, transparent 100%);
        pointer-events: none;
        z-index: 5;
      }

      @media (max-width: 760px) {
        .nav-bar {
          padding: 18px 18px;
        }

        .nav-links {
          display: none;
        }

        .nav-signin {
          font-size: 13px;
          padding: 8px 14px;
        }

        div[data-testid="stSelectbox"] {
          top: 66px !important;
          right: 18px !important;
          width: 118px !important;
        }

        .hero-section {
          padding-top: 86px;
        }

        .badge {
          font-size: 10px;
          max-width: 86vw;
          text-align: center;
          justify-content: center;
        }

        .hero-title {
          font-size: clamp(2.5rem, 12vw, 4rem);
        }

        .stats-row {
          gap: 16px;
        }

        .stat-divider {
          display: none;
        }

        .features-grid {
          margin-top: 60px;
          padding: 0 20px;
        }
      }
    </style>

    <div class="landing-container">
      <div id="cursor-glow"></div>

      <div class="aura-bg">
        <div class="glow-outer"></div>
        <div class="glow-center"></div>
      </div>

      <div class="nav-bar">
        <a href="#" class="nav-logo">
          <div class="logo-icon">✦</div>
          <span class="logo-text">Taxara</span>
        </a>

        <ul class="nav-links">
          <li><a href="#features">__NAV_FEATURES__</a></li>
          <li><a href="#">__NAV_PRICING__</a></li>
          <li><a href="#">__NAV_DOCS__</a></li>
          <li><a href="#">__NAV_BLOG__</a></li>
        </ul>

        <a href="?page=login" target="_self" class="nav-signin">__NAV_SIGN_IN__</a>
      </div>

      <div class="hero-section">
        <div class="badge">
          <span class="badge-dot"></span>
          __BADGE__
        </div>

        <h1 class="hero-title">
          __HERO_TITLE__
        </h1>

        <p class="hero-subtitle">
          __HERO_SUBTITLE__
        </p>

        <div class="cta-buttons">
          <a href="?page=register" target="_self" class="btn-primary">
            __START_FREE__
            <span>-></span>
          </a>

          <a href="#features" class="btn-secondary">
            <span>▶</span>
            __WATCH_DEMO__
          </a>
        </div>

        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">__SCAN_ACCURACY__</div>
          </div>

          <div class="stat-divider"></div>

          <div class="stat-item">
            <div class="stat-number">40K+</div>
            <div class="stat-label">__RECEIPTS_PROCESSED__</div>
          </div>

          <div class="stat-divider"></div>

          <div class="stat-item">
            <div class="stat-number">12 min</div>
            <div class="stat-label">__AVG_TAX_SAVE__</div>
          </div>
        </div>
      </div>

      <div class="features-grid" id="features">
        <div class="feature-card">
          <div class="feature-icon">🧾</div>
          <div class="feature-title">__FEATURE_OCR_TITLE__</div>
          <div class="feature-desc">__FEATURE_OCR_DESC__</div>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🏛️</div>
          <div class="feature-title">__FEATURE_TAX_TITLE__</div>
          <div class="feature-desc">__FEATURE_TAX_DESC__</div>
        </div>

        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <div class="feature-title">__FEATURE_ANALYTICS_TITLE__</div>
          <div class="feature-desc">__FEATURE_ANALYTICS_DESC__</div>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔒</div>
          <div class="feature-title">__FEATURE_SECURE_TITLE__</div>
          <div class="feature-desc">__FEATURE_SECURE_DESC__</div>
        </div>
      </div>

      <div class="bottom-fade"></div>
    </div>
    """

    replacements = {
        "__NAV_FEATURES__": t("nav_features"),
        "__NAV_PRICING__": t("nav_pricing"),
        "__NAV_DOCS__": t("nav_docs"),
        "__NAV_BLOG__": t("nav_blog"),
        "__NAV_SIGN_IN__": t("nav_sign_in"),
        "__BADGE__": t("badge"),
        "__HERO_TITLE__": t("hero_title"),
        "__HERO_SUBTITLE__": t("hero_subtitle"),
        "__START_FREE__": t("start_free"),
        "__WATCH_DEMO__": t("watch_demo"),
        "__SCAN_ACCURACY__": t("scan_accuracy"),
        "__RECEIPTS_PROCESSED__": t("receipts_processed"),
        "__AVG_TAX_SAVE__": t("avg_tax_save"),
        "__FEATURE_OCR_TITLE__": t("feature_ocr_title"),
        "__FEATURE_OCR_DESC__": t("feature_ocr_desc"),
        "__FEATURE_TAX_TITLE__": t("feature_tax_title"),
        "__FEATURE_TAX_DESC__": t("feature_tax_desc"),
        "__FEATURE_ANALYTICS_TITLE__": t("feature_analytics_title"),
        "__FEATURE_ANALYTICS_DESC__": t("feature_analytics_desc"),
        "__FEATURE_SECURE_TITLE__": t("feature_secure_title"),
        "__FEATURE_SECURE_DESC__": t("feature_secure_desc"),
    }

    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, value)

    cleaned_html = re.sub(r"\n\s*\n", "\n", html_content)
    st.markdown(cleaned_html, unsafe_allow_html=True)

    components.html(
        """
        <script>
          const doc = window.parent.document;
          const glow = doc.getElementById("cursor-glow");

          if (glow) {
            doc.addEventListener("mousemove", function(e) {
              glow.style.opacity = "1";
              glow.style.left = e.clientX + "px";
              glow.style.top = e.clientY + "px";
            });

            doc.addEventListener("mouseleave", function() {
              glow.style.opacity = "0";
            });
          }
        </script>
        """,
        height=0,
        width=0,
    )