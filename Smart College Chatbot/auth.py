"""
SmartCollegeBot - Authentication Module
Admin login + Student access with session management
"""

import hashlib
import json
import os
from datetime import datetime

# ─── USER DATABASE (file-based for demo) ──────────────────────────────────────

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

DEFAULT_USERS = {
    "admin": {
        "password": _hash_password("admin123"),
        "role": "admin",
        "name": "Administrator",
        "email": "admin@smartcollegebot.in",
        "created_at": "2024-01-01"
    },
    "student1": {
        "password": _hash_password("student123"),
        "role": "student",
        "name": "Komal Anand",
        "email": "komal@college.in",
        "created_at": "2024-01-01"
    },
    "demo": {
        "password": _hash_password("demo123"),
        "role": "student",
        "name": "Demo User",
        "email": "demo@college.in",
        "created_at": "2024-01-01"
    }
}

def _load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    # Create default users
    _save_users(DEFAULT_USERS)
    return DEFAULT_USERS

def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def authenticate(username: str, password: str):
    """
    Returns user dict if authentication succeeds, None otherwise.
    """
    users = _load_users()
    username = username.strip().lower()
    if username in users:
        if users[username]["password"] == _hash_password(password):
            user = users[username].copy()
            user["username"] = username
            return user
    return None

def register_user(username: str, password: str, name: str, email: str = "", role: str = "student"):
    """Register a new user. Returns (success: bool, message: str)."""
    users = _load_users()
    username = username.strip().lower()
    name = name.strip()
    
    if len(username) < 3:
        return False, "Name must be at least 3 characters."
    if not name:
        return False, "Please enter your name."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if username in users:
        return False, "An account with this name already exists. Please login or use a different name."
    if email and "@" not in email:
        return False, "Please enter a valid email address."
    
    users[username] = {
        "password": _hash_password(password),
        "role": role,
        "name": name,
        "email": email.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    _save_users(users)
    return True, "Account created successfully! You can now login."

def get_all_users():
    """Admin function: get all users (without passwords)."""
    users = _load_users()
    safe = {}
    for uname, data in users.items():
        safe[uname] = {k: v for k, v in data.items() if k != "password"}
    return safe

def delete_user(username: str):
    """Admin: delete a user."""
    users = _load_users()
    if username == "admin":
        return False, "Cannot delete the admin account."
    if username not in users:
        return False, "User not found."
    del users[username]
    _save_users(users)
    return True, f"User '{username}' deleted."

def reset_password(username: str, new_password: str):
    """Admin: reset a user's password."""
    users = _load_users()
    if username not in users:
        return False, "User not found."
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."
    users[username]["password"] = _hash_password(new_password)
    _save_users(users)
    return True, f"Password for '{username}' reset successfully."
