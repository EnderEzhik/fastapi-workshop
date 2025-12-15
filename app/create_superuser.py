import asyncio
from sqlalchemy import select

from app.core.database import AsyncSessionMaker
from app.core.security import get_password_hash
from app.models.user import User


async def create_superuser():
    async with AsyncSessionMaker() as session:
        username = "admin"
        password = "long_long_secret_secret_password_password"

        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        check_user = result.scalar_one_or_none()
        if check_user:
            print(f"Пользователь с username {username} уже существует")
            return
        super_user = User(username=username,
                          full_name="admin",
                          hashed_password=get_password_hash(password),
                          is_superuser=True)
        session.add(super_user)
        await session.commit()
        print(f"Суперпользователь {username} создан")


if __name__ == "__main__":
    asyncio.run(create_superuser())
