from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    role: str
    active: bool
    created_at: str 
    
    class Config:
        orm_mode = True
