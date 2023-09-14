from fastapi import APIRouter, status

from app.background_tasks import tasks
from app.task.dao import TaskDAO, TaskUserDAO
from app.auth.dao import UsersDAO
from app.task.schemas import (
    TaskAddUserSchema,
    TaskDeleteSchema,
    TaskDeleteUserSchema,
    TaskGetSchema,
    TaskUpdateSchema,
    TaskCreateSchema,
)

from app.task import exceptions as exc

router = APIRouter(prefix="/task", tags=["Задачи"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreateSchema):
    """
    Создать новую задачу.
    """
    await TaskDAO().insert_record(description=task.description, deadline=task.deadline)
    return {"detail": "Задача создана"}


@router.get(
    "",
    response_model=TaskGetSchema,
    responses={
        404: {
            "description": "Задача не найдена в базе данных.",
            "content": {
                "application/json": {
                    "example": {"detail": "Задача с таким id не найдена."}
                }
            },
        },
    },
)
async def get_task(task_id: int):
    """
    Возвращает одну задачу со списком пользователей, ассоциированных с нею.
    """
    result = await TaskDAO().get_task_with_users(task_id)
    if not result:
        raise exc.TaskDoesNotExistsHttpError
    return result


@router.get("/list", response_model=list[TaskGetSchema])
async def get_all_tasks():
    """
    Возвращает все существующие задачи, включая список пользователей, связанных с
    задачей.
    """
    return await TaskDAO().get_all_tasks_with_users()


@router.put(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {
            "description": "Задача для удаления не найдена",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Невозможно изменить задачу с таким id. Такая задача не найдена."
                    }
                }
            },
        },
    },
)
async def update_task(task: TaskUpdateSchema):
    """
    Обновляет все поля задачи.
    """
    result = await TaskDAO().update_record(
        record_id=task.task_id, description=task.description, deadline=task.deadline
    )

    if not result:
        raise exc.CantUpdateTaskHttpError

    return {"detail": "Задача обновлена"}


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Successful Response",
        },
        404: {
            "description": "Задача для удаления не найдена",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Невозможно удалить задачу с таким id. Такая задача не найдена."
                    }
                }
            },
        },
    },
)
async def delete_task(task: TaskDeleteSchema):
    """
    Удаляет задачу. Если задачи не существует, вызовет ошибку 404.
    """
    result = await TaskDAO().delete_record(id=task.task_id)
    if not result:
        raise exc.CantDeleteTaskHttpError


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {"detail": "Пользователь успешно добавлен к задаче"}
                }
            },
        },
        409: {
            "description": "Невозможно добавить пользователя к задаче",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Невозможно связать пользователя с задачей. Проверьте существует ли пользователь с таким id или задача с таким id"
                    }
                }
            },
        },
    },
)
async def add_user_to_task(task: TaskAddUserSchema):
    """
    Добавить пользователя к существующей задаче.
    """
    try:
        await TaskUserDAO.insert_record(user_id=task.user_id, task_id=task.task_id)
    except exc.CantAddUserToTaskDatabaseError:
        raise exc.CantAddUserToTaskHttpError
    except exc.UserAlreadyAddedToTaskDatabaseError:
        raise exc.UserAlreadyAddedToTaskHTTPError

    user_data = await UsersDAO().get_by_id(task.user_id)
    task_data = await TaskDAO().get_by_id(task.task_id)
    if user_data and task_data:
        tasks.email_user_added_to_task.delay(
            task_description=task_data.description,
            deadline=task_data.deadline,
            task_id=task_data.id,
            user_email=user_data.email,
        )
    return {"detail": "Пользователь успешно добавлен к задаче"}


@router.delete(
    "/user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        409: {
            "description": "Невозможно удалить пользователя из задачи.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Невозможно удалить пользователя из задачи. Проверьте существует ли пользователь с таким id или задача с таким id"
                    }
                }
            },
        },
    },
)
async def delete_user_from_task(task: TaskDeleteUserSchema):
    """
    Удалить пользователя из существующей задачи.
    """
    result = await TaskUserDAO().delete_record(
        task_id=task.task_id, user_id=task.user_id
    )
    if not result:
        raise exc.CantDeleteUserFromTaskHttpError
