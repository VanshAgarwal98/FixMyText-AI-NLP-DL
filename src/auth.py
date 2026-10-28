"""
FixMyText AI — Authentication helpers for Streamlit sessions.

Uses bcrypt-hashed passwords stored in SQLite.
Session state keys: logged_in, user_id, username, role.
"""

import streamlit as st
from src.database import authenticate_user, create_user, ensure_admin


def _init_session():
    """Guarantee auth keys exist in session state."""
    defaults = {"logged_in": False, "user_id": None, "username": None, "role": None}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def login(username: str, password: str) -> bool:
    """Attempt login; set session state on success."""
    _init_session()
    user = authenticate_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.role = user["role"]
        return True
    return False


def logout():
    """Clear session auth state."""
    for k in ("logged_in", "user_id", "username", "role"):
        st.session_state[k] = None
    st.session_state.logged_in = False


def register(username: str, password: str, role: str = "user") -> bool:
    """Register a new user. Returns True on success."""
    uid = create_user(username, password, role)
    return uid is not None


def require_login() -> bool:
    """Return True if user is logged in; otherwise show login form."""
    _init_session()
    return st.session_state.get("logged_in", False)


def is_admin() -> bool:
    """Return True if the logged-in user has the admin role."""
    _init_session()
    return st.session_state.get("role") == "admin"


def current_user_id() -> int | None:
    _init_session()
    return st.session_state.get("user_id")


def current_username() -> str | None:
    _init_session()
    return st.session_state.get("username")


def render_auth_sidebar():
    """Render login / register / logout controls in the sidebar."""
    _init_session()
    ensure_admin()

    if st.session_state.logged_in:
        role_icon = "🛡️" if st.session_state.role == "admin" else "🎓"
        role_name = "Administrator" if st.session_state.role == "admin" else "Student / Staff"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 12px 14px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-weight: 700; color: #ffffff; font-size: 0.95rem;">{st.session_state.username}</div>
                    <div style="font-size: 0.75rem; color: #52ab98; font-weight: 600;">{role_icon} {role_name}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sign Out", key="sidebar_logout", use_container_width=True):
            logout()
            st.rerun()
    else:
        st.caption("AUTHENTICATION")
        # Quick Demo Logins
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔑 Admin", key="quick_admin", help="Quick login as administrator", use_container_width=True):
                login("admin", "admin123")
                st.rerun()
        with col_b:
            if st.button("🎓 Student", key="quick_student", help="Quick login as student", use_container_width=True):
                login("student1", "student123")
                st.rerun()

        with st.expander("Custom Login / Register", expanded=False):
            tab_login, tab_register = st.tabs(["Login", "Register"])
            with tab_login:
                u = st.text_input("Username", key="login_u")
                p = st.text_input("Password", type="password", key="login_p")
                if st.button("Sign In", key="btn_login", type="primary", use_container_width=True):
                    if login(u, p):
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            with tab_register:
                nu = st.text_input("Choose username", key="reg_u")
                np_ = st.text_input("Choose password", type="password", key="reg_p")
                np2 = st.text_input("Confirm password", type="password", key="reg_p2")
                if st.button("Register", key="btn_reg", use_container_width=True):
                    if len(nu.strip()) < 3:
                        st.error("Username must be at least 3 characters.")
                    elif len(np_) < 5:
                        st.error("Password must be at least 5 characters.")
                    elif np_ != np2:
                        st.error("Passwords do not match.")
                    elif register(nu, np_):
                        st.success("Account created! Please log in.")
                    else:
                        st.error("Username already taken.")
