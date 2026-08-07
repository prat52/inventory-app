from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)
    company = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "id"),
    )


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True,autoincrement=True)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)