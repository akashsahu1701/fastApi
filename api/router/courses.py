from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)


@router.get("/")
def getCourses(db: Session = Depends(get_db)):
    courses = db.query(models.Courses).all()
    return {"data": courses}


@router.get("/{course_id}")
def getCourse(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")
    return {"data": course}


@router.post("/", status_code=status.HTTP_201_CREATED)
def addCourse(course: schemas.Course, db: Session = Depends(get_db), get_current_user: int = Depends(oauth.get_current_user)):
    new_post = models.Courses(**course.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Course added successfully"}


@router.delete("/{course_id}")
def deleteCourse(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    if course.first() == None:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")

    course.delete(synchronize_session=False)
    db.commit()

    return {"msg": "course deleted successfully"}


@router.put("/{course_id}")
def update(course_id: int, course: schemas.Course, db: Session = Depends(get_db)):
    course_query = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    if course_query.first() == None:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")

    course_query.update(course.dict(), synchronize_session=False)
    db.commit()

    return {"msg": "course updated successful"}
