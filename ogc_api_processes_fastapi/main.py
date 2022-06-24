from fastapi import FastAPI

from . import routers


def instantiate_app() -> FastAPI:

    app = FastAPI()
    app.include_router(routers.processes_router)

    return app


app = instantiate_app()
