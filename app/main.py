from typing import Union

from fastapi import FastAPI

from .api import api_router
from .database import init_database, close_database

app = FastAPI()

app.add_event_handler("startup", init_database)
app.add_event_handler("shutdown", close_database)

app.include_router(api_router)


@app.get("/")
def read_root() -> Union[str, int]:
    return "Hello, world!"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None) -> dict:
    return {"item_id": item_id, "q": q}
