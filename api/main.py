from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello_server():
    return {"msg": "Hello World"}


fakedb = []


@app.get("/courses")
def getCourses():
    return fakedb


@app.get("/courses/{course_id}")
def getCourse(course_id: int):
    return fakedb[course_id-1]
