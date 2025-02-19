from fastapi import APIRouter, Depends

from backend.core.database import get_db

router = APIRouter()


def test_funct():
    pass # get rid of when BG functionality is plugged in

# @router.post("/tasks/")
# async def create_task(task: test_funct, db=Depends(get_db)):
#     new_task = Task.create(db, name=task.name)
#     return {"id": new_task.id, "name": new_task.name, "status": new_task.status}
