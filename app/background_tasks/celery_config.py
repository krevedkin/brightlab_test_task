from celery import Celery

celery_app = Celery(
    "celery_config",
    broker="redis://localhost",
    include=["app.background_tasks.tasks"],
)
