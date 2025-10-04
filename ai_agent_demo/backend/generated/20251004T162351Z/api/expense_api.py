from fastapi import APIRouter, HTTPException
from typing import List

from ..models import ExpenseModel

router = APIRouter()

@router.post('/expense')
def create_expense(item: ExpenseModel):
    # TODO: add validation/persistence
    return {'status': 'ok', 'item': item}
