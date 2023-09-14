from fastapi import status

from app.exceptions import BaseHTTPException


class TaskDoesNotExistsHttpError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задача с таким id не найдена."


class CantAddUserToTaskHttpError(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Невозможно связать пользователя с задачей. Проверьте существует ли пользователь с таким id или задача с таким id."


class CantDeleteTaskHttpError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Невозможно удалить задачу с таким id. Такая задача не найдена."


class CantUpdateTaskHttpError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Невозможно изменить задачу с таким id. Такая задача не найдена."


class CantDeleteUserFromTaskHttpError(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Невозможно удалить пользователя из задачи. Проверьте существует ли пользователь с таким id или задача с таким id"


class UserAlreadyAddedToTaskDatabaseError(Exception):
    message = """
    Запись в БД с такими такими значениями уже существует,
    предоставьте уникальную пару user_id и task_id
    """

    def __init__(self):
        super().__init__(self.message)


class UserAlreadyAddedToTaskHTTPError(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже добавлен к этой задаче."


class CantAddUserToTaskDatabaseError(Exception):
    message = """
    Невозможно создать запись, такого user_id или task_id не найдено в БД.
    """

    def __init__(self):
        super().__init__(self.message)
