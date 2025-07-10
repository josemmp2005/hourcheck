from pydantic import BaseModel

class UserWorkModality(BaseModel):
    id: str 
    user_id: str 
    company_id: str 
    modality_id: str  
    from_data: str  
    to_data: str 
    
    class Config:
        orm_mode = True
        
