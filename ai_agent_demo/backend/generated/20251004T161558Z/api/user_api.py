from fastapi import APIRouter, HTTPException
from typing import List

from ..models import UserModel

router = APIRouter()

@router.post('/user')
def create_user(item: UserModel):
    # TODO: add validation/persistence
    return {'status': 'ok', 'item': item}
