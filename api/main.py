from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello_server():
    return {"msg": "Hello World"}


class Course(BaseModel):
    id: int
    name: str
    price: float
    is_early_bird: Optional[bool] = None


fakedb = []


@app.get("/courses")
def getCourses():
    return fakedb


@app.get("/courses/{course_id}")
def getCourse(course_id: int):
    return fakedb[course_id-1]


@app.post("/courses")
def addCourse(course: Course):
    fakedb.append(course.dict())
    return {"msg": "course added successfully"}


@app.delete("/courses/{course_id}")
def deleteCourse(course_id: int):
    fakedb.pop(course_id)
    return {"msg": "course deleted successfully"}
