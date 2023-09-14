from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    tasks = relationship("Task", secondary="tasks_users", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"


class RefreshSessions(Base):
    __tablename__ = "refresh_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    refresh_token: Mapped[Uuid] = mapped_column(Uuid, unique=True)
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
