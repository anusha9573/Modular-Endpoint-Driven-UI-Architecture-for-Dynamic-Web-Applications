from pydantic import BaseModel

class StatementModel(BaseModel):
    file_path: str
    uploaded_at: str
    user_id: str
