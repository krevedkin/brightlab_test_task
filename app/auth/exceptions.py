from fastapi import status

from app.exceptions import BaseHTTPException


class BaseAuthException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    _headers_401 = {"WWW-Authenticate": "Bearer"}


class NoRefreshTokenHTTPException(BaseAuthException):
    detail = "refresh token отсутствует"


class InvalidRefreshTokenHTTPException(BaseAuthException):
    detail = "Неверный формат refresh token"


class NoRefreshSessionHTTPException(BaseAuthException):
    detail = "Сессия не найдена. Пройдите процедуру аутентификации заново"


class RefreshTokenExpriredException(BaseAuthException):
    detail = "refresh token просрочен"


class InvalidCredentialsHTTPException(BaseAuthException):
    detail = "Неверный логин или пароль"


class UserNotFoundHTTPException(BaseAuthException):
    detail = "Пользователь не найден"


class IncorrectTokenFormatException(BaseAuthException):
    detail = "Неверный формат токена"


class UserAlreadyExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже существует"