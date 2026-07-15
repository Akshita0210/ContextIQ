import streamlit as st

from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.metric_cards import style_metric_cards

from src.services.admin_service import (
    get_all_kbs,
    create_new_kb,
    remove_kb,
    upload_documents,
    get_documents,
    remove_document,
    add_user,
    remove_user,
    get_users,
    logout_user
)

from src.services.rag_service import refresh_pipeline

# ==========================================================
# ADMIN CSS (UI ONLY)
# ==========================================================

def _inject_admin_css():

    st.markdown(
        """
        <style>
            /* ---------- Page background ---------- */
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            .main {
                background: linear-gradient(160deg, #F9FAFB 0%, #F4F5F8 45%, #EFF1F5 100%) !important;
            }

            [data-testid="stHeader"] {
                background: transparent !important;
            }

            .block-container {
                padding-top: 2rem;
                max-width: 1200px;
            }

            /* ---------- Top bar ---------- */
            .admin-topbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.4rem;
            }

            .admin-brand {
                display: flex;
                align-items: center;
                gap: 0.8rem;
            }

            .admin-brand-icon {
                width: 48px;
                height: 48px;
                border-radius: 14px;
                background: linear-gradient(135deg, #7C2D42, #B8763F);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                box-shadow: 0 8px 20px rgba(124, 45, 66, 0.28);
            }

            .admin-page-title {
                font-size: 1.6rem;
                font-weight: 900;
                color: #2B2027;
                margin-bottom: 0;
                line-height: 1.2;
            }

            .admin-page-subtitle {
                font-size: 0.85rem;
                color: #8A7A80;
                margin: 0;
            }

            hr {
                border-top: 1px solid #E9E4E6;
                margin: 1.1rem 0;
            }

            .admin-section-title {
                font-size: 1.1rem;
                font-weight: 800;
                color: #2B2027;
                margin-bottom: 0.15rem;
            }

            .admin-section-subtitle {
                font-size: 0.85rem;
                color: #8A7A80;
                margin-bottom: 1rem;
            }

            /* ---------- Tabs ---------- */
            button[data-baseweb="tab"] {
                font-weight: 700 !important;
                font-size: 0.92rem !important;
                color: #A8949B !important;
            }

            button[data-baseweb="tab"][aria-selected="true"] {
                color: #7C2D42 !important;
            }

            div[data-baseweb="tab-highlight"] {
                background-color: #7C2D42 !important;
            }

            div[data-baseweb="tab-border"] {
                background-color: #E9E4E6 !important;
            }

            /* ---------- Buttons ---------- */
            .stButton button {
                border-radius: 9px;
                font-weight: 600;
            }

            div[data-testid="stButton"] button {
                background: linear-gradient(135deg, #7C2D42, #5C1F30);
                color: #FFFFFF !important;
                border: none;
            }

            div[data-testid="stButton"] button:hover {
                background: linear-gradient(135deg, #B8763F, #7C2D42);
                opacity: 0.96;
            }

            /* ---------- Inputs ---------- */
            div[data-testid="stTextInput"] input,
            div[data-testid="stSelectbox"] > div {
                border-radius: 9px !important;
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: #7C2D42 !important;
                box-shadow: 0 0 0 3px rgba(124, 45, 66, 0.12) !important;
            }

            div[data-testid="stTextInput"] label,
            div[data-testid="stSelectbox"] label {
                font-size: 0.82rem !important;
                font-weight: 600 !important;
                color: #6B5C62 !important;
            }

            /* ---------- File uploader ---------- */
            div[data-testid="stFileUploaderDropzone"] {
                border-radius: 12px !important;
                border: 1.5px dashed #DCC7B0 !important;
                background-color: #FBF8F5 !important;
            }

            /* ---------- List rows ---------- */
            .row-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.65rem 0.3rem;
                border-bottom: 1px solid #EEE8EA;
                color: #2B2027;
                font-size: 0.92rem;
            }

            .row-item:last-child {
                border-bottom: none;
            }

            /* ---------- Badges ---------- */
            .badge-admin {
                background-color: #F3E3D6;
                color: #B8763F;
                font-size: 0.75rem;
                font-weight: 700;
                padding: 3px 12px;
                border-radius: 999px;
                display: inline-block;
                border: 1px solid #E8CDA9;
            }

            .badge-dept {
                background-color: #F3E5E9;
                color: #7C2D42;
                font-size: 0.75rem;
                font-weight: 700;
                padding: 3px 12px;
                border-radius: 999px;
                display: inline-block;
                border: 1px solid #E6D0D7;
            }

            .empty-state {
                text-align: center;
                padding: 2.4rem 1rem;
                color: #B5A2A9;
            }

            .empty-state-icon {
                font-size: 2.1rem;
                margin-bottom: 0.5rem;
            }

            /* ---------- KB pill selector label ---------- */
            .kb-context-label {
                font-size: 0.78rem;
                font-weight: 700;
                color: #A8949B;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.4rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def _card(key):

    return stylable_container(
        key=key,
        css_styles="""
            {
                background-color: #FFFFFF;
                border: 1px solid #EEE8EA;
                border-radius: 16px;
                padding: 1.4rem 1.5rem;
                box-shadow: 0 4px 20px rgba(43, 32, 39, 0.06);
            }
        """
    )


# ==========================================================
# KNOWLEDGE BASE MANAGEMENT
# ==========================================================

def kb_management(embeddings):

    kbs = get_all_kbs()

    # --------------------------------------------------
    # CREATE KB (Always visible)
    # --------------------------------------------------

    with _card("kb_create_card"):

        st.markdown("**+ Create Knowledge Base**")

        new_kb = st.text_input(
            "Knowledge Base Name",
            key="new_kb",
            placeholder="e.g. Finance, HR, Legal"
        )

        if st.button(
            "+  Create Knowledge Base",
            use_container_width=True
        ):

            success, message = create_new_kb(
                new_kb
            )

            if success:

                st.success(message)

                st.rerun()

            else:

                st.error(message)

    st.write("")

    # --------------------------------------------------
    # NO KB EXISTS
    # --------------------------------------------------

    if not kbs:

        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                No Knowledge Bases available.<br>Create one above to get started.
            </div>
            """,
            unsafe_allow_html=True
        )

        return None

    # --------------------------------------------------
    # KB SELECTION
    # --------------------------------------------------

    kb_names = [
        kb["name"]
        for kb in kbs
    ]

    with _card("kb_select_card"):

        st.markdown("**Select Knowledge Base**")

        selected_kb = st.selectbox(
            "Select Knowledge Base",
            kb_names,
            label_visibility="collapsed"
        )

        st.write("")

        if st.button(
            "🗑 Delete Selected Knowledge Base",
            use_container_width=True
        ):

            success, message = remove_kb(
                selected_kb,
                embeddings
            )

            if success:

                st.success(message)

                refresh_pipeline()

                st.rerun()

            else:

                st.error(message)

    return selected_kb

# ==========================================================
# DOCUMENT MANAGEMENT
# ==========================================================

def document_management(
    selected_kb,
    embeddings
):
    # ------------------------------------------------------
    # Upload Documents
    # ------------------------------------------------------

    with _card("doc_upload_card"):

        st.markdown("**Upload Documents**")

        st.markdown(
            f'<p class="admin-section-subtitle">Knowledge Base: <b>{selected_kb}</b></p>',
            unsafe_allow_html=True
        )

        uploaded_files = st.file_uploader(
            "Upload PDF Files",
            type="pdf",
            accept_multiple_files=True,
            key="admin_upload"
        )

        if st.button(
            "Upload Documents",
            use_container_width=True
        ):

            if not uploaded_files:

                st.warning("Please select at least one PDF.")

            else:

                with st.spinner("Uploading and indexing documents..."):

                    results = upload_documents(
                        uploaded_files,
                        selected_kb,
                        embeddings
                    )

                upload_completed = False

                for result in results:

                    if result["status"] == "duplicate":

                        st.warning(
                            f"⚠️ {result['document']['filename']} already exists "
                            f"in {result['document']['kb_name']}."
                        )

                    elif result["status"] == "success":

                        st.success(
                            f"✅ {result['document']['filename']} uploaded successfully."
                        )

                        upload_completed = True

                if upload_completed:

                    refresh_pipeline()

                    st.rerun()

                    st.divider()

    st.write("")

    # ------------------------------------------------------
    # Existing Documents
    # ------------------------------------------------------

    documents = get_documents(
        selected_kb
    )

    with _card("doc_list_card"):

        header_col, count_col = st.columns([4, 1])

        with header_col:

            st.markdown("**Uploaded Documents**")

        with count_col:

            st.markdown(
                f"<span class='badge-dept'>{len(documents)} file"
                f"{'s' if len(documents) != 1 else ''}</span>",
                unsafe_allow_html=True
            )

        if not documents:

            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-state-icon">📄</div>
                    No documents available in this Knowledge Base.
                </div>
                """,
                unsafe_allow_html=True
            )

            return

        st.write("")

        for document in documents:

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"<div class='row-item'>📄 {document['filename']}</div>",
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{document['doc_id']}"
                ):

                    success, message = remove_document(
                        selected_kb,
                        document["doc_id"],
                        embeddings
                    )

                    if success:

                        st.success(
                            "Document deleted successfully."
                        )

                        refresh_pipeline()

                        st.rerun()

                    else:

                        st.error(
                            "Failed to delete document."
                        )

# ==========================================================
# USER MANAGEMENT
# ==========================================================

def user_management():

    with _card("user_create_card"):

        st.markdown("**+ Create User**")

        col_a, col_b = st.columns(2)

        with col_a:

            username = st.text_input(
                "Username",
                key="new_username",
                placeholder="e.g. jdoe"
            )

        with col_b:

            password = st.text_input(
                "Password",
                type="password",
                key="new_password",
                placeholder="••••••••"
            )

        departments = [
            kb["name"]
            for kb in get_all_kbs()
        ]

        if departments:

            department = st.selectbox(
                "Department",
                departments,
                key="department"
            )

            st.write("")

            if st.button(
                "+  Create User",
                use_container_width=True
            ):

                success, message = add_user(
                    username,
                    password,
                    department
                )

                if success:

                    st.success(message)
                    st.rerun()

                else:

                    st.error(message)

        else:

            st.info(
                "Create a Knowledge Base before creating users."
            )

    st.write("")

    users = get_users()

    with _card("user_list_card"):

        header_col, count_col = st.columns([4, 1])

        with header_col:

            st.markdown("**Existing Users**")

        with count_col:

            st.markdown(
                f"<span class='badge-dept'>{len(users)} user"
                f"{'s' if len(users) != 1 else ''}</span>",
                unsafe_allow_html=True
            )

        st.write("")

        admin_found = False

        for user in users:

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:

                st.write(f"👤 {user['username']}")

            with col2:

                if user["role"] == "Admin":

                    admin_found = True

                    st.markdown(
                        "<span class='badge-admin'>Administrator</span>",
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"<span class='badge-dept'>{user['department']}</span>",
                        unsafe_allow_html=True
                    )

            with col3:

                if user["role"] != "Admin":

                    if st.button(
                        "🗑",
                        key=f"user_{user['username']}"
                    ):

                        success, message = remove_user(
                            user["username"]
                        )

                        if success:

                            st.success(message)
                            st.rerun()

                        else:

                            st.error(message)

            st.markdown(
                "<hr style='margin:0.4rem 0; border-color:#EEE8EA;'>",
                unsafe_allow_html=True
            )


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

def admin_dashboard(embeddings):

    _inject_admin_css()

    st.markdown(
        """
        <div class="admin-topbar">
            <div class="admin-brand">
                <div class="admin-brand-icon">🛠</div>
                <div>
                    <p class="admin-page-title">ContextIQ Admin</p>
                    <p class="admin-page-subtitle">Manage Knowledge Bases, Documents and Users</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    kbs_overview = get_all_kbs()
    users_overview = get_users()

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric("Knowledge Bases", len(kbs_overview))

    with m2:

        st.metric("Total Users", len(users_overview))

    with m3:

        admin_count = sum(
            1 for u in users_overview if u["role"] == "Admin"
        )

        st.metric("Administrators", admin_count)

    style_metric_cards(
        background_color="#FFFFFF",
        border_left_color="#7C2D42",
        border_color="#EEE8EA",
        box_shadow=True
    )

    st.write("")

    tab_kb, tab_docs, tab_users = st.tabs(
        ["Knowledge Bases", "Documents", "Users"]
    )

    with tab_kb:

        st.write("")

        kb_management(
            embeddings
        )

    with tab_docs:

        st.write("")

        # --------------------------------------------------
        # Independent KB selector for the Documents tab
        # --------------------------------------------------

        doc_kbs = get_all_kbs()

        if not doc_kbs:

            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-state-icon">🗂</div>
                    Create a Knowledge Base first to manage its documents.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            doc_kb_names = [
                kb["name"]
                for kb in doc_kbs
            ]

            with _card("doc_kb_picker_card"):

                st.markdown("**Choose Knowledge Base**")
                st.write("\n")
                doc_selected_kb = st.selectbox(
                    "Choose Knowledge Base for Documents",
                    doc_kb_names,
                    key="doc_kb_selector",
                    label_visibility="collapsed"
                )

            st.write("")

            document_management(
                doc_selected_kb,
                embeddings
            )

    with tab_users:

        st.write("")

        user_management()

    st.write("")
    st.divider()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        logout_user()