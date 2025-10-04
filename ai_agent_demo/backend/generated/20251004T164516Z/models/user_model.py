from pydantic import BaseModel

class UserModel(BaseModel):
    id: str
    email: str
    password_hash: str
    created_at: str
