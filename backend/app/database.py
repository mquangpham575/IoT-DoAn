import json
import sqlite3
from typing import Any, Optional

from app.config import settings


def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection with Row factory so query results can be
    converted to dict easily.
    """
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize database tables.

    SQLite is used because it is lightweight and suitable for demo/prototype.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                gas INTEGER NOT NULL,
                light REAL NOT NULL,
                noise INTEGER NOT NULL,
                comfort_level INTEGER NOT NULL,
                status_label TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                reasons TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_sensor_reading(record: dict[str, Any]) -> int:
    """
    Insert one processed sensor reading and return its new ID.
    """
    reasons_json = json.dumps(record.get("reasons", []), ensure_ascii=False)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sensor_readings (
                device_id, temperature, humidity, gas, light, noise,
                comfort_level, status_label, risk_score, reasons,
                recommendation, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["device_id"],
                record["temperature"],
                record["humidity"],
                record["gas"],
                record["light"],
                record["noise"],
                record["comfort_level"],
                record["status_label"],
                record["risk_score"],
                reasons_json,
                record["recommendation"],
                record["created_at"],
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    try:
        item["reasons"] = json.loads(item.get("reasons") or "[]")
    except json.JSONDecodeError:
        item["reasons"] = []
    return item


def get_latest_reading() -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sensor_readings
            ORDER BY id DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        return _row_to_dict(row) if row else None


def get_reading_history(limit: int = 50) -> list[dict[str, Any]]:
    safe_limit = max(1, min(limit, 500))

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM sensor_readings
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        )
        return [_row_to_dict(row) for row in cursor.fetchall()]
