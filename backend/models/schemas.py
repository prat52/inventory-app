from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int
    company : str


class UserRegister(BaseModel): 
    email:str
    password:str


class UserLogin(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str