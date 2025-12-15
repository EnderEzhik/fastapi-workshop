from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.api.deps import SessionDep
from app.models.token import Token
from app.repositories.users import authenticate
import app.core.logging

from loguru import logger


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login/access-token", response_model=Token)
async def get_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(session, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Неудачная попытка входа: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid login or password", headers={ "WWW-Authenticate": "Bearer" })
    elif not user.is_active:
        logger.warning(f"Неактивный пользователь пытался войти в систему: {form_data.username}")
        raise HTTPException(status_code=400, detail="User is not active")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={ "sub": user.username }, expires_delta=access_token_expires)
    logger.info(f"Пользователь успешно вошел в систему: {user.username}")
    return Token(access_token=access_token, token_type="bearer")
