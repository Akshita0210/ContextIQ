import os
import json

from src.vectordb.chroma_store import load_vectorstore
from src.knowledge_base.registry import (
    load_registry,
    save_registry
)


def delete_document(
    kb_name,
    doc_id,
    embeddings
):
    """
    Delete a document completely.

    Steps:
    1. Delete all vectors from Chroma.
    2. Delete the PDF file.
    3. Remove the document from the registry.
    """

    registry = load_registry()

    if kb_name not in registry:
        return False

    document_to_delete = None

    for document in registry[kb_name]:

        if document["doc_id"] == doc_id:
            document_to_delete = document
            break

    if document_to_delete is None:
        return False

    # -----------------------------------
    # Delete vectors from Chroma
    # -----------------------------------

    vectorstore = load_vectorstore(embeddings)

    print("=" * 60)
    print("BEFORE DELETE")
    print(vectorstore.get(
        where={
            "doc_id": doc_id
        }
    ))
    print("=" * 60)

    vectorstore.delete(
        where={
            "doc_id": doc_id
        }
    )

    print("=" * 60)
    print("AFTER DELETE")
    print(vectorstore.get(
        where={
            "doc_id": doc_id
        }
    ))
    print("=" * 60)

    # -----------------------------------
    # Delete physical PDF
    # -----------------------------------

    file_path = document_to_delete["file_path"]

    if os.path.exists(file_path):
        os.remove(file_path)

    # -----------------------------------
    # Remove from registry
    # -----------------------------------

    registry[kb_name] = [
        doc
        for doc in registry[kb_name]
        if doc["doc_id"] != doc_id
    ]

    save_registry(registry)

    return True