from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dao import RefreshSessionsDAO, UsersDAO
from app.auth.dependencies import get_current_user
from app.auth.exceptions import (
    InvalidCredentialsHTTPException,
    InvalidRefreshTokenHTTPException,
    NoRefreshSessionHTTPException,
    NoRefreshTokenHTTPException,
    RefreshTokenExpriredException,
    UserNotFoundHTTPException,
)
from app.auth.models import User as UserModel
from app.auth.schemas import AccessToken, User, UserRegister, UserUpdate
from app.auth.utils import (
    authenticate_user,
    get_password_hash,
    register_user,
    set_tokens,
)
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/token",
    response_model=AccessToken,
    responses={
        401: {
            "description": "Неправильный логин или пароль",
            "content": {
                "application/json": {
                    "example": {"detail": "Неправильный логин или пароль"}
                }
            },
        },
    },
)
async def get_access_token(
    response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, password=form_data.password)
    if not user:
        raise InvalidCredentialsHTTPException

    if isinstance(user, UserModel):
        return await set_tokens(response, user)


@router.post("/refresh", response_model=AccessToken)
async def refresh_token(
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)

    if not refresh_token:
        raise NoRefreshTokenHTTPException

    try:
        refresh_token = UUID(refresh_token)
    except ValueError:
        raise InvalidRefreshTokenHTTPException

    refresh_session = await RefreshSessionsDAO().get_refresh_session(refresh_token)

    if not refresh_session:
        raise NoRefreshSessionHTTPException

    if refresh_session.expire < datetime.now(timezone.utc):
        raise RefreshTokenExpriredException
    user_data = await UsersDAO().get_by_id(refresh_session.user_id)

    if user_data:
        return await set_tokens(response, user_data)

    raise UserNotFoundHTTPException


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
):
    refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
    await RefreshSessionsDAO().delete_record(refresh_token=refresh_token)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def registration(user: UserRegister):
    """
    Создает нового пользователя.
    """
    await register_user(user.email, user.password)


@router.get("/me")
async def get_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Получить данные текущего пользователя.
    """
    return User(id=user.id, email=user.email)


@router.put("/update-user")
async def update_user(
    update_data: UserUpdate,
    user: Annotated[User, Depends(get_current_user)],
):
    """
    Полностью обновляет запись о пользователе. Необходимо передать новый email
    и два пароля, после чего запись обновится.
    """
    update_data.password = get_password_hash(update_data.password)
    await UsersDAO().update_record(
        record_id=user.id,
        email=update_data.email,
        hashed_password=update_data.password,
    )


@router.delete("/delete-user")
async def delete_user(
    user: Annotated[User, Depends(get_current_user)],
    request: Request,
    response: Response,
):
    """
    Удаляет залогиненого пользователя. После удаления производит logout.
    """

    await UsersDAO().delete_record(id=user.id)
    refresh_token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.REFRESH_TOKEN_COOKIE_NAME)
    await RefreshSessionsDAO().delete_record(refresh_token=refresh_token)
