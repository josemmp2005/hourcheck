import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Validar que todas las variables estén configuradas
if not SECRET_KEY:
    raise Exception("SECRET_KEY debe estar configurada en el archivo .env")
if not ALGORITHM:
    raise Exception("ALGORITHM debe estar configurada en el archivo .env")
if not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise Exception("ACCESS_TOKEN_EXPIRE_MINUTES debe estar configurada en el archivo .env")

security = HTTPBearer()

def create_token(usuario:dict):
    payload = {
        "sub": usuario["id"],
        "email": usuario["email"],
        "active": usuario["active"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_token_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")