import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = os.path.join("data", "finance.db")
BACKUP_DIR = os.path.join("data", "backups")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/schema.sql", "r", encoding="utf-8") as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    conn.close()


# ===============================
# BACKUP DATABASE 
# ===============================

def backup_database():
    """
    Create a timestamped backup of the database.
    """
    if not os.path.exists(DB_PATH):
        print("No database found to back up.")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"finance_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_file)

    shutil.copy(DB_PATH, backup_path)
    print(f"Backup created successfully: {backup_path}")


# ===============================
# RESTORE DATABASE 
# ===============================

def restore_database(backup_filename: str):
    """
    Restore the database from a selected backup file.
    """
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    if not os.path.exists(backup_path):
        print("Selected backup file does not exist.")
        return

    confirm = input(
        "⚠️ This will overwrite the current database. Continue? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Restore cancelled.")
        return

    shutil.copy(backup_path, DB_PATH)
    print("Database restored successfully. Restart the application.")
