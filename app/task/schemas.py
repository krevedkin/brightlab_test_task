from datetime import datetime

from pydantic import BaseModel, FutureDatetime

from app.auth.schemas import User


class TaskSchemaBase(BaseModel):
    description: str
    deadline: datetime


class TaskGetSchema(TaskSchemaBase):
    id: int
    users: list[User]


class TaskCreateSchema(TaskSchemaBase):
    deadline: FutureDatetime


class TaskUpdateSchema(TaskSchemaBase):
    task_id: int
    deadline: FutureDatetime


class TaskDeleteSchema(BaseModel):
    task_id: int


class TaskAddUserSchema(BaseModel):
    task_id: int
    user_id: int


class TaskDeleteUserSchema(TaskAddUserSchema):
    ...
