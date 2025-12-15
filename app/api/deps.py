import jwt
from jwt import InvalidTokenError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated
from pydantic import ValidationError

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.database import AsyncSessionMaker
from app.models.token import TokenData
from app.models.user import User
from app.repositories.users import get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


# Функция-зависимость для генерации новой сессии
async def get_session():
    async with AsyncSessionMaker() as session:
        yield session


# Создаем краткую версиб зависимоси для использования в других модулях
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(status_code=401,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Autheenticate": "Bearer"})

    try:
        payload = jwt.decode(jwt=token,
                             key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        if not token_data["sub"]:
            raise credentials_exception
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    user = await get_user_by_username(session, token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=404, detail="User is not active")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_superuser(current_user: CurrentUserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="У пользователя нет прав для данного действия")
    return current_user
