from fastapi import APIRouter, HTTPException
from app.db.supabase_client import supabase
from app.models.user import User, UserRegister, UserLogin
from app.utils.hash_password import hash_password, verify_password
from app.utils.jwt import create_token

router = APIRouter()

@router.get("/", response_model=list[User])
def get_users():
    response = supabase.table("users").select("*").execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error fetching users")
    
    return response.data

@router.post("/", response_model=User)
def create_user(user: UserRegister):
    # print(f"Received user registration request: {user}")
    
    existing_user = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": user.role,
        "active": user.active
    }
    
    # print(f"Creating user with data: {user_data}")
    
    response = supabase.table("users").insert(user_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Error creating user")
    
    # Retornar el usuario creado
    return response.data[0]


@router.post("/login")
def user_login(user: UserLogin):
    response = supabase.table("users").select("*").eq("email", user.email).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid email")
    
    # print(f"User found: {response.data[0]}")
    
    user_data = response.data[0]
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = create_token(user_data)
    
    return token
        
    
    
    
    
    
    
    