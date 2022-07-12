from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://sqvjrbqpdsqgbo:a38001e9465f171fa8f23f3d5ba58bd195d535ce16794e0f35bfbeba6f905a21@ec2-52-20-166-21.compute-1.amazonaws.com:5432/d94f5sfbv578fk'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
