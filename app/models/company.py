from pydantic import BaseModel

class Company(BaseModel):
    id: str  # UUID como string que devuelve Supabase
    name: str
    cif: str
    email: str
    description: str 
    photo_url: str
    created_at: str
    
    class Config:
        orm_mode = True

class CompanyCreate(BaseModel):
    name: str
    cif: str
    email: str
    description: str 
    photo_url: str
    
    class Config:
        orm_mode = True
        
class CompanyUpdate(BaseModel):
    name: str | None = None
    cif: str | None = None
    email: str | None = None
    description: str | None = None 
    photo_url: str | None = None
    
    class Config:
        orm_mode = True