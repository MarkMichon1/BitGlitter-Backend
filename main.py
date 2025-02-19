from fastapi import FastAPI, APIRouter

from backend.api import root_router
from backend.core.database import get_db, initialize_database

initialize_database()

app_backend = FastAPI()
app_backend.include_router(root_router)

@app_backend.get('/')
def test_route():
    return {'test': True}

@app_backend.get('/')
def test_route2():
    return {'test': True}