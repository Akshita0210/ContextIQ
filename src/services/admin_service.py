from src.knowledge_base.kb_manager import (
    create_kb,
    delete_kb,
    load_kbs
)

from src.knowledge_base.ingestion_manager import (
    process_uploaded_file
)

from src.knowledge_base.registry import (
    list_documents
)

from src.knowledge_base.delete import (
    delete_document
)

from src.auth.auth_manager import (
    create_user,
    delete_user,
    get_all_users
)


# ==========================================================
# KNOWLEDGE BASE
# ==========================================================

def create_new_kb(kb_name):
    return create_kb(kb_name)


def remove_kb(kb_name, embeddings):
    return delete_kb(kb_name, embeddings)


def get_all_kbs():
    return load_kbs()


# ==========================================================
# DOCUMENTS
# ==========================================================

def upload_document(
    uploaded_file,
    kb_name,
    embeddings
):
    return process_uploaded_file(
        uploaded_file,
        kb_name,
        embeddings
    )


def get_documents(kb_name):
    return list_documents(kb_name)


def remove_document(
    kb_name,
    doc_id,
    embeddings
):

    success = delete_document(
        kb_name,
        doc_id,
        embeddings
    )

    if success:
        return True, "Document deleted successfully."

    return False, "Unable to delete document."


# ==========================================================
# USERS
# ==========================================================

def add_user(
    username,
    password,
    department
):
    return create_user(
        username,
        password,
        department
    )


def remove_user(username):
    return delete_user(username)


def get_users():
    return get_all_users()


def upload_documents(
    uploaded_files,
    kb_name,
    embeddings
):
    results = []

    for uploaded_file in uploaded_files:
        result = upload_document(
            uploaded_file,
            kb_name,
            embeddings
        )
        results.append(result)

    return results

from src.auth.login import logout


# ==========================================================
# SESSION
# ==========================================================

def logout_user():
    logout()