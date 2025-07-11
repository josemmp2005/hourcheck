from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, companies, companies_invitations, work_madalities, clock_entries, clock_issues, user_company_roles, absences

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
app.include_router(work_madalities.router, prefix="/work-madalities", tags=["work-madalities"])
app.include_router(clock_entries.router, prefix="/clock-entries", tags=["clock-entries"])
app.include_router(clock_issues.router, prefix="/clock-issues", tags=["clock-issues"])
app.include_router(user_company_roles.router, prefix="/user-company-roles", tags=["user-company-roles"])
app.include_router(absences.router, prefix="/absences", tags=["absences"])

