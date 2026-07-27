import os

import streamlit as st


def _inject_chat_css():

    st.markdown(
        """
        <style>
            /* ---------- Chat area background (lighter tint) ---------- */
            [data-testid="stAppViewContainer"],
            [data-testid="stMain"],
            section.main,
            .main {
                background: linear-gradient(180deg, #F5F7FF 0%, #EBEFFC 100%) !important;
            }

            [data-testid="stHeader"] {
                background: transparent !important;
            }

            .block-container {
                padding-top: 2rem;
            }

            hr {
                border-top: 1px solid #E0E5F2;
                margin: 0.8rem 0 1.2rem 0;
            }
        

            /* ---------- Chat messages ---------- */
            div[data-testid="stChatMessage"] {
                border-radius: 16px;
                padding: 0.55rem 0.8rem;
                margin-bottom: 0.55rem;
                box-shadow: 0 1px 3px rgba(30, 41, 59, 0.05);
            }

            div[data-testid="stChatMessageContent"] p {
                font-size: 0.96rem;
                line-height: 1.6;
                color: #1E293B;
            }

            /* User bubble — indigo family */
            div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
                background: linear-gradient(135deg, #E8ECFC 0%, #DCE4FA 100%);
                border: 1px solid #CBD5F5;
            }

            div[data-testid="stChatMessageAvatarUser"] {
                background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
            }

            /* Assistant bubble — teal family */
            div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
                background: linear-gradient(135deg, #E5FBF7 0%, #DFF6F2 100%);
                border: 1px solid #BFEDE3;
            }

            div[data-testid="stChatMessageAvatarAssistant"] {
                background: linear-gradient(135deg, #0D9488, #14B8A6) !important;
            }

            /* ---------- Chat input ---------- */
            div[data-testid="stChatInput"] textarea {
                border-radius: 16px !important;
                border: 1.5px solid #D6DCF2 !important;
                background-color: #FFFFFF !important;
            }

            div[data-testid="stChatInput"]:focus-within {
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
                border-radius: 16px;
            }

            /* ---------- Sources ---------- */
            .sources-label {
                font-size: 0.75rem;
                font-weight: 700;
                color: #0D9488;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.4rem;
            }

            .source-chip {
                display: inline-block;
                background: linear-gradient(135deg, #E5FBF7 0%, #EEF2FF 100%);
                color: #1E293B;
                border: 1px solid #CBD5F5;
                border-radius: 999px;
                padding: 4px 13px;
                margin: 3px 6px 3px 0;
                font-size: 0.78rem;
                font-weight: 500;
            }

            /* ---------- Empty state ---------- */
            .chat-welcome {
                text-align: center;
                padding: 3.5rem 1rem 2.2rem 1rem;
            }

            .chat-welcome-icon-wrap {
                width: 68px;
                height: 68px;
                margin: 0 auto 1rem auto;
                border-radius: 20px;
                background: linear-gradient(135deg, #4F46E5 0%, #0D9488 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.9rem;
                box-shadow: 0 8px 24px rgba(79, 70, 229, 0.22);
            }

            .chat-welcome-title {
                font-size: 1.4rem;
                font-weight: 800;
                color: #111827;
                margin-bottom: 0.4rem;
            }

            .chat-welcome-subtitle {
                font-size: 0.92rem;
                color: #64748B;
                max-width: 440px;
                margin: 0 auto;
                line-height: 1.55;
            }

            .chat-welcome-pills {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                margin-top: 1.3rem;
                flex-wrap: wrap;
            }

            .chat-welcome-pill {
                background: #FFFFFF;
                border: 1px solid #DDE3F5;
                border-radius: 999px;
                padding: 6px 16px;
                font-size: 0.8rem;
                color: #3730A3;
                box-shadow: 0 1px 2px rgba(30, 41, 59, 0.04);
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def user_dashboard(user):
    """
    Render the user dashboard.

    Parameters
    ----------
    user : dict
        Logged in user information.

    Returns
    -------
    str | None
        User question if asked.
    """

    _inject_chat_css()

    department = user["department"]

    user_query = st.chat_input(
        f"Ask anything about {department}"
    )

    return user_query

def display_chat_history(history):
    """
    Display previous chat messages.
    """

    if history is None:

        st.markdown(
            """
            <div class="chat-welcome">
                <div class="chat-welcome-icon-wrap">✨</div>
                <div class="chat-welcome-title">Ask me anything</div>
                <div class="chat-welcome-subtitle">
                    I can answer questions using your department's knowledge base —
                    just start typing below to begin the conversation.
                </div>
                <div class="chat-welcome-pills">
                    <span class="chat-welcome-pill">Policy questions</span>
                    <span class="chat-welcome-pill">Data lookups</span>
                    <span class="chat-welcome-pill">Document search</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    if not history.messages:

        st.markdown(
            """
            <div class="chat-welcome">
                <div class="chat-welcome-icon-wrap">✨</div>
                <div class="chat-welcome-title">Ask me anything</div>
                <div class="chat-welcome-subtitle">
                    I can answer questions using your department's knowledge base —
                    just start typing below to begin the conversation.
                </div>
                <div class="chat-welcome-pills">
                    <span class="chat-welcome-pill"> Policy questions</span>
                    <span class="chat-welcome-pill"> Data lookups</span>
                    <span class="chat-welcome-pill"> Document search</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    for message in history.messages:

        if message.type == "human":

            with st.chat_message("user"):

                st.write(message.content)

        elif message.type == "ai":

            with st.chat_message("assistant"):

                st.write(message.content)




import re


# def filter_relevant_sources(answer, context, max_sources=2):
#     """
#     Filter retrieved documents and keep only the most relevant ones.
#     """

#     if not context:
#         return []

#     answer_lower = answer.lower()

#     scored_docs = []

#     for doc in context:

#         text = doc.page_content.lower()

#         # Split into sentences
#         sentences = re.split(r"[.!?]\s+", text)

#         score = 0

#         for sentence in sentences:

#             sentence = sentence.strip()

#             if len(sentence) < 25:
#                 continue

#             if sentence in answer_lower:
#                 score += 3

#             else:
#                 # Count overlapping keywords
#                 overlap = sum(
#                     1
#                     for word in sentence.split()
#                     if len(word) > 4 and word in answer_lower
#                 )

#                 score += overlap

#         scored_docs.append((score, doc))

#     scored_docs.sort(key=lambda x: x[0], reverse=True)

#     return [doc for score, doc in scored_docs[:max_sources]]
from difflib import SequenceMatcher


def filter_relevant_sources(answer, context, max_sources=1):
    """
    Return only the document that best matches the generated answer.
    """

    if not context:
        return []

    answer = answer.lower()

    scored = []

    for doc in context:

        best_score = 0

        sentences = re.split(r"[.!?]\s+", doc.page_content)

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 20:
                continue

            similarity = SequenceMatcher(
                None,
                answer,
                sentence.lower()
            ).ratio()

            best_score = max(best_score, similarity)

        scored.append((best_score, doc))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [scored[0][1]]
def display_sources(context):

    if not context:
        return

    sources = set()

    for doc in context:

        source = os.path.basename(
            doc.metadata.get(
                "source",
                "Unknown"
            )
        )

        page = doc.metadata.get(
            "page",
            0
        )

        sources.add(
            f"{source} (Page {page + 1})"
        )

    if sources:

        st.write("")

        st.markdown(
            '<div class="sources-label">Sources</div>',
            unsafe_allow_html=True
        )

        chips_html = "".join(
            f'<span class="source-chip">📄 {source}</span>'
            for source in sorted(sources)
        )

        st.markdown(
            chips_html,
            unsafe_allow_html=True
        )

