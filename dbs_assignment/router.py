from fastapi import APIRouter

from dbs_assignment.endpoints import hello
from dbs_assignment.endpoints import posts, users, tags

router = APIRouter()
router.include_router(hello.router, tags=["hello"])
router.include_router(posts.router)
router.include_router(users.router)
router.include_router(tags.router)








