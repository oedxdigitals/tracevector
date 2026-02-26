import sqlite3
import json
from datetime import datetime

from tvx.storage.base import BaseStorage


class SQLiteStorage(BaseStorage):

    def __init__(self, db_path="tracevector.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def init(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            created_at TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            timestamp TEXT,
            scan_json TEXT,
            FOREIGN KEY(case_id) REFERENCES cases(id)
        )
        """)

        self.conn.commit()

    def create_case(self, case_id: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO cases (id, created_at) VALUES (?, ?)",
            (case_id, datetime.utcnow().isoformat())
        )
        self.conn.commit()

    def add_scan(self, case_id: str, scan_data: dict):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO scans (case_id, timestamp, scan_json) VALUES (?, ?, ?)",
            (
                case_id,
                datetime.utcnow().isoformat(),
                json.dumps(scan_data)
            )
        )
        self.conn.commit()

    def get_case(self, case_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
        case = cursor.fetchone()

        cursor.execute("SELECT * FROM scans WHERE case_id = ?", (case_id,))
        scans = cursor.fetchall()

        return {
            "case": dict(case) if case else None,
            "scans": [dict(s) for s in scans]
        }
