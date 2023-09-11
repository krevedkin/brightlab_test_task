from fastapi import APIRouter

from app.task.dao import TaskDAO
from app.task.schemas import TaskDeleteSchema, TaskSchema, TaskUpdateSchema

router = APIRouter(prefix="/task", tags=["Задачи"])


@router.post("")
async def create_task(task: TaskSchema):
    await TaskDAO().insert_record(description=task.description, deadline=task.deadline)


@router.get("")
async def get_task(task_id: int):
    return await TaskDAO().get_by_id(task_id)


@router.put("")
async def update_task(task: TaskUpdateSchema):
    await TaskDAO().update_record(
        record_id=task.task_id, description=task.description, deadline=task.deadline
    )


@router.delete("")
async def delete_task(task: TaskDeleteSchema):
    await TaskDAO().delete_record(id=task.task_id)


@router.post("/list")
async def create_task_list():
    ...


@router.get("/list")
async def get_task_list():
    ...


@router.put("/list")
async def update_task_list():
    ...


@router.delete("/list")
async def delete_task_list():
    ...
