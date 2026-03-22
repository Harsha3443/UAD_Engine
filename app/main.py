from fastapi import FastAPI
from app.api.v1 import projects, resources
from app.core.config import settings
from app.middleware.audit import AuditLogMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Unified Application Backend Engine"
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuditLogMiddleware)

app.include_router(projects.router, prefix=settings.API_V1_STR + "/projects", tags=["projects"])
app.include_router(resources.router, prefix=settings.API_V1_STR + "/resource", tags=["resources"])

@app.get("/")
def read_root():
    return {"message": "Welcome to UAD Engine built by Antigravity"}