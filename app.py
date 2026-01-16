import streamlit as st
import time
from core import auth, db
from core.admin_dashboard import admin_dashboard
from core.member_dashboard import member_dashboard

def apply_global_style():
    st.markdown(
        """
        <style>
        :root {
            --primary: #4f46e5;
            --primary-dark: #312e81;
            --accent: #14b8a6;
            --text: #0f172a;
            --muted: #64748b;
            --card: #ffffff;
            --border: #e2e8f0;
            --surface: #f8fafc;
            --sidebar: #111827;
        }

        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #ecfeff 100%);
            color: var(--text);
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

        div[data-testid="stForm"] {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.75rem 2rem;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
        }

        .hero-card {
            background: linear-gradient(120deg, rgba(79, 70, 229, 0.12), rgba(20, 184, 166, 0.12));
            border: 1px solid rgba(148, 163, 184, 0.45);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }

        .hero-card h1 {
            margin-bottom: 0.4rem;
            color: #1e1b4b;
        }

        .hero-card p {
            color: var(--muted);
        }

        .info-pill {
            display: inline-block;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            background: rgba(79, 70, 229, 0.12);
            color: #4338ca;
            font-weight: 600;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }

        .stButton > button {
            background: linear-gradient(90deg, #4f46e5, #4338ca);
            color: #ffffff;
            border-radius: 12px;
            border: none;
            padding: 0.6rem 1.3rem;
            font-weight: 600;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 12px 24px rgba(79, 70, 229, 0.25);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 32px rgba(79, 70, 229, 0.3);
        }

        .stButton > button:focus {
            outline: 2px solid #a5b4fc;
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
            background: #4338ca;
            color: #ffffff;
            border-color: #4338ca;
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
            color: #1e1b4b;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stSelectbox"] div {
            background: var(--surface);
            border-radius: 10px;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: #a5b4fc;
            box-shadow: 0 0 0 2px rgba(165, 180, 252, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def login_page():
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
    st.header("Login")

    with st.form("login_form"):
        phone_number = st.text_input("Phone Number").lower()
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            user = auth.check_login(phone_number, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user['User_ID']
                st.session_state['username'] = user['Username']
                st.session_state['role'] = user['Role']
                st.session_state['page'] = 'dashboard'
                st.rerun()
            else:
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
                    st.success("Account created successfully! Please log in.")
                    time.sleep(2)
                    st.session_state['page'] = 'login'
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please fill out all fields.")

    if st.button("Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Welfare Fund Management", layout="wide")
    apply_global_style()
    
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
