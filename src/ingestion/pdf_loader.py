# from turtle import st

# from langchain_community.document_loaders import PyPDFLoader

# def load_uploaded_pdfs(uploaded_files):

#     documents = []

#     for uploaded_file in uploaded_files:

#         temp_pdf = f"./{uploaded_file.name}"

#         with open(temp_pdf, "wb") as f:
#             f.write(uploaded_file.getvalue())

#         loader = PyPDFLoader(temp_pdf)

#         docs = loader.load()

#         documents.extend(docs)

#     return documents


############### PHASE 3 ###############

import os

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(uploaded_file, kb_name):
    """
    Save one uploaded PDF and return its LangChain documents
    along with the saved file path.
    """

    kb_folder = os.path.join(
        "data",
        "raw_docs",
        kb_name
    )

    os.makedirs(kb_folder, exist_ok=True)

    pdf_path = os.path.join(
        kb_folder,
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    for doc in documents:
        doc.metadata["kb_id"] = kb_name
        doc.metadata["file_path"] = pdf_path

    return documents, pdf_path