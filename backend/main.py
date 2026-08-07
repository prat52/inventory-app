from fastapi import Depends, FastAPI 
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






app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine) #tell sql alchemy to create the tables in the database if they don't exist
#whichever class inherits from Base will be created as a table in the database

@app.get("/")
def greet():
    return "hello world"





# def init_db():
#     db = session()
#     count = db.query(database_models.Product).count()
#     if count == 0:
#         for product in products:
#             db.add(database_models.Product(**product.model_dump()))
#             #** converts the dictionary returned by model_dump() into keyword arguments for the Product constructor, it gives key value pair out of dictionary and passes it to the Product constructor
#             #model_dump() is a method of pydantic BaseModel that returns a dictionary of the model's data
#         db.commit()

# init_db() #initialize the database with the products if the products table is empty


# @app.get("/products")
# def get_products(db: Session = Depends(get_db)):
#     products = db.query(database_models.Product).all()
#     return products
    

@app.get("/products")
def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    products = db.query(database_models.Product).filter(
        database_models.Product.user_id == current_user.id
    ).all()

    return products

# @app.get("/products/{product_id}")
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     # for product in products:
#     #     if product.id == product_id:
#     #         return product
#     # return {"error": "Product not found"}
#     db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
#     if db_product is None:
#         return {"error": "Product not found"}
#     return db_product

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

# @app.post("/products")
# def create_product(product: Product, db: Session = Depends(get_db)):
#     db.add(database_models.Product(**product.model_dump()))
#     db.commit()
#     return product

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

