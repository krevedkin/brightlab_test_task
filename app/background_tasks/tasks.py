import asyncio
from uuid import UUID

from app.background_tasks.celery_config import celery_app
from app.services.email_service import EmailService
from app.task.dao import TaskDAO


@celery_app.task
def email_user_added_to_task(
    task_description: str,
    deadline: str,
    task_id: int,
    user_email: str,
):
    email = EmailService()

    message = f"Пользователь EMAIL добавил вас как исполнителя задачи: \
            {task_description} Срок выполнения до {deadline}"

    subject = f"Новая задача №{task_id}"

    msg = email.create_message(
        content=message,
        subject=subject,
        to=user_email,
    )

    email.send_email(msg)


@celery_app.task()
def email_users_task_expired(task_id: int):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(TaskDAO().get_task_with_users(task_id))
    if result and not result.completed:
        users = result.users
        email = EmailService()
        messages = []
        for user in users:
            msg = email.create_message(
                content=f"Задача {result.id} просрочена!",
                to=user.email,
                subject=f"Задача {result.id} просрочена!",
            )
            messages.append(msg)

        for message in messages:
            email.send_email(message)


def revoke_task(task_id: UUID):
    celery_app.control.revoke(str(task_id))
