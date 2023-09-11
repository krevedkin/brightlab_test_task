from app.dao.base import BaseDAO
from app.task.models import Task, TaskUser


class TaskDAO(BaseDAO):
    model = Task


class TaskUserDAO(BaseDAO):
    model = TaskUser
