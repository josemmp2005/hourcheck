from pydantic import BaseModel

class ClockIssue(BaseModel):
    id: str
    user_id: str
    company_id: str
    date: str
    issue_type: str
    description: str | None = None
    status: str
    created_at: str
    
    class Config:
        orm_mode = True