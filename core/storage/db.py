import sqlite3
import json
import time

DB_PATH = "signalhire.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id TEXT PRIMARY KEY,
        created_at REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        candidate_id TEXT,
        task_name TEXT,
        start_time REAL,
        end_time REAL,
        summary TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        timestamp REAL,
        event_type TEXT,
        phase TEXT,
        passed INTEGER,
        tests_passed INTEGER,
        diff TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_candidate(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO candidates VALUES (?, ?)",
        (candidate_id, time.time())
    )

    conn.commit()
    conn.close()


def save_session(session):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
        (
            session["session_id"],
            session["candidate_id"],
            session["task_name"],
            session["start_time"],
            session["end_time"],
            json.dumps(session["summary"])
        )
    )

    conn.commit()
    conn.close()


def save_events(events):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for e in events:
        cur.execute(
            "INSERT INTO events (session_id, timestamp, event_type, phase, passed, tests_passed, diff) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                e.get("session_id"),
                e.get("timestamp"),
                e.get("event_type"),
                e.get("phase"),
                int(e.get("passed")) if e.get("passed") is not None else None,
                e.get("tests_passed"),
                json.dumps(e.get("diff"))
            )
        )

    conn.commit()
    conn.close()