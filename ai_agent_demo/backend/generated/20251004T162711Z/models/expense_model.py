from pydantic import BaseModel

class ExpenseModel(BaseModel):
    date: str
    amount: str
    merchant: str
    category: str
    description: str
