import os
from dotenv import load_dotenv
from supabase import create_client

# Cargar las variables de entorno desde el archivo .env en la raíz del proyecto
# Subir dos niveles desde app/db/ hasta la raíz del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    error_msg = []
    if not SUPABASE_URL:
        error_msg.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        error_msg.append("SUPABASE_KEY")
    
    raise Exception(
        f"Las siguientes variables de entorno deben estar configuradas en el archivo .env: {', '.join(error_msg)}\n"
        f"Archivo .env esperado en: {dotenv_path}\n"
        f"¿Existe el archivo .env? {os.path.exists(dotenv_path)}"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)