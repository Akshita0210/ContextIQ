from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def build_rag_chain(
    llm,
    retriever,
    contextualize_prompt,
    qa_prompt
):

    history_aware_retriever = (
        create_history_aware_retriever(
            llm,
            retriever,
            contextualize_prompt
        )
    )

    qa_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        qa_chain
    )

    return rag_chain


from langchain_core.runnables.history import RunnableWithMessageHistory
from src.memory.chat_history import get_session_history

def build_conversational_chain(
    rag_chain,
    session_store
):

    conversational_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: get_session_history(
            session_id,
            session_store
        ),
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversational_chain