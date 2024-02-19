from fastapi import APIRouter
from dbs_assignment.config import settings
from dbs_assignment.database import fetch_database_version

router = APIRouter()


@router.get("/v1/hello")
async def hello():
    return {
        'hello': settings.NAME
    }

@router.get("/v1/status")
async def get_database_status():
    version = await fetch_database_version()
    return {"version": version}
