import csv
from typing import List, Dict
from datetime import datetime
import os

REQUIRED_GENERATED_FIELDS = [
    "day",
    "exercise",
    "sets",
    "reps",
    "rest_seconds",
    "notes",
]

REQUIRED_REVIEW_FIELDS = [
    "day",
    "exercise",
    "sets",
    "reps",
]


def read_csv(path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns a list of rows as dicts.
    """
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(path: str, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """
    Writes rows to CSV with strict column order.
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate_columns(rows: List[Dict[str, str]], required_fields: List[str]) -> bool:
    """
    Ensures all required columns exist.
    """
    if not rows:
        raise ValueError("CSV is empty.")

    headers = rows[0].keys()
    missing = [f for f in required_fields if f not in headers]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return True


def validate_numeric_fields(rows: List[Dict[str, str]], fields: List[str]) -> None:
    """
    Ensures specified fields contain valid positive integers.
    """
    for i, row in enumerate(rows, start=1):
        for field in fields:
            value = row.get(field, "").strip()
            if not value.isdigit() or int(value) <= 0:
                raise ValueError(
                    f"Invalid value in row {i} for '{field}': '{value}'"
                )


def validate_generated_tt(rows: List[Dict[str, str]]) -> None:
    """
    Validation for AI-generated training templates.
    """
    validate_columns(rows, REQUIRED_GENERATED_FIELDS)
    validate_numeric_fields(rows, ["sets", "reps", "rest_seconds"])


def validate_review_tt(rows: List[Dict[str, str]]) -> None:
    """
    Validation for user-provided training templates.
    """
    validate_columns(rows, REQUIRED_REVIEW_FIELDS)
    validate_numeric_fields(rows, ["sets", "reps"])

def log_daily_health(weight: float, sleep_hours: float, calories_in: int, workout_done: bool, notes: str = "") -> bool:
    """
    Appends a daily health snapshot to a local CSV file.
    """
    file_path = "data/health_log.csv"
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        headers = ["date", "weight", "sleep_hours", "calories_in", "workout_done", "notes"]
        writer = csv.DictWriter(f, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "weight": weight,
            "sleep_hours": sleep_hours,
            "calories_in": calories_in,
            "workout_done": workout_done,
            "notes": notes
        })
    return True
