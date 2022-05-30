from this import s
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
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404,
                            detail=f"post with id: {course_id} does not exists")
    return {"data": course}


@app.post("/courses")
def addCourse(course: Course, db: Session = Depends(get_db)):
    new_post = models.Courses(**course.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Course added successfully"}


@app.delete("/courses/{course_id}")
def deleteCourse(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    if course.first() == None:
        raise HTTPException(status_code=404,
                            detail=f"post with id: {course_id} does not exists")

    course.delete(synchronize_session=False)
    db.commit()

    return {"msg": "course deleted successfully"}


@app.put("/courses/{course_id}")
def update(course_id: int, course: Course, db: Session = Depends(get_db)):
    course_query = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    if course_query.first() == None:
        raise HTTPException(status_code=404,
                            detail=f"post with id: {course_id} does not exists")

    course_query.update(course.dict(), synchronize_session=False)
    db.commit()

    return {"msg": "course updated successful"}
