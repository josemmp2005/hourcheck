from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str
    active: bool
    created_at: str 
    
    class Config:
        orm_mode = True

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str
    active: bool = True
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: str
    password: str
    
    class Config:
        orm_mode = True