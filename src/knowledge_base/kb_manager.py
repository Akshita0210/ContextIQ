import json
import os
import shutil
from pathlib import Path

from src.knowledge_base.registry import (
    load_registry,
    save_registry
)

from src.vectordb.chroma_store import (
    delete_kb_chunks
)

KB_FILE = Path("data/knowledge_bases.json")

RAW_DOCS_DIR = Path("data/raw_docs")


# ==========================================================
# LOAD KNOWLEDGE BASES
# ==========================================================

def load_kbs():

    if not KB_FILE.exists():
        return []

    with open(
        KB_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================================
# SAVE KNOWLEDGE BASES
# ==========================================================

def save_kbs(kbs):

    with open(
        KB_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            kbs,
            f,
            indent=4
        )


# ==========================================================
# CREATE KNOWLEDGE BASE
# ==========================================================

def create_kb(name):

    name = name.strip()

    if not name:
        return False, "Knowledge Base name cannot be empty."

    kbs = load_kbs()

    kb_id = name.lower().replace(" ", "_")

    for kb in kbs:

        if kb["id"] == kb_id:

            return False, "Knowledge Base already exists."

    kbs.append(
        {
            "id": kb_id,
            "name": name
        }
    )

    save_kbs(kbs)

    os.makedirs(
        RAW_DOCS_DIR / name,
        exist_ok=True
    )

    return True, "Knowledge Base created successfully."


# ==========================================================
# DELETE KNOWLEDGE BASE
# ==========================================================

def delete_kb(
    kb_name,
    embeddings
):
    """
    Completely delete a Knowledge Base.
    """

    # ----------------------------------------
    # Delete vectors
    # ----------------------------------------

    delete_kb_chunks(
        kb_name,
        embeddings
    )

    # ----------------------------------------
    # Delete PDFs
    # ----------------------------------------

    kb_folder = RAW_DOCS_DIR / kb_name

    if kb_folder.exists():

        shutil.rmtree(kb_folder)

    # ----------------------------------------
    # Delete registry entries
    # ----------------------------------------

    registry = load_registry()

    if kb_name in registry:

        del registry[kb_name]

        save_registry(
            registry
        )

    # ----------------------------------------
    # Delete KB entry
    # ----------------------------------------

    kbs = load_kbs()

    kbs = [
        kb
        for kb in kbs
        if kb["name"] != kb_name
    ]

    save_kbs(
        kbs
    )

    return (
        True,
        "Knowledge Base deleted successfully."
    )