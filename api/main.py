from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

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
def getCourses(db: Session = Depends(get_db)):
    courses = db.query(models.Courses).all()
    return {"data": courses}


@app.get("/courses/{course_id}")
def getCourse(course_id: int, db: Session = Depends(get_db)):
    # course = db.filter()
    return fakedb[course_id-1]


@app.post("/courses")
def addCourse(course: Course, db: Session = Depends(get_db)):
    new_post = models.Courses(
        id=course.id, name=course.name, price=course.price, is_early_bird=course.is_early_bird)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Course added successfully"}


@app.delete("/courses/{course_id}")
def deleteCourse(course_id: int):
    fakedb.pop(course_id)
    return {"msg": "course deleted successfully"}


@app.get("/sql")
def test(db: Session = Depends(get_db)):
    return {"msg": "successful"}
