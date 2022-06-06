from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)


@router.get("/", response_model=List[schemas.Course])
def getCourses(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    courses = db.query(models.Courses).all()
    return courses


@router.get("/{course_id}")
def getCourse(course_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")
    return {"data": course}


@router.post("/", status_code=status.HTTP_201_CREATED)
def addCourse(course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    new_course = models.Courses(
        owner_id=current_user.id, owner=current_user, **course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"msg": "Course added successfully"}


@router.delete("/{course_id}")
def deleteCourse(course_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    course = db.query(models.Courses).filter(
        models.Courses.id == course_id).first()

    if course == None:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")

    if course.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform required actions")

    course.delete(synchronize_session=False)
    db.commit()

    return {"msg": "course deleted successfully"}


@router.put("/{course_id}")
def update(course_id: int, updated_course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    course_query = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    course = course_query.first()

    if course == None:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")

    if course.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not Authorized to perform required actions")

    course_query.update(updated_course.dict(), synchronize_session=False)
    db.commit()

    return {"msg": "course updated successful"}
