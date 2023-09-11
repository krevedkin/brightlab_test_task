from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import Response
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.auth.dao import RefreshSessionsDAO, UsersDAO
from app.auth.exceptions import UserAlreadyExistsHTTPException
from app.auth.models import User
from app.auth.schemas import AccessToken, RefreshToken
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_ecnode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINS)
    to_ecnode.update({"exp": expire})
    return jwt.encode(to_ecnode, settings.SECRET_KEY, settings.ALGORITHM)


async def get_user(email: str, user_id: str | None = None) -> User | None:
    user = await UsersDAO.get_by_email(email)
    if not user and user_id:
        user = await UsersDAO().get_by_id(int(user_id))
    return user


async def authenticate_user(email: str, password: str) -> User | bool:
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_refresh_token():
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXP_DAYS
    )
    refresh_token = uuid4()
    return RefreshToken(refresh_token=refresh_token, expire=expire)


async def set_tokens(response: Response, user: User) -> AccessToken:
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )
    refresh_token = create_refresh_token()

    await RefreshSessionsDAO().add_refresh_token(
        user_id=user.id,
        token=refresh_token.refresh_token,
        expire=refresh_token.expire,
    )
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=str(refresh_token.refresh_token),
        httponly=True,
        expires=refresh_token.expire,
    )
    return AccessToken(access_token=access_token, token_type="bearer")


async def register_user(email: str, password: str):
    hashed_password = get_password_hash(password)
    try:
        await UsersDAO().add_user(email=email, hashed_password=hashed_password)
    except IntegrityError:
        raise UserAlreadyExistsHTTPException
