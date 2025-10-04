from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class Item2Request(BaseModel):
    text: str

router = APIRouter()

@router.post('/api/item2')
def create_item(req: Item{i}Request):
    # validation and persistence logic goes here
    return {'status':'ok'}
