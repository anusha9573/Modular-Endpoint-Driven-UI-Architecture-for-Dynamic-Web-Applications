from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class Item1Request(BaseModel):
    text: str

router = APIRouter()

@router.post('/api/item1')
def create_item(req: Item{i}Request):
    # validation and persistence logic goes here
    return {'status':'ok'}
