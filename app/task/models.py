from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TaskUser(Base):
    __tablename__ = "tasks_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    __table_args__ = (UniqueConstraint("user_id", "task_id"),)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    users = relationship("User", secondary="tasks_users", back_populates="tasks")


class CeleryTask(Base):
    __tablename__ = "celery_tasks"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
