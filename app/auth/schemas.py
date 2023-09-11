from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field, validator


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: UUID4
    expire: datetime


class User(BaseModel):
    id: int
    email: EmailStr


class UserChangeBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    password_repeat: str = Field(min_length=6)

    @validator("password_repeat")
    def passwords_must_be_equal(cls, password_repeat, values):
        password = values.get("password")
        if password and password != password_repeat:
            raise ValueError("Пароли не совпадают")

        return password_repeat


class UserRegister(UserChangeBase):
    ...


class UserUpdate(UserChangeBase):
    ...
