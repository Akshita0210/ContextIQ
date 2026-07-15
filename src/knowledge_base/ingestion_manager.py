import uuid

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.splitter import split_documents

from src.knowledge_base.metadata import extract_metadata

from src.knowledge_base.duplicate import (
    compute_file_hash,
    compute_uploaded_file_hash
)

from src.knowledge_base.registry import (
    document_exists,
    register_document
)

from src.vectordb.chroma_store import (
    create_vectorstore,
    load_vectorstore,
    vector_db_exists
)


def process_uploaded_file(
    uploaded_file,
    kb_name,
    embeddings
):
    """
    Process one uploaded PDF completely.
    """

    # --------------------------
    # Duplicate Detection FIRST
    # --------------------------

    file_hash = compute_uploaded_file_hash(uploaded_file)

    existing_doc = document_exists(file_hash)

    if existing_doc:

        return {
            "status": "duplicate",
            "document": existing_doc
        }

    # --------------------------
    # Load PDF only if new
    # --------------------------

    documents, pdf_path = load_pdf(
        uploaded_file,
        kb_name
    )

    metadata = extract_metadata(pdf_path)

    # --------------------------
    # Generate unique document id
    # --------------------------

    doc_id = str(uuid.uuid4())

    # --------------------------
    # Split
    # --------------------------

    splits = split_documents(documents)

    for split in splits:

        split.metadata["kb_id"] = kb_name
        split.metadata["doc_id"] = doc_id

    # --------------------------
    # Store in Chroma
    # --------------------------

    if vector_db_exists():

        vectorstore = load_vectorstore(embeddings)
        vectorstore.add_documents(splits)
        print("=" * 60)
        print("Stored Metadata")
        print(splits[0].metadata)
        print("=" * 60)

    else:
        print("=" * 60)
        print("Stored Metadata")
        print(splits[0].metadata)
        print("=" * 60)

        vectorstore = create_vectorstore(
            splits,
            embeddings
        )

    # --------------------------
    # Register document
    # --------------------------

    register_document(
        kb_name=kb_name,
        metadata=metadata,
        file_hash=file_hash,
        chunk_count=len(splits),
        doc_id=doc_id
    )

    return {
    "status": "success",
    "document": {
        "filename": metadata["filename"],
        "doc_id": doc_id,
        "kb_name": kb_name,
        "chunk_count": len(splits)
    }
}