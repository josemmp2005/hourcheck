from pydantic import BaseModel

class WorkModality(BaseModel):
    id: str  
    name: str
    description: str | None = None
    
    class Config:
        orm_mode = True
        
