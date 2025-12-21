import os
import sqlite3
import pytest
from database.db import initialize_database, DB_PATH

TEST_DB = "data/test_finance.db"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create a fresh test database before tests,
    and delete it after all tests finish.
    """
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    # Temporarily override DB_PATH
    original_path = DB_PATH
    from database import db
    db.DB_PATH = TEST_DB

    initialize_database()

    yield  # run tests

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    db.DB_PATH = original_path
