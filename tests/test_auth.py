from auth.auth import register_user, login_user
from database.db import initialize_database

def test_user_registration_and_login():
    initialize_database()

    username = "test_user"
    password = "test_pass"

    assert register_user(username, password) is True
    user_id = login_user(username, password)

    assert user_id is not None
