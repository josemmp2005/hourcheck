from pydantic import BaseModel

class Vacation(BaseModel):
    id: str
    user_id: str
    company_id: str
    start_date: str
    end_date: str
    status: str
    reason: str | None = None
    requested_at: str
    
    class Config:
        orm_mode = True