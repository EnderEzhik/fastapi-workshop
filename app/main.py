from fastapi import FastAPI

from app.api.routes import products, auth, users
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware


app = FastAPI()

setup_logging()
setup_middleware(app)

app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
