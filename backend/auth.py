from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import JWTError
from config import SECRET_KEY


ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def create_access_token(data):

    to_encode=data.copy()

    expire = datetime.utcnow() + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token):

    try:

        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username=payload.get("sub")

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="login"
)

from fastapi import Depends
from sqlalchemy.orm import Session
from database import session, get_db
from models.database_models import User



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = verify_token(token)

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user