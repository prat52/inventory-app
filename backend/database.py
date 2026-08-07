from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import db_url

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
