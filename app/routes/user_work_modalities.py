from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.user_work_modality import UserWorkModality
from app.utils.jwt import get_token_data

router = APIRouter()

# This endpoint is used to associate a work modality with a user
@router.post("/{user_id}", response_model=UserWorkModality)
def create_user_work_modality(user_id: str, modality: UserWorkModality, token: dict = Depends(get_token_data)):
    # Check if the user exists
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", token.get("sub")).eq("company_id", modality.company_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    user_role = user_company_role.data[0]["role"]
    if user_role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="User does not have permission to create work modalities for this company")

    # Check if the user exists
    user_data = supabase.table("users").select("*").eq("id", user_id).execute()
    if not user_data.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create the user work modality
    modality_data = {
        "user_id": user_id,
        "company_id": modality.company_id,
        "modality_id": modality.modality_id,
        "from_date": modality.from_date,
        "to_date": modality.to_date
    }
    
    response = supabase.table("user_work_modalities").insert(modality_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating user work modality")
    
    return response.data[0]

