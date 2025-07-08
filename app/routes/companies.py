from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.company import Company, CompanyCreate, CompanyUpdate
from app.utils.jwt import get_token_data

router = APIRouter()

@router.post("/register", response_model=Company)
def create_company(company: CompanyCreate, token: dict = Depends(get_token_data)):
    existing_company = supabase.table("companies").select("*").eq("cif", company.cif).execute()
    
    if existing_company.data:
        raise HTTPException(status_code=400, detail="CIF already registered")
    
    company_data = {
        "name": company.name,
        "cif": company.cif,
        "email": company.email,
        "description": company.description,
        "photo_url": company.photo_url
    }
    
    company = supabase.table("companies").insert(company_data).execute()
    
    if not company.data:
        raise HTTPException(status_code=500, detail="Error creating company")
        
    user_company_role_data = {
        "user_id": token.get("sub"), 
        "company_id": company.data[0]["id"],  
        "role": "admin"
    }
    
    supabase.table("user_company_roles").insert(user_company_role_data).execute()
    
    return company.data[0]

