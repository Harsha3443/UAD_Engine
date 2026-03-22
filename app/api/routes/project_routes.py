from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.project import ProjectCreate, ProjectRead,ProjectCreateResponse
from app.core.database import get_db
from app.services.project_service import create_project

from app.core.security import get_current_project
from app.models.UAD_Project import UADProject


router = APIRouter()

@router.post("/projects", response_model=ProjectCreateResponse)
def create_project_endpoint(
    project_in: ProjectCreate,
    db: Session = Depends(get_db)
):
    project = create_project(db, project_in)
    return project

@router.get("/me", response_model=ProjectRead)
def get_current_project_endpoint(
    project: UADProject = Depends(get_current_project)
):
    return project