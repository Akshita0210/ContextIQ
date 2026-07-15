import os

import streamlit as st
from dotenv import load_dotenv

# ==========================================================
# AUTH
# ==========================================================

from src.auth.login import login_page

# ==========================================================
# UI
# ==========================================================

from src.ui.admin_dashboard import admin_dashboard

from src.ui.user_dashboard import (
    filter_relevant_sources,
    user_dashboard,
    display_chat_history,
    display_sources
)

# ==========================================================
# SERVICES
# ==========================================================

from src.services.rag_service import (
    load_embeddings,
    load_rag_pipeline,
    refresh_pipeline
)

# ==========================================================
# MEMORY
# ==========================================================

from src.memory.session_manager import (
    initialize_chat_sessions,
    create_new_chat,
    load_chat_index,
    save_chat_history,
    restore_user_sessions,
    rename_chat,
    delete_chat
)

# ==========================================================
# RAG
# ==========================================================

from src.chains.rag_chain import (
    build_conversational_chain
)

# ==========================================================
# PAGE CONFIG (UI ONLY)
# ==========================================================

st.set_page_config(
    page_title="ContextIQ",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# GLOBAL CSS (UI ONLY)
# ==========================================================

st.markdown(
    """
    <style>
        /* ---------- Global ---------- */
        html, body, [class*="css"] {
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        /* ---------- Sidebar background ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F5F7FF 0%, #EBEFFC 100%);
            border-right: 1px solid #C4CCEE;
        }

        /* =====================================================
           SIDEBAR FONT CONSISTENCY
           IMPORTANT: do NOT apply font-family to * inside the
           sidebar — Streamlit's collapse-arrow icon relies on
           a ligature icon font (Material Symbols). Overriding
           it globally breaks that icon and shows raw text like
           "keyboard_double_arrow_left". So we target only the
           specific text elements we actually control.
        ===================================================== */

        .sidebar-title,
        .sidebar-subtitle,
        .sidebar-department,
        .sidebar-department span,
        .sidebar-section-label,
        section[data-testid="stSidebar"] .stButton button,
        section[data-testid="stSidebar"] .stButton button p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] input {
            font-family: "Inter", "Segoe UI", sans-serif !important;
        }

        .sidebar-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #1E1B4B;
            margin-bottom: 0;
            line-height: 1.3;
        }

        .sidebar-subtitle {
            font-size: 0.82rem;
            font-weight: 400;
            color: #4C4F6B;
            margin-top: 0;
            line-height: 1.3;
        }

        .sidebar-department {
            font-size: 0.85rem;
            font-weight: 600;
            color: #312E81;
            margin: 0.6rem 0 0.2rem 0;
        }

        .sidebar-department span {
            font-weight: 400;
            color: #4C4F6B;
        }

        .sidebar-section-label {
            font-size: 0.78rem;
            font-weight: 700;
            color: #4338CA;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ---------- Buttons ---------- */
        section[data-testid="stSidebar"] .stButton button {
            border-radius: 8px;
            border: 1px solid #C4CCEE;
            background-color: #FFFFFF;
            color: #312E81 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease-in-out;
        }

        section[data-testid="stSidebar"] .stButton button p {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #312E81 !important;
        }

        section[data-testid="stSidebar"] .stButton button:hover {
            border-color: #4F46E5;
            color: #4F46E5 !important;
        }

        /* ---------- New Chat / Chat list buttons ---------- */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] .stButton button {
            background-color: #EEF1FC;
            border: 1px solid #D6DCF4;
            text-align: left;
        }

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] .stButton button:hover {
            background-color: #E0E5FA;
            border-color: #A5B0E3;
        }

        /* ---------- Global buttons ---------- */
        .stButton button {
            border-radius: 8px;
        }

        /* ---------- Divider spacing ---------- */
        hr {
            margin: 0.6rem 0;
            border-top: 1px solid #C4CCEE;
        }

        .chat-empty-state {
            text-align: center;
            color: #6366A5;
            font-size: 0.85rem;
            padding: 1.2rem 0.5rem;
        }

        /* ---------- Fix white bottom bar behind chat input ---------- */
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        div[data-testid="stChatInput"] {
            background: linear-gradient(180deg, #F5F7FF 0%, #EBEFFC 100%) !important;
        }

        [data-testid="stBottom"] > div {
            background: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# INITIALIZATION
# ==========================================================

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ Groq API Key not found in .env")
    st.stop()

# ==========================================================
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "store" not in st.session_state:
    st.session_state.store = {}

# ==========================================================
# LOGIN
# ==========================================================

if not st.session_state.logged_in:
    login_page()
    st.stop()

current_user = st.session_state.user

# ==========================================================
# LOAD EMBEDDINGS
# ==========================================================

with st.spinner("Loading knowledge engine..."):
    embeddings = load_embeddings()

# ==========================================================
# ADMIN ROUTING
# ==========================================================

if current_user["role"] == "Admin":

    admin_dashboard(
        embeddings
    )

    st.stop()

# ==========================================================
# USER INITIALIZATION
# ==========================================================

from src.memory.session_manager import (
    restore_user_sessions
)

restore_user_sessions(
    current_user["username"],
    st.session_state.store
)

department = current_user["department"]

with st.spinner(f"Preparing {department} assistant..."):

    pipeline = load_rag_pipeline(
        department
    )

    rag_chain = pipeline["rag_chain"]

    conversational_chain = build_conversational_chain(
        rag_chain,
        st.session_state.store
    )

session_id = st.session_state.current_chat


# ==========================================================
# USER SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        '<p class="sidebar-title">ContextIQ</p>'
        '<p class="sidebar-subtitle">Your AI knowledge assistant</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<p class="sidebar-title">Department: <span class="sidebar-subtitle">{department}</span></p>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "+  New Chat",
        use_container_width=True
    ):
        create_new_chat(
            current_user["username"]
        )

        st.rerun()

    st.divider()

    # -----------------------------------------
    # Chat List
    # -----------------------------------------

    st.markdown(
        '<span class="sidebar-title">Chat History</span>',
        unsafe_allow_html=True
    )

    st.write("")

    index = load_chat_index(
        current_user["username"]
    )

    if not index["chats"]:

        st.markdown(
            "<div class='chat-empty-state'>🗒️ No chats yet.<br>Start a new "
            "conversation above.</div>",
            unsafe_allow_html=True
        )

    for chat in index["chats"]:

        chat_id = chat["id"]
        title = chat["title"]

        is_active = (
            st.session_state.get("current_chat") == chat_id
        )

        col1, col2, col3 = st.columns([5, 1, 1])

        # -------------------------
        # Open Chat
        # -------------------------

        with col1:

            if st.button(
                f"{'●' if is_active else '○'} {title}",
                key=f"chat_{chat_id}",
                use_container_width=True
            ):

                st.session_state.current_chat = chat_id
                st.rerun()

        # -------------------------
        # Rename Button
        # -------------------------

        with col2:

            if st.button(
                "✏️",
                key=f"rename_{chat_id}"
            ):

                st.session_state.rename_chat = chat_id

        # -------------------------
        # Rename Textbox
        # -------------------------

        if (
            st.session_state.get("rename_chat")
            == chat_id
        ):

            with st.container():

                new_title = st.text_input(
                    "Rename Chat",
                    value=title,
                    key=f"title_{chat_id}",
                    label_visibility="collapsed"
                )

                col_save, col_cancel = st.columns(2)

                with col_save:

                    if st.button(
                        "✅ Save",
                        key=f"save_{chat_id}",
                        use_container_width=True
                    ):

                        rename_chat(
                            current_user["username"],
                            chat_id,
                            new_title
                        )

                        del st.session_state["rename_chat"]

                        st.rerun()

                with col_cancel:

                    if st.button(
                        "✖️ Cancel",
                        key=f"cancel_{chat_id}",
                        use_container_width=True
                    ):

                        del st.session_state["rename_chat"]

                        st.rerun()
        # -------------------------
        # Delete Chat
        # -------------------------

        with col3:

            if st.button(
                "🗑",
                key=f"delete_{chat_id}"
            ):

                delete_chat(
                    current_user["username"],
                    chat_id,
                    st.session_state.store
                )

                st.rerun()

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.store = {}

        st.rerun()


# ==========================================================
# USER DASHBOARD
# ==========================================================

user_query = user_dashboard(
    current_user
)

# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================

if session_id in st.session_state.store:

    history = st.session_state.store[
        session_id
    ]

    display_chat_history(
        history
    )

# ==========================================================
# PROCESS USER QUERY
# ==========================================================

if user_query:

    with st.chat_message("user"):

        st.write(user_query)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = conversational_chain.invoke(
                {
                    "input": user_query
                },
                config={
                    "configurable": {
                        "session_id": session_id
                    }
                }
            )

        history = st.session_state.store[
            session_id
        ]

        save_chat_history(
            current_user["username"],
            session_id,
            history.messages
        )

        st.write(response["answer"])

        if (
            response["answer"]
            != "I couldn't find this information in the current Knowledge Base."
        ):

            filtered_context = filter_relevant_sources(
                response["answer"],
                response["context"],
                max_sources=2
            )

            display_sources(filtered_context)