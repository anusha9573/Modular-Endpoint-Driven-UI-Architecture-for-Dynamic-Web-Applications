from fastapi import APIRouter, HTTPException
import sqlite3
from backend import database
from typing import List

from ..models import ExpenseModel

router = APIRouter()

@router.post('/expense')
def create_expense(item: ExpenseModel):
    conn = sqlite3.connect(database.DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS expense (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, amount TEXT, merchant TEXT, category TEXT, description TEXT)')
    cur.execute('INSERT INTO expense (date, amount, merchant, category, description) VALUES (?, ?, ?, ?, ?)', (item.date, item.amount, item.merchant, item.category, item.description,))
    conn.commit()
    conn.close()
    return {'status': 'ok'}
