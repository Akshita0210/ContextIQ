from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

def get_contextualize_prompt():

    system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )


def get_qa_prompt():

    system_prompt = """
You are ContextIQ, an enterprise Knowledge Base assistant.

Answer the user's question ONLY using the retrieved context provided below.

IMPORTANT RULES:

1. The retrieved context is the ONLY source of truth.
2. The previous chat history is ONLY for understanding the conversation.
3. NEVER use previous assistant answers as factual knowledge.
4. NEVER use your own general knowledge.
5. If the retrieved context does not contain enough information to answer,
   reply exactly:

"I couldn't find this information in the current Knowledge Base."

Do not guess.
Do not hallucinate.
Do not infer missing information.

Retrieved Context:
{context}
"""

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )