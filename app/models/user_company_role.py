from pydantic import BaseModel

class UserCompanyRole(BaseModel):
    id: str
    user_id: str
    company_id: str
    role: str
    
    class Config:
        orm_mode = True
        