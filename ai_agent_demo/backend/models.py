from pydantic import BaseModel
from typing import List, Optional


class BriefRequest(BaseModel):
    text: str


class TaskDetail(BaseModel):
    role: str  # frontend | backend
    title: str
    description: str
    filename: Optional[str] = None
    language: Optional[str] = None
    code: Optional[str] = None


class TaskResponse(BaseModel):
    tasks: List[str]
    structured: List[TaskDetail] = []
