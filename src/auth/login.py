import streamlit as st
from pathlib import Path
from src.auth.auth_manager import authenticate


# ==========================================================
# LOGIN PAGE
# ==========================================================

def login_page():

    # ---------- CSS ----------
    st.markdown("""
    <style>
    .stApp{
        background-color: #DCE7F3;
    }
    
    header {visibility:hidden;}
    footer {visibility:hidden;}

    .block-container{
        padding-top:0.8rem;
        padding-bottom:0rem;
        padding-left:2.5rem;
        padding-right:2.5rem;
        max-width:100%;
    }

    div.stButton > button{
        height:52px;
        width:100%;
        border-radius:10px;
        font-size:17px;
        font-weight:600;
        background:linear-gradient(90deg,#2563EB,#0EA5E9);
        color:white;
        border:none;
    }

    div.stButton > button:hover{
        color:white;
    }

    /* ---------- Left panel: plain white box, black text ---------- */
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]{
        background-color:#FFFFFF !important;
    }

    div[data-testid="column"]:nth-of-type(1) label,
    div[data-testid="column"]:nth-of-type(1) p,
    div[data-testid="column"]:nth-of-type(1) h1,
    div[data-testid="column"]:nth-of-type(1) h2,
    div[data-testid="column"]:nth-of-type(1) h3,
    div[data-testid="column"]:nth-of-type(1) span,
    div[data-testid="column"]:nth-of-type(1) div{
        color:#000000 !important;
    }

    div[data-testid="column"]:nth-of-type(1) input{
        color:#000000 !important;
    }

    /* Keep the Login button text white for contrast on its blue gradient */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button,
    div[data-testid="column"]:nth-of-type(1) div.stButton > button *{
        color:#FFFFFF !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------- Title spacing ----------
    st.write("")

    left, right = st.columns([1, 1], gap="large")

    # ======================================================
    # LEFT PANEL
    # ======================================================

    with left:

        with st.container(border=True):

            st.markdown(
                "<h2 style='font-weight:700;'>ContextIQ</h2>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "<p style='font-size:22px;font-weight:700;margin-top:-10px;'>"
                "Intelligent Answers. Trusted Knowledge."
                "</p>",
                unsafe_allow_html=True,
            )

            st.divider()

            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")


            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            st.write("\n")
            st.write("\n")


            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            st.write("")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")


            if st.button("Login", use_container_width=True):

                user = authenticate(username, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("Login Successful!")
                    st.rerun()

                else:

                    st.error("Invalid username or password.")

    # ======================================================
    # RIGHT PANEL
    # ======================================================

    with right:

        with st.container(border=True):

            image_path = (
                Path(__file__).resolve().parents[2]
                / "src"
                / "assets"
                / "login_illustration.jpg"
            )

            if image_path.exists():

                st.image(
                    str(image_path),
                    use_container_width=True,
                )

            else:

                st.warning("login_illustration.jpg not found.")

# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user = None

    for key in [
        "store",
        "chat_sessions",
        "current_chat",
        "sessions_restored",
    ]:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()






