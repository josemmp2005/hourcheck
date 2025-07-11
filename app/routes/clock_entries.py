from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.clock_entry import ClockEntry
from app.utils.jwt import get_token_data

router = APIRouter()

# This endpoint is used to clock in a user
@router.post("/clock-in", response_model=ClockEntry)
def clock_in(entry: ClockEntry, token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    company_id = entry.company_id
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", company_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    entry_data = {
        "user_id": user_id,
        "company_id": company_id,
        "type": "clock-in",
        "timestamp": entry.timestamp,
        "method": entry.method,
        "notes": entry.notes
    }
    
    response = supabase.table("clock_entries").insert(entry_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating clock entry")
    
    return response.data[0]

# This endpoint is used to clock out a user
@router.post("/clock-out", response_model=ClockEntry)
def clock_out(entry: ClockEntry, token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    company_id = entry.company_id
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", company_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    entry_data = {
        "user_id": user_id,
        "company_id": company_id,
        "type": "clock-out",
        "timestamp": entry.timestamp,
        "method": entry.method,
        "notes": entry.notes
    }
    
    response = supabase.table("clock_entries").insert(entry_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating clock entry")
    
    return response.data[0]