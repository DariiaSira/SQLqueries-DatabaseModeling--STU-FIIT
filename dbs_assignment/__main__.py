from fastapi import FastAPI
from dbs_assignment.router import router
from dbs_assignment.database import get_database_version
import asyncio

app = FastAPI(title="DBS")
app.include_router(router)

# Подключение к базе данных PostgreSQL
@app.on_event("startup")
async def startup_event():
    await get_database_version(app)
