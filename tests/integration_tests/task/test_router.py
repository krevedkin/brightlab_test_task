from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.task
async def test_create_task(ac: AsyncClient):
    date = datetime.utcnow() + timedelta(minutes=10)

    print(date.isoformat())
    response = await ac.post(
        "/task",
        json={
            "description": "Test task",
            "deadline": date.isoformat() + "Z",
        },
    )
    assert response.status_code == 201


@pytest.mark.task
async def test_get_task(ac: AsyncClient):
    response = await ac.get("/task", params={"task_id": 1})
    data = response.json()
    expected_keys = ["description", "deadline", "id", "users"]

    assert all([key in data for key in expected_keys])
    assert response.status_code == 200


@pytest.mark.task
async def test_get_task_not_exist(ac: AsyncClient):
    response = await ac.get("/task", params={"task_id": 100500})
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Задача с таким id не найдена."


@pytest.mark.task
async def test_get_all_tasks(ac: AsyncClient, mocker):
    response = await ac.get("/task/list")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 1

    data = data[0]
    expected_keys = ["description", "deadline", "id", "users"]
    assert all([key in data for key in expected_keys])

    mocker.patch.object(ac, "get")
    response = await ac.get("/task/list")
    response.json.return_value = []

    assert await response.json() == []


@pytest.mark.task
async def test_update_task(ac: AsyncClient):
    date = datetime.utcnow() + timedelta(minutes=10)
    response = await ac.put(
        "/task",
        json={
            "description": "Обновленное описание задачи",
            "deadline": date.isoformat() + "Z",
            "task_id": 1,
        },
    )
    assert response.status_code == 201


@pytest.mark.task
async def test_update_task_error(ac: AsyncClient):
    date = datetime.utcnow() + timedelta(minutes=1)
    response = await ac.put(
        "/task",
        json={
            "description": "Обновленное описание задачи",
            "deadline": date.isoformat() + "Z",
            "task_id": 100500,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert (
        data["detail"]
        == "Невозможно изменить задачу с таким id. Такая задача не найдена."
    )


@pytest.mark.task
async def test_update_task_past_date(ac: AsyncClient):
    date = datetime.utcnow() - timedelta(minutes=10)
    response = await ac.put(
        "/task",
        json={
            "description": "Обновленное описание задачи",
            "deadline": date.isoformat() + "Z",
            "task_id": 1,
        },
    )

    assert response.status_code == 422


@pytest.mark.task
async def test_delete_task(ac: AsyncClient):
    response = await ac.request(
        method="delete",
        url="/task",
        json={
            "task_id": 1,
        },
    )
    assert response.status_code == 204


async def test_delete_task_error(ac: AsyncClient):
    response = await ac.request(
        method="delete",
        url="/task",
        json={
            "task_id": 100500,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert (
        data["detail"]
        == "Невозможно удалить задачу с таким id. Такая задача не найдена."
    )


@pytest.mark.task
@pytest.mark.parametrize(
    ("status_code", "detail", "task_id", "user_id"),
    [
        (
            201,
            "Пользователь успешно добавлен к задаче",
            1,
            3,
        ),
        (
            201,
            "Пользователь успешно добавлен к задаче",
            2,
            3,
        ),
        (
            409,
            "Пользователь уже добавлен к этой задаче.",
            1,
            1,
        ),
        (
            409,
            "Невозможно связать пользователя с задачей. Проверьте существует ли пользователь с таким id или задача с таким id.",
            100500,
            100500,
        ),
    ],
)
async def test_add_user_to_task(ac: AsyncClient, status_code, detail, task_id, user_id):
    response = await ac.post(
        "/task/user",
        json={
            "task_id": task_id,
            "user_id": user_id,
        },
    )
    data = response.json()
    assert response.status_code == status_code
    assert data["detail"] == detail


@pytest.mark.task
@pytest.mark.parametrize(
    ("status_code", "task_id", "user_id"),
    [
        (204, 1, 1),
        (409, 100500, 1),
        (409, 1, 100500),
        (409, 100500, 100500),
    ],
)
async def test_delete_user_from_task(ac: AsyncClient, status_code, task_id, user_id):
    response = await ac.request(
        method="delete",
        url="/task/user",
        json={"task_id": task_id, "user_id": user_id},
    )
    assert response.status_code == status_code

    if status_code == 409:
        data = response.json()
        assert (
            data["detail"]
            == "Невозможно удалить пользователя из задачи. Проверьте существует ли пользователь с таким id или задача с таким id"
        )
