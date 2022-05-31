from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def hello_server():
    return {"msg": "Hello World"}


@app.get("/users")
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return {"data": users}


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exists")

    return {"data": user}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def addUsers(user: schemas.User, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User added successfully"}


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
                            detail=f"course with id: {course_id} does not exists")
    return {"data": course}


@app.post("/courses", status_code=status.HTTP_201_CREATED)
def addCourse(course: schemas.Course, db: Session = Depends(get_db)):
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
                            detail=f"course with id: {course_id} does not exists")

    course.delete(synchronize_session=False)
    db.commit()

    return {"msg": "course deleted successfully"}


@app.put("/courses/{course_id}")
def update(course_id: int, course: schemas.Course, db: Session = Depends(get_db)):
    course_query = db.query(models.Courses).filter(
        models.Courses.id == course_id)

    if course_query.first() == None:
        raise HTTPException(status_code=404,
                            detail=f"course with id: {course_id} does not exists")

    course_query.update(course.dict(), synchronize_session=False)
    db.commit()

    return {"msg": "course updated successful"}
