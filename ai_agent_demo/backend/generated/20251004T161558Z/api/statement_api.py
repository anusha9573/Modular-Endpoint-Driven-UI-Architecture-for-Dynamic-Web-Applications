from fastapi import APIRouter, HTTPException
from typing import List

from ..models import StatementModel

router = APIRouter()

@router.post('/statement')
def create_statement(item: StatementModel):
    # TODO: add validation/persistence
    return {'status': 'ok', 'item': item}
