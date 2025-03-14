from fastapi import FastAPI

from .api import api_router
from .database import init_database, close_database

app = FastAPI()

app.add_event_handler("startup", init_database)
app.add_event_handler("shutdown", close_database)

app.include_router(api_router)
