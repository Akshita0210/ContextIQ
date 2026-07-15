from src.auth.auth_manager import load_users, save_users, hash_password

users = load_users()

users["admin"] = {
    "password": hash_password("admin123"),
    "role": "Admin",
    "department": None
}

save_users(users)

print("Admin created successfully.")