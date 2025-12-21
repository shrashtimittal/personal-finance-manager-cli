from auth.auth import register_user, login_user

def test_user_registration_and_login():
    username = "testuser"
    password = "testpass"

    # Register
    assert register_user(username, password) is True

    # Duplicate registration should fail
    assert register_user(username, password) is False

    # Login should succeed
    user_id = login_user(username, password)
    assert user_id is not None

    # Wrong password should fail
    assert login_user(username, "wrongpass") is None

