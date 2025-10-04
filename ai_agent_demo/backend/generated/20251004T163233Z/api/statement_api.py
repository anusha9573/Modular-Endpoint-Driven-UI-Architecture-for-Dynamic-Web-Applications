from fastapi import APIRouter, HTTPException
import sqlite3
from backend import database
from typing import List

from ..models import StatementModel

router = APIRouter()

@router.post('/statement')
def create_statement(item: StatementModel):
    conn = sqlite3.connect(database.DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS statement (id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT, uploaded_at TEXT, user_id TEXT)')
    cur.execute('INSERT INTO statement (file_path, uploaded_at, user_id) VALUES (?, ?, ?)', (item.file_path, item.uploaded_at, item.user_id,))
    conn.commit()
    conn.close()
    return {'status': 'ok'}
