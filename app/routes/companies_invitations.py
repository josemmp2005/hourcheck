from fastapi import APIRouter, HTTPException, Depends
from app.db.supabase_client import supabase
from app.models.company_invitation import CompanyInvitation, CompanyInvitationCreate, CompanyInvitationVerify
from app.utils.jwt import get_token_data
from app.utils.email import send_email
from datetime import datetime, timedelta, timezone
import secrets
import string

router = APIRouter()

@router.post("/email/send", response_model=CompanyInvitation)
def send_email_invitation(invitation: CompanyInvitationCreate, token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    company_id = invitation.company_id
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", company_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with this company")
    
    user_role = user_company_role.data[0]["role"]
    if user_role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="User does not have permission to send invitations for this company")

    existing_invitation = supabase.table("company_invitations").select("*").eq("company_id", company_id).eq("email", invitation.email).eq("used", False).execute()
    if existing_invitation.data:
        raise HTTPException(status_code=400, detail="An active invitation already exists for this email")

    allowed_roles = ["employee", "admin", "hr"]
    if invitation.role not in allowed_roles:
        raise HTTPException(status_code=400, detail=f"Role must be one of: {', '.join(allowed_roles)}")

    alphabet = string.ascii_uppercase + string.digits
    max_attempts = 5
    
    for attempt in range(max_attempts):
        invitation_code = ''.join(secrets.choice(alphabet) for _ in range(10))
        
        existing_code = supabase.table("company_invitations").select("code").eq("company_id", company_id).eq("code", invitation_code).execute()
        if not existing_code.data:
            break
    else:
        raise HTTPException(status_code=500, detail="Could not generate unique invitation code")
    
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=1)
    invitation_data = {
        "company_id": invitation.company_id,
        "email": invitation.email,
        "code": invitation_code, 
        "role": invitation.role,
        "used": False,
        "expires_at": expires_at.isoformat()
    }
    
    try:
        response = supabase.table("company_invitations").insert(invitation_data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Error creating invitation")
    except Exception as e:
        print(f"Error inserting invitation: {e}")
        print(f"Invitation data: {invitation_data}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    try:
        send_email(invitation.email, invitation_code)
    except Exception as e:
        print(f"Error enviando email: {e}")
    
    return response.data[0]


@router.post("/code/verify", response_model=CompanyInvitation)
def verify_invitation_code(verification: CompanyInvitationVerify, token: dict = Depends(get_token_data)):
    if not verification.code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    response = supabase.table("company_invitations").select("*").eq("code", verification.code).eq("used", False).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Invitation code not found or already used")
    
    invitation = response.data[0]
    
    expires_at = datetime.fromisoformat(invitation["expires_at"]).replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=400, detail="Invitation code has expired")
    
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    existing = supabase.table("user_company_roles").select("*").eq("user_id", user_id).eq("company_id", invitation["company_id"]).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="User is already associated with this company")
    
    try:
        supabase.table("user_company_roles").insert({
            "user_id": user_id,
            "company_id": invitation["company_id"],
            "role": invitation["role"]
        }).execute()
        supabase.table("company_invitations").update({"used": True}).eq("id", invitation["id"]).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return invitation

@router.get("/code/generate", response_model=CompanyInvitation)
def generate_invitation_code(token: dict = Depends(get_token_data)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_company_role = supabase.table("user_company_roles").select("*").eq("user_id", user_id).execute()
    if not user_company_role.data:
        raise HTTPException(status_code=403, detail="User is not associated with any company")
    
    company_id = user_company_role.data[0]["company_id"]
    
    alphabet = string.ascii_uppercase + string.digits
    invitation_code = ''.join(secrets.choice(alphabet) for _ in range(10))
    
    expires_at = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    invitation_data = {
        "company_id": company_id,
        "email": None,
        "code": invitation_code,
        "role": "employee",
        "used": False,
        "expires_at": expires_at
    }
    
    try:
        response = supabase.table("company_invitations").insert(invitation_data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Error creating invitation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return response.data[0]
