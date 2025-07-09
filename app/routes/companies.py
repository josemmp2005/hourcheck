from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.company import Company, CompanyCreate, CompanyUpdate, CompanySelection
from app.models.user import User
from app.utils.jwt import get_token_data, create_token


router = APIRouter()

# Create a new company, you must be authenticated and have a unique CIF
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

# Update an existing company, you must be authenticated, this endpoint update the token adding the company_id and role
@router.post("/select-company")
def select_company(selection: CompanySelection, token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", selection.company_id).execute()
    
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    user_data = supabase.table("users").select("*").eq("id", user_id).execute()
    if not user_data.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = user_data.data[0]
    role_info = user_company_role.data[0]
    
    token_data = {
        "id": user["id"],
        "email": user["email"],
        "active": user["active"],
        "company_id": selection.company_id,
        "role": role_info["role"]
    }
    
    new_token = create_token(token_data)
    
    return {
        "token": new_token,
        "company_id": selection.company_id,
        "role": role_info["role"]
    }

# This endpoint returns all company employees, you must be authenticated and have the role of admin or hr, you must select a company first, if
# not, it will raise an error because the token does not have the company_id and role
@router.get("/employees", response_model=list[User])
def get_employees(token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    company_id = token.get("company_id")
    user_role = token.get("role")
    
    if not user_id or not company_id:
        raise HTTPException(status_code=401, detail="Company context required - please select a company first")
    
    if user_role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="User does not have permission to view employees")
    
    employees = supabase.table("user_company_roles").select("*, users(*)").eq("company_id", company_id).execute()
    
    if not employees.data:
        return []
    
    users_data = []
    for employee in employees.data:
        if employee["users"]:
            user_info = employee["users"]
            user_info["role"] = employee["role"]
            users_data.append(user_info)
    
    return users_data

# This endpoint returns all companies the user is associated with, you must be authenticated
@router.get("/user-companies", response_model=list[dict])
def get_user_companies(token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_companies = supabase.table("user_company_roles").select("*, companies(*)").eq("user_id", user_id).execute()
    
    if not user_companies.data:
        return []
    
    companies_data = []
    for user_company in user_companies.data:
        company_info = {
            "company_id": user_company["company_id"],
            "role": user_company["role"],
            "company": user_company["companies"]
        }
        companies_data.append(company_info)
    
    return companies_data

