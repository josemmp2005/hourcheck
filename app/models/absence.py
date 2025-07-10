from pydantic import BaseModel

class Absence(BaseModel):
    id: str
    user_id: str
    date: str
    type: str
    justified: bool
    notes: str | None = None
    company_id: str
    
    class Config:
        orm_mode = True