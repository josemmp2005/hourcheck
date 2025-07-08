from pydantic import BaseModel
import uuid

class CompanyInvitation(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    email: str
    code: str
    role: str
    used: bool = False
    expires_at: str
    
    class Config:
        orm_mode = True