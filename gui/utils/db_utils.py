import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple


# ===============================
# CONFIG
# ===============================

# Adjust if your DB filename is different
DB_FILENAME = "finance.db"

# Default backup directory
BACKUP_DIR = Path("backups")


# ===============================
# BACKUP DATABASE
# ===============================

def backup_database() -> Tuple[bool, str]:
    """
    Create a timestamped backup of the database.
    Returns (success, message_or_path).
    """
    db_path = Path(DB_FILENAME)

    if not db_path.exists():
        return False, "Database file not found."

    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"finance_backup_{timestamp}.db"

    try:
        shutil.copy2(db_path, backup_file)
        return True, str(backup_file)
    except Exception as e:
        return False, str(e)


# ===============================
# RESTORE DATABASE
# ===============================

def restore_database(backup_path: str) -> Tuple[bool, str]:
    """
    Restore database from a backup file.
    Returns (success, message).
    """
    backup_file = Path(backup_path)
    db_path = Path(DB_FILENAME)

    if not backup_file.exists():
        return False, "Backup file not found."

    try:
        shutil.copy2(backup_file, db_path)
        return True, "Database restored successfully."
    except Exception as e:
        return False, str(e)
