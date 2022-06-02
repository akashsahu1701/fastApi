from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users ']
)


@router.get("/")
def getUsers(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return {"data": users}


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exists")

    return {"data": user}


@router.post("/", status_code=status.HTTP_201_CREATED)
def addUsers(user: schemas.User, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User added successfully"}
