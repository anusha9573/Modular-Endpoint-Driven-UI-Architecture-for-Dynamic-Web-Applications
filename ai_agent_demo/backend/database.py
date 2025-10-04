import sqlite3
from typing import List, Tuple
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brief TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brief_id INTEGER,
            task TEXT NOT NULL,
            FOREIGN KEY(brief_id) REFERENCES briefs(id)
        )
        """
    )
    conn.commit()
    conn.close()


def save_brief_and_tasks(brief: str, tasks: List[str]) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO briefs (brief) VALUES (?)", (brief,))
    brief_id = cur.lastrowid
    cur.executemany("INSERT INTO tasks (brief_id, task) VALUES (?, ?)", [(brief_id, t) for t in tasks])
    conn.commit()
    conn.close()
    return brief_id


def get_tasks_for_brief(brief_id: int) -> List[Tuple[int, str]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, task FROM tasks WHERE brief_id = ?", (brief_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
