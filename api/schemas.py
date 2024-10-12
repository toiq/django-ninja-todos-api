from typing import Optional
from ninja import Schema
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ProfileSchemaIn(BaseModel):
    dark_mode: Optional[bool] = False
    user_id: int


class ProfileSchemaOut(ProfileSchemaIn):
    id: int

    class Config:
        orm_mode = True


class TodoListSchemaIn(Schema):
    name: str
    description: Optional[str] = None


class TodoListSchemaOut(Schema):
    id: int
    name: str
    description: Optional[str] = None
    created: datetime
    updated: datetime


class SignInSchema(Schema):
    username: str
    password: str


class SignUpSchema(Schema):
    username: str = Field(max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)


class TodoSchemaIn(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    due_date: Optional[datetime] = None
    todo_list: int


class TodoSchemaOut(TodoSchemaIn):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
