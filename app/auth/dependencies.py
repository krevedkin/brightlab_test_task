from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.exceptions import IncorrectTokenFormatException, UserNotFoundHTTPException
from app.auth.utils import get_user
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        user_id = payload.get("user_id")
    except JWTError:
        raise IncorrectTokenFormatException

    user = await get_user(email=username, user_id=user_id)

    if user is None:
        raise UserNotFoundHTTPException

    return user
