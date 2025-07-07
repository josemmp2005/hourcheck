import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt


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

def create_token(usuario:dict):
    payload = {
        "sub": usuario["id"],
        "email": usuario["email"],
        "role": usuario["role"],
        "active": usuario["active"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token