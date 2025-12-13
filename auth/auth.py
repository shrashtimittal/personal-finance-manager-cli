import sqlite3
import hashlib
from database.db import get_connection


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, hashed_pw)
    )

    user = cursor.fetchone()
    conn.close()

    return user[0] if user else None

