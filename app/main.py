from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, companies, companies_invitations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(companies.router, prefix="/company", tags=["company"])
app.include_router(companies_invitations.router, prefix="/company-invitation", tags=["company-invitation"])