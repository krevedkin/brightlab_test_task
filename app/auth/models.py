from datetime import datetime

from click import DateTime
from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"


class RefreshSessions(Base):
    __tablename__ = "refresh_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    refresh_token: Mapped[Uuid] = mapped_column(Uuid, unique=True)
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # type: ignore
