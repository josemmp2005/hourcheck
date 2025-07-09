from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.work_modality import WorkModality

router = APIRouter()

# Get all work modalities
@router.get("/", response_model=list[WorkModality])
def get_work_modalities():
    response = supabase.table("work_modalities").select("*").execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error fetching work modalities")
    
    return response.data