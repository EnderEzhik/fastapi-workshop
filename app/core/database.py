from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_ASYNC = "sqlite+aiosqlite:///products.db"
DATABASE_SYNC = "sqlite:///products.db"

engine = create_async_engine(url=DATABASE_ASYNC, echo=True)
AsyncSessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False)
