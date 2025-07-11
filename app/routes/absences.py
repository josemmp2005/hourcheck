from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.absence import Absence
from app.utils.jwt import get_token_data

router = APIRouter()

@router.post("/request-absence", response_model=Absence)
def request_absence(absence: Absence, token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    company_id = absence.company_id
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", company_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    absence_data = {
        "user_id": user_id,
        "company_id": company_id,
        "type": absence.type,
        "start_date": absence.start_date,
        "end_date": absence.end_date,
        "reason": absence.reason,
        "status": "pending"
    }
    
    response = supabase.table("absences").insert(absence_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating absence request")
    
    return response.data[0]