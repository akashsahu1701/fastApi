from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "Mycdkjscnadkcnjnecmnwencje"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_TIME = 30


def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user
