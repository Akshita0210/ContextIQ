import os
from langchain_chroma import Chroma

VECTOR_DB_PATH = "data/vector_db"


def create_vectorstore(documents, embeddings):

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    return vectorstore


def load_vectorstore(embeddings):

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )


def vector_db_exists():

    return (
        os.path.exists(VECTOR_DB_PATH)
        and len(os.listdir(VECTOR_DB_PATH)) > 0
    )


def delete_document_chunks(doc_id, embeddings):
    """
    Delete all chunks belonging to a document.
    """

    vectorstore = load_vectorstore(embeddings)

    vectorstore.delete(
        where={
            "doc_id": doc_id
        }
    )

def delete_kb_chunks(
    kb_name,
    embeddings
):
    """
    Delete every chunk belonging to a Knowledge Base.
    """

    vectorstore = load_vectorstore(
        embeddings
    )

    vectorstore.delete(
        where={
            "kb_id": kb_name
        }
    )