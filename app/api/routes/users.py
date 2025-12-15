from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUserDep, SessionDep, get_current_superuser
from app.models.user import UserCreate, UserRegister, UserUpdate, UserOut
import app.repositories.users as user_repo


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.get("/{username}", response_model=UserOut)
async def get_user(session: SessionDep, current_user: CurrentUserDep, username: str):
    user = await user_repo.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username != current_user.username and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="У пользователя нет прав")
    return user


@router.get("/", response_model=list[UserOut], dependencies=[Depends(get_current_superuser)])
async def get_users_list(session: SessionDep, offset: int = 0, limit: int = 100):
    users = await user_repo.get_users(session, offset, limit)
    return users


@router.post("/", response_model=UserOut)
async def register_user(session: SessionDep, user_register: UserRegister):
    user = await user_repo.get_user_by_username(session, user_register.username)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь с таким username уже существует")
    user_create = UserCreate(**user_register.model_dump())
    new_user = await user_repo.create_user(session, user_create)
    return new_user


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(session: SessionDep, current_user: CurrentUserDep, user_id: int, user_update: UserUpdate):
    user_db = await user_repo.get_user_by_id(session, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if user_db.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="У пользователя нет прав")
    updated_user = await user_repo.update_user(session, user_db, user_update)
    return updated_user


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(get_current_superuser)])
async def delete_user_by_user_id(session: SessionDep, current_user: CurrentUserDep, user_id: int):
    user = await user_repo.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Администратору нельзя удалить самого себя")
    await user_repo.delete_user(session, user)
