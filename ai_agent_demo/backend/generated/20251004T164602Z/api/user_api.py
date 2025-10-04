from fastapi import APIRouter, HTTPException
import sqlite3
from backend import database
from typing import List

from ..models import UserModel

router = APIRouter()

@router.post('/user')
def create_user(item: UserModel):
    conn = sqlite3.connect(database.DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT, email TEXT, password_hash TEXT, created_at TEXT)')
    cur.execute('INSERT INTO user (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)', (item.id, item.email, item.password_hash, item.created_at,))
    conn.commit()
    conn.close()
    return {'status': 'ok'}
