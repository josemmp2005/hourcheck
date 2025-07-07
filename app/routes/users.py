from fastapi import APIRouter, HTTPException
from app.db.supabase_client import supabase
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[User])
def get_users():
    response = supabase.table("users").select("*").execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error fetching users")
    
    return response.data

