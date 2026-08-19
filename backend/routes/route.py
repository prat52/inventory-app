from auth import verify_password, create_access_token, hash_password
from models.schemas import UserLogin, UserRegister
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import database_models
from limiter import limiter

router = APIRouter()  # Changed from app = FastAPI()

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(database_models.User).filter(
        database_models.User.email == user.email
    ).first()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid Email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong Password")

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, user: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(database_models.User).filter(
        database_models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = database_models.User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()

    return {"message": "Registration Successful"}