import streamlit as st
import time
from core import auth, db
from core.admin_dashboard import admin_dashboard
from core.member_dashboard import member_dashboard
from core.ui_helpers import render_lottie

def queue_toast(message: str, icon: str = "✨") -> None:
    st.session_state["toast_payload"] = {"message": message, "icon": icon}

def show_queued_toast() -> None:
    toast_payload = st.session_state.pop("toast_payload", None)
    if toast_payload:
        st.toast(toast_payload["message"], icon=toast_payload["icon"])

def apply_global_style():
    st.markdown(
        """
        <style>
        :root {
            --primary: #1d4ed8;
            --primary-dark: #1e3a8a;
            --accent: #0f766e;
            --text: #0b1220;
            --muted: #475569;
            --card: #ffffff;
            --border: #dbe2ea;
            --surface: #f1f5f9;
            --sidebar: #0f172a;
            --highlight: #e0f2fe;
        }

        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 40%, #e0f2fe 100%);
            color: var(--text);
            background-size: 200% 200%;
            animation: backgroundShift 18s ease-in-out infinite;
        }

        .stApp header, .stApp footer {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
            color: #e2e8f0;
            border-right: 1px solid rgba(148, 163, 184, 0.2);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #f1f5f9;
        }

        [data-testid="stSidebar"] a {
            color: #93c5fd;
        }

        div[data-testid="stForm"] {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.75rem 2rem;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
            animation: fadeInUp 0.6s ease both;
        }

        .hero-card {
            background: linear-gradient(120deg, rgba(29, 78, 216, 0.12), rgba(14, 116, 144, 0.12));
            border: 1px solid rgba(148, 163, 184, 0.6);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.7s ease both;
        }

        .hero-card::before,
        .hero-card::after {
            content: "";
            position: absolute;
            border-radius: 999px;
            opacity: 0.6;
            filter: blur(0px);
            animation: floatOrb 8s ease-in-out infinite;
        }

        .hero-card::before {
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.25), rgba(37, 99, 235, 0));
            top: -60px;
            right: -40px;
        }

        .hero-card::after {
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(14, 116, 144, 0.25), rgba(14, 116, 144, 0));
            bottom: -90px;
            left: -60px;
            animation-delay: 1.4s;
        }

        .hero-card h1 {
            margin-bottom: 0.4rem;
            color: #0f172a;
        }

        .hero-card p {
            color: var(--muted);
        }

        .info-pill {
            display: inline-block;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            background: rgba(29, 78, 216, 0.12);
            color: #1d4ed8;
            font-weight: 600;
            font-size: 0.85rem;
            margin-right: 0.5rem;
            animation: pillGlow 2.8s ease-in-out infinite;
        }

        .stButton > button {
            background: linear-gradient(90deg, #1d4ed8, #1e40af);
            color: #ffffff;
            border-radius: 12px;
            border: none;
            padding: 0.6rem 1.3rem;
            font-weight: 600;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 12px 24px rgba(29, 78, 216, 0.25);
        }

        div[data-testid="stForm"] button,
        .stButton > button {
            opacity: 1 !important;
        }

        div[data-testid="stForm"] button:hover,
        .stButton > button:hover {
            transform: translateY(-1px) scale(1.02);
            box-shadow: 0 18px 34px rgba(29, 78, 216, 0.4), 0 0 18px rgba(59, 130, 246, 0.35);
        }

        .stButton > button:focus {
            outline: 2px solid #93c5fd;
            outline-offset: 2px;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.4rem 1rem;
            color: var(--muted);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: #1d4ed8;
            color: #ffffff;
            border-color: #1d4ed8;
        }

        div[data-testid="stMetric"] {
            background: var(--card);
            border-radius: 16px;
            padding: 1rem;
            border: 1px solid var(--border);
            box-shadow: 0 16px 32px rgba(15, 23, 42, 0.08);
        }

        div[data-testid="stMetric"] label {
            color: var(--muted);
        }

        div[data-testid="stMetric"] div {
            color: #0f172a;
        }

        button[data-testid="stSidebarCollapseButton"] {
            background: rgba(148, 163, 184, 0.2);
            border-radius: 10px;
            color: #e2e8f0;
            transition: background 0.2s ease, transform 0.2s ease;
        }

        button[data-testid="stSidebarCollapseButton"]:hover {
            background: rgba(147, 197, 253, 0.3);
            transform: translateY(-1px);
        }

        h1, h2, h3, h4 {
            color: #0f172a;
        }

        .stMarkdown small, .stCaption {
            color: var(--muted);
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] div {
            background: var(--surface);
            border-radius: 10px;
            color: var(--text);
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: #93c5fd;
            box-shadow: 0 0 0 2px rgba(147, 197, 253, 0.4);
        }

        label, .stMarkdown, .stMarkdown p, .stTextInput label, .stSelectbox label {
            color: var(--text);
        }

        .stAlert > div {
            border-radius: 12px;
        }

        .stAlert [data-testid="stMarkdownContainer"] {
            color: var(--text);
        }

        .dashboard-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin: 1.5rem 0 1.8rem;
        }

        .dashboard-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.3rem 1.4rem;
            box-shadow: 0 18px 32px rgba(15, 23, 42, 0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            animation: fadeInUp 0.7s ease both;
        }

        .dashboard-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 24px 36px rgba(15, 23, 42, 0.14);
        }

        .card-icon {
            width: 52px;
            height: 52px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            background: linear-gradient(135deg, rgba(29, 78, 216, 0.2), rgba(14, 116, 144, 0.2));
            color: #1d4ed8;
            margin-bottom: 0.75rem;
        }

        .card-title {
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.35rem;
        }

        .card-desc {
            color: var(--muted);
            margin: 0;
            font-size: 0.95rem;
        }

        .lottie-wrapper {
            width: 100%;
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.4);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
            animation: fadeInUp 0.8s ease both;
        }

        @media (max-width: 768px) {
            .hero-card {
                padding: 1.5rem;
            }

            .dashboard-cards {
                grid-template-columns: 1fr;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }

        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(12px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes floatOrb {
            0%,
            100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(12px);
            }
        }

        @keyframes pillGlow {
            0%,
            100% {
                box-shadow: 0 0 0 rgba(29, 78, 216, 0.2);
            }
            50% {
                box-shadow: 0 8px 18px rgba(29, 78, 216, 0.25);
            }
        }

        @keyframes backgroundShift {
            0%,
            100% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def login_page():
    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown(
            """
            <div class="hero-card">
                <span class="info-pill">Secure Access</span>
                <span class="info-pill">Member & Admin</span>
                <h1>Society Welfare Fund Management System</h1>
                <p>Track contributions, manage funds, and keep your community finances organized.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        render_lottie("https://assets7.lottiefiles.com/packages/lf20_0yfsb3a1.json", height=240, key="login-lottie")
    st.header("Login")

    with st.form("login_form"):
        phone_number = st.text_input("Phone Number").lower()
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            user = auth.check_login(phone_number, password)
            if user:
                queue_toast("Welcome back! Redirecting to your dashboard.", icon="✅")
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user['User_ID']
                st.session_state['username'] = user['Username']
                st.session_state['role'] = user['Role']
                st.session_state['page'] = 'dashboard'
                st.rerun()
            else:
                st.toast("Login failed. Please check your credentials.", icon="⚠️")
                st.error("Invalid phone number or password.")

    if st.button("Create new account"):
        st.session_state['page'] = 'register'
        st.rerun()

def registration_page():
    st.markdown(
        """
        <div class="hero-card">
            <span class="info-pill">Quick Setup</span>
            <span class="info-pill">Secure Profiles</span>
            <h1>Create your account</h1>
            <p>Join the society portal in minutes to manage your dues and stay updated.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("registration_form"):
        new_username = st.text_input("Username (this will be your display name)").lower()
        phone_number = st.text_input("Phone Number (this will be your User ID for login)").lower()
        new_password = st.text_input("Choose a Password", type="password")
        email = st.text_input("Email (Optional)").lower()
        role = st.selectbox("Select Role", ["Member", "Admin"])
        register_button = st.form_submit_button("Register")

        if register_button:
            if new_username and new_password and phone_number:
                success, message = auth.create_user(new_username, new_password, role, phone_number, email)
                if success:
                    queue_toast("Account created successfully. Please log in to continue.", icon="🎉")
                    st.success("Account created successfully! Please log in.")
                    time.sleep(2)
                    st.session_state['page'] = 'login'
                    st.rerun()
                else:
                    st.toast("Registration failed. Please review the details.", icon="❌")
                    st.error(message)
            else:
                st.toast("Please fill out all required fields.", icon="ℹ️")
                st.warning("Please fill out all fields.")

    if st.button("Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Welfare Fund Management", layout="wide")
    apply_global_style()

    if "reduce_motion" not in st.session_state:
        st.session_state["reduce_motion"] = False
    with st.sidebar:
        st.markdown("### Preferences")
        st.session_state["reduce_motion"] = st.toggle(
            "Reduce motion",
            value=st.session_state["reduce_motion"],
            help="Turn off animations for a calmer experience.",
        )
    show_queued_toast()
    
    db.setup_database()

    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state['username'] = None
        st.session_state['role'] = None

    # Page routing
    if st.session_state['logged_in']:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state['page'] = 'login'
            st.session_state['logged_in'] = False
            st.rerun()
        
        # Role-based page rendering
        if st.session_state['role'] == 'Admin':
            admin_dashboard()
        elif st.session_state['role'] == 'Member':
            member_dashboard()
        else:
            st.error("Unknown role. Please contact support.")
    
    elif st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'register':
        registration_page()

if __name__ == "__main__":
    main()
