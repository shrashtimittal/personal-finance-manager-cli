import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


def generate_filename(prefix: str) -> str:
    """
    Generate a timestamped filename.
    Example: reports_2025-02-01_14-30-22.csv
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}.csv"


def export_to_csv(
    data: List[Dict],
    columns: List[str],
    filename_prefix: str = "export",
    directory: str = "exports"
) -> Tuple[bool, str]:
    """
    Export list of dictionaries to CSV.

    Args:
        data: list of dict rows
        columns: ordered list of column names
        filename_prefix: prefix for filename
        directory: output directory

    Returns:
        (success, file_path)
    """

    if not data:
        return False, "No data to export."

    try:
        export_dir = Path(directory)
        export_dir.mkdir(exist_ok=True)

        filename = generate_filename(filename_prefix)
        file_path = export_dir / filename

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            for row in data:
                writer.writerow({col: row.get(col, "") for col in columns})

        return True, str(file_path)

    except Exception as e:
        return False, str(e)
