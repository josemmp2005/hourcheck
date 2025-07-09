from pydantic import BaseModel
from datetime import datetime

class CompanyInvitation(BaseModel):
    id: str  # UUID como string
    company_id: str  # UUID como string
    email: str
    code: str
    role: str
    used: bool = False
    expires_at: str
    created_at: str
    
    class Config:
        orm_mode = True
        
class CompanyInvitationCreate(BaseModel):
    company_id: str  # UUID como string
    email: str
    role: str
    # code se genera automáticamente
    # expires_at se calcula automáticamente
    
    class Config:
        orm_mode = True

class CompanyInvitationVerify(BaseModel):
    code: str
    
    class Config:
        orm_mode = True