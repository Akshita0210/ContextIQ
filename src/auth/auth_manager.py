import os
import json
import bcrypt
import shutil
from pathlib import Path
USERS_FILE = "data/users.json"


# ==========================================================
# USER FILE
# ==========================================================

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE,"r",encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE,"w",encoding="utf-8") as f:
        json.dump(users,f,indent=4)


# ==========================================================
# PASSWORD
# ==========================================================

def hash_password(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(),hashed_password.encode())


# ==========================================================
# LOGIN
# ==========================================================

def authenticate(username, password):

    users = load_users()

    if username not in users:
        return None

    user = users[username]

    if verify_password(password,user["password"]):
        return {
            "username": username,
            "role": user["role"],
            "department": user["department"]
        }

    return None


# ==========================================================
# CREATE USER
# ==========================================================

def create_user(username,password,department):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "password": hash_password(password),
        "role": "User",
        "department": department

    }

    save_users(users)
    return True, "User created successfully."


# ==========================================================
# DELETE USER
# ==========================================================

def delete_user(username):

    users = load_users()

    if username == "admin":
        return False, "Admin cannot be deleted."

    if username not in users:
        return False, "User not found."

    # =====================================================
    # Delete user's chat history folder
    # =====================================================

    chat_folder = Path(
        "data/chat_history"
    ) / username

    if chat_folder.exists():

        shutil.rmtree(
            chat_folder
        )

    # =====================================================
    # Delete user
    # =====================================================

    del users[username]

    save_users(users)

    return (
        True,
        "User deleted successfully."
    )


# ==========================================================
# GET USERS
# ==========================================================

def get_all_users():
    users = load_users()
    result = []
    for username, info in users.items():
        result.append(
            {
                "username": username,
                "role": info["role"],
                "department": info["department"]
            }
        )
    return result