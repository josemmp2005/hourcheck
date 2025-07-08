from pydantic import BaseModel
import uuid

class User(BaseModel):
    id: uuid.UUID 
    name: str
    email: str
    password: str
    active: bool
    photo_url: str
    created_at: str 
    
    class Config:
        orm_mode = True

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    active: bool = True
    photo_url: str 
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True