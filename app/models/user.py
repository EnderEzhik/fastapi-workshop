from sqlalchemy import Column, Integer, String, Boolean

from pydantic import BaseModel, ConfigDict, Field

from app.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    full_name = Column(String(64))
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


# базовая модель пользователя
class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=20)
    full_name: str | None = Field(default=None, min_length=2, max_length=64)
    is_active: bool = True
    is_superuser: bool = False


# новая модель пользователя при регистрации
class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=20)
    full_name: str | None = Field(default=None, min_length=2, max_length=64)
    password: str = Field(..., min_length=6, max_length=32)


# модель создания нового пользователя только для суперпользователя
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=32)


# модель пользователя при обновлении
class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=2, max_length=20)
    full_name: str | None = Field(default=None, min_length=2, max_length=64)
    password: str | None = Field(default=None, min_length=6, max_length=32)


# модель пользователя при его возвращении по API
class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
