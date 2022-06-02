from fastapi import FastAPI
from . import models
from .database import engine
from .router import courses, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(courses.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def hello_server():
    return {"msg": "Hello World"}
