from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskMove(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    board_id: int
    title: str
    description: Optional[str]
    status: str
    position: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Board schemas
class BoardCreate(BaseModel):
    title: str
    description: Optional[str] = None

class BoardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class BoardResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class BoardWithTasks(BoardResponse):
    tasks: List[TaskResponse] = []