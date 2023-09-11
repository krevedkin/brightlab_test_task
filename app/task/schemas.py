from datetime import datetime

from pydantic import BaseModel


class TaskSchema(BaseModel):
    description: str
    deadline: datetime


class TaskUpdateSchema(TaskSchema):
    task_id: int


class TaskDeleteSchema(BaseModel):
    task_id: int
