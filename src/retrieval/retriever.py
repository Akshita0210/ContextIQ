def get_retriever(vectorstore, kb_id):
    return vectorstore.as_retriever(
        search_kwargs={
            "k": 3,     # default value is 4 if not mentioned
            "filter": {
                "kb_id": kb_id
            }
        }
    )