from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models import database_models
from models.schemas import Product
from database import session, engine
from sqlalchemy.orm import Session
from routes.route import router 
from database import get_db
from auth import get_current_user
from models.database_models import User
from fastapi import HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "hello world"
    

@app.get("/products")
def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    products = db.query(database_models.Product).filter(
        database_models.Product.user_id == current_user.id
    ).all()

    return products


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    product = db.query(database_models.Product).filter(
        database_models.Product.id == product_id,
        database_models.Product.user_id == current_user.id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.post("/products")
def create_product(
    product: Product,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_product = database_models.Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        company=product.company,
        user_id=current_user.id
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@app.put("/products/{id}")
def update_product(
    id: int,
    product: Product,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id,
        database_models.Product.user_id == current_user.id
    ).first()

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db_product.company = product.company

    db.commit()
    db.refresh(db_product)

    return db_product

@app.delete("/products/{id}")
def delete_product(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id,
        database_models.Product.user_id == current_user.id
    ).first()

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(db_product)
    db.commit()

    return {
        "message": "Deleted Successfully"
    }