from app.background_tasks.celery_config import celery_app
from app.services.email_service import EmailService


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

