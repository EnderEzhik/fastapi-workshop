from time import perf_counter

from fastapi import FastAPI, Request

from loguru import logger


def setup_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_process_time_haver(request: Request, call_next):
        start_time = perf_counter()
        response = await call_next(request)

        process_time = (perf_counter() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} выполнялся {process_time:.2f} ms")
        response.headers["X-Process-Time"] = f"{process_time:.2f}"
        return response
