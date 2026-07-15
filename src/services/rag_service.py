import streamlit as st

from src.llm.groq_client import get_llm
from src.ingestion.embeddings import get_embeddings

from src.vectordb.chroma_store import load_vectorstore
from src.retrieval.retriever import get_retriever

from src.prompts.prompts import (
    get_contextualize_prompt,
    get_qa_prompt
)

from src.chains.rag_chain import build_rag_chain


# ============================================================
# Cached Resources
# ============================================================

@st.cache_resource
def load_embeddings():
    return get_embeddings()


@st.cache_resource
def load_llm():
    return get_llm()


# ============================================================
# Build RAG Pipeline
# ============================================================

@st.cache_resource
def load_rag_pipeline(kb_name):

    embeddings = load_embeddings()

    llm = load_llm()

    # Don't cache this separately.
    # It will be recreated whenever the pipeline cache is cleared.
    vectorstore = load_vectorstore(
        embeddings
    )

    retriever = get_retriever(
        vectorstore,
        kb_name
    )

    contextualize_prompt = get_contextualize_prompt()

    qa_prompt = get_qa_prompt()

    rag_chain = build_rag_chain(
        llm,
        retriever,
        contextualize_prompt,
        qa_prompt
    )

    return {
        "embeddings": embeddings,
        "llm": llm,
        "vectorstore": vectorstore,
        "retriever": retriever,
        "rag_chain": rag_chain
    }


# ============================================================
# Refresh Pipeline
# ============================================================

def refresh_pipeline():

    load_rag_pipeline.clear()