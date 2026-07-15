import streamlit as st
import os
import json
from pathlib import Path


# ==========================================================
# CHAT SESSION MANAGEMENT
# ==========================================================

def initialize_chat_sessions():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {
            "chat_1": []
        }
        st.session_state.current_chat = "chat_1"


def create_new_chat(username):
    """
    Create a new chat for the user and update index.json.
    """

    index = load_chat_index(username)

    chats = index["chats"]

    if chats:

        max_number = max(
            int(chat["id"].split("_")[1])
            for chat in chats
        )

        new_chat = f"chat_{max_number + 1}"

    else:

        new_chat = "chat_1"

    chats.insert(
        0,
        {
            "id": new_chat,
            "title": f"Chat {new_chat.split('_')[1]}"
        }
    )

    index["current_chat"] = new_chat

    save_chat_index(
        username,
        index
    )

    st.session_state.chat_sessions[new_chat] = []

    st.session_state.current_chat = new_chat

    return new_chat


# ==========================================================
# CHAT HISTORY STORAGE
# ==========================================================

CHAT_DIR = "data/chat_history"

os.makedirs(
    CHAT_DIR,
    exist_ok=True
)


# ==========================================================
# SAVE CHAT HISTORY
# ==========================================================

def save_chat_history(
    username,
    session_id,
    messages
):

    user_folder = os.path.join(
        CHAT_DIR,
        username
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    filepath = os.path.join(
        user_folder,
        f"{session_id}.json"
    )

    data = []

    for msg in messages:

        data.append(
            {
                "type": msg.type,
                "content": msg.content
            }
        )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ==========================================================
# LOAD CHAT HISTORY
# ==========================================================

def load_chat_history(
    username,
    session_id
):

    user_folder = os.path.join(
        CHAT_DIR,
        username
    )

    filepath = os.path.join(
        user_folder,
        f"{session_id}.json"
    )

    if not os.path.exists(filepath):

        return []

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
    
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


def restore_user_sessions(
    username,
    session_store
):
    
    """
    Restore user's chat sessions from index.json.
    """

    if st.session_state.get("sessions_restored", False):
        return

    st.session_state.sessions_restored = True

    index = load_chat_index(username)

    st.session_state.chat_sessions = {}

    for chat in index["chats"]:

        session_id = chat["id"]

        st.session_state.chat_sessions[session_id] = []

        history = ChatMessageHistory()

        messages = load_chat_history(
            username,
            session_id
        )

        for msg in messages:

            if msg["type"] == "human":

                history.add_message(
                    HumanMessage(
                        content=msg["content"]
                    )
                )

            elif msg["type"] == "ai":

                history.add_message(
                    AIMessage(
                        content=msg["content"]
                    )
                )

        session_store[session_id] = history

    st.session_state.current_chat = index["current_chat"]


# ==========================================================
# CHAT INDEX
# ==========================================================
def get_user_folder(username):

    user_folder = Path(CHAT_DIR) / username
    user_folder.mkdir(parents=True,exist_ok=True)
    return user_folder

def load_chat_index(username):
    """
    Load index.json for a user.
    """
    user_folder = get_user_folder(username)
    print(user_folder)
    index_file = user_folder / "index.json"
    if not index_file.exists():
        index = {
            "current_chat": "chat_1",
            "chats": [
                {
                    "id": "chat_1",
                    "title": "Chat 1"
                }
            ]
        }

        with open(index_file,"w",encoding="utf-8") as f:
            json.dump(
                index,
                f,
                indent=4
            )
        return index

    with open(index_file,"r",encoding="utf-8") as f:
        return json.load(f)


def save_chat_index(username,index):
    """
    Save index.json.
    """
    user_folder = get_user_folder(username)
    index_file = user_folder / "index.json"
    with open(index_file,"w",encoding="utf-8") as f:
        json.dump(
            index,
            f,
            indent=4
        )


# ==========================================================
# RENAME CHAT
# ==========================================================
def rename_chat(
    username,
    chat_id,
    new_title
):

    index = load_chat_index(
        username
    )

    for chat in index["chats"]:

        if chat["id"] == chat_id:

            chat["title"] = new_title
            break

    save_chat_index(
        username,
        index
    )

# ==========================================================
# DELETE CHAT
# ==========================================================
def delete_chat(
    username,
    chat_id,
    session_store
):
    """
    Delete a chat.

    If it is the last remaining chat,
    reset everything back to Chat 1.
    """

    index = load_chat_index(username)

    user_folder = get_user_folder(username)

    # =====================================================
    # CASE 1 : Only one chat remains
    # =====================================================

    if len(index["chats"]) == 1:

        # Delete old chat history file
        old_chat_file = user_folder / f"{chat_id}.json"

        if old_chat_file.exists():
            os.remove(old_chat_file)

        # Remove from memory
        if chat_id in session_store:
            del session_store[chat_id]

        if chat_id in st.session_state.chat_sessions:
            del st.session_state.chat_sessions[chat_id]

        # Reset to Chat 1
        new_chat_id = "chat_1"

        index["current_chat"] = new_chat_id

        index["chats"] = [
            {
                "id": new_chat_id,
                "title": "Chat 1"
            }
        ]

        save_chat_index(
            username,
            index
        )

        st.session_state.chat_sessions = {
            new_chat_id: []
        }

        session_store[new_chat_id] = ChatMessageHistory()

        st.session_state.current_chat = new_chat_id

        return

    # =====================================================
    # CASE 2 : More than one chat exists
    # =====================================================

    # Delete chat history file
    chat_file = user_folder / f"{chat_id}.json"

    if chat_file.exists():
        os.remove(chat_file)

    # Remove from memory
    if chat_id in session_store:
        del session_store[chat_id]

    if chat_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[chat_id]

    # Remove from index.json
    index["chats"] = [
        chat
        for chat in index["chats"]
        if chat["id"] != chat_id
    ]

    # If deleted chat was active,
    # switch to the newest remaining chat.
    if index["current_chat"] == chat_id:

        new_current_chat = index["chats"][0]["id"]

        index["current_chat"] = new_current_chat

        st.session_state.current_chat = new_current_chat

    # Save changes
    save_chat_index(
        username,
        index
    )