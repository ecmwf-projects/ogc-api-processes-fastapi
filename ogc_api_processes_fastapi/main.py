from fastapi import FastAPI

from routers import processes_router

app = FastAPI()

app.include_router(processes_router)
