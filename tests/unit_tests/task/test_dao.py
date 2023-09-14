import pytest

from app.task.dao import TaskDAO, TaskUserDAO
from app.task.models import Task
from app.task.exceptions import (
    CantAddUserToTaskDatabaseError,
    UserAlreadyAddedToTaskDatabaseError,
)


@pytest.mark.task
async def test_get_all_tasks_with_users():
    result = await TaskDAO().get_all_tasks_with_users()
    assert all([isinstance(task, Task) for task in result])


@pytest.mark.task
async def test_get_tasks_with_users():
    task = await TaskDAO().get_task_with_users(task_id=1)
    assert isinstance(task, Task)
    assert len(task.users) == 2


@pytest.mark.task
async def test_get_tasks_with_users_record_doesnt_exist():
    task = await TaskDAO().get_task_with_users(task_id=10)
    assert task is None


@pytest.mark.task
async def test_insert_record_task_user():
    await TaskUserDAO().insert_record(task_id=2, user_id=2)

    with pytest.raises(UserAlreadyAddedToTaskDatabaseError):
        await TaskUserDAO().insert_record(task_id=2, user_id=2)

    with pytest.raises(CantAddUserToTaskDatabaseError):
        await TaskUserDAO().insert_record(task_id=100, user_id=100)
