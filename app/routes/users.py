from fastapi import APIRouter, HTTPException
from app.db.supabase_client import supabase
from app.models.user import User, UserRegister, UserLogin
from app.utils.hash_password import hash_password, verify_password
from app.utils.jwt import create_token

router = APIRouter()

# Get all users
@router.get("/", response_model=list[User])
def get_users():
    response = supabase.table("users").select("*").execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error fetching users")
    
    return response.data

# This endpoint is used to register a new user
@router.post("/register", response_model=User)
def create_user(user: UserRegister):    
    existing_user = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "active": user.active,
        "photo_url": user.photo_url
    }
        
    response = supabase.table("users").insert(user_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating user")
    
    return response.data[0]


# User login endpoint 
@router.post("/login")
def user_login(user: UserLogin):
    response = supabase.table("users").select("*").eq("email", user.email).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid email")
        
    user_data = response.data[0]
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = create_token(user_data)
    
    return token
        