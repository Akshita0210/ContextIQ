import json
import os
import uuid

REGISTRY_PATH = "data/document_registry.json"

def load_registry():
    """
    Load the document registry.
    """

    if not os.path.exists(REGISTRY_PATH):
        return {}

    with open(REGISTRY_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_registry(registry):
    """
    Save the registry to disk.
    """

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)


def register_document(
    kb_name,
    metadata,
    file_hash,
    chunk_count,
    doc_id
):
    """
    Register a newly indexed document.
    """

    registry = load_registry()

    if kb_name not in registry:
        registry[kb_name] = []

    document = {
        "doc_id": doc_id,
        "filename": metadata["filename"],
        "file_path": metadata["file_path"],
        "pages": metadata["pages"],
        "file_size": metadata["file_size"],
        "uploaded_at": metadata["uploaded_at"],
        "hash": file_hash,
        "chunks": chunk_count
    }

    registry[kb_name].append(document)

    save_registry(registry)


def document_exists(file_hash):
    """
    Check if a document with the given hash already exists.

    Args:
        file_hash (str): SHA-256 hash of the document.

    Returns:
        dict | None:
            Returns the document metadata if found,
            otherwise returns None.
    """

    registry = load_registry()

    for kb_name, documents in registry.items():

        for document in documents:

            if document["hash"] == file_hash:
                return {
                    "kb_name": kb_name,
                    **document
                }

    return None


def list_documents(kb_name):
    """
    Return all documents inside a KB.
    """

    registry = load_registry()

    return registry.get(kb_name, [])



def get_document(kb_name, doc_id):
    """
    Return a document from the registry.
    """

    registry = load_registry()

    if kb_name not in registry:
        return None

    for document in registry[kb_name]:

        if document["doc_id"] == doc_id:
            return document

    return None