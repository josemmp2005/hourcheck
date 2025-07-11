from pydantic import BaseModel

class ClockEntry(BaseModel):
    id: str 
    user_id: str
    company_id: str
    type: str
    timestamp: str
    method: str
    notes: str | None = None  

    
    class Config:
        orm_mode = True