import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.tracevector_cases.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init():
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            plugin TEXT,
            target TEXT,
            result TEXT,
            risk TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


class Storage:

    def __init__(self):
        _init()

    def create_case(self, case_id):
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cases (id, created_at) VALUES (?, ?)",
            (case_id, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()

    def add_evidence(self, case_id, plugin, target, result, risk):
        conn = _connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO evidence (case_id, plugin, target, result, risk, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                plugin,
                target,
                json.dumps(result),
                json.dumps(risk),
                datetime.utcnow().isoformat()
            )
        )
        conn.commit()
        conn.close()

    def get_case(self, case_id):
        conn = _connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM cases WHERE id=?", (case_id,))
        case = cur.fetchone()

        cur.execute("SELECT * FROM evidence WHERE case_id=?", (case_id,))
        evidence = cur.fetchall()

        conn.close()

        return {
            "case": dict(case) if case else None,
            "evidence": [dict(e) for e in evidence]
        }


def get_storage():
    return Storage()
