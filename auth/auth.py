import hashlib
from database.db import get_connection

# ===============================
# PASSWORD UTILITIES
# ===============================

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    Raw passwords are never stored in the database.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ===============================
# USER AUTHENTICATION
# ===============================

def register_user(username: str, password: str) -> bool:
    """
    Register a new user with a hashed password.

    Returns:
        True  -> registration successful
        False -> username already exists or error occurred
    """
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password)
        )
        conn.commit()
        return True

    except Exception:
        # Covers duplicate username or DB errors
        return False

    finally:
        conn.close()


def login_user(username: str, password: str):
    """
    Authenticate a user.

    Returns:
        user_id (int) if credentials are valid
        None if authentication fails
    """
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hashed_password)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None
