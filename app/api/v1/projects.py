from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectCreateResponse
from app.core.security import generate_api_key, get_api_key_hash
from app.middleware.auth import get_current_project

router = APIRouter()

@router.post("/", response_model=ProjectCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.name == project_in.name))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    raw_api_key = generate_api_key()
    hashed_key = get_api_key_hash(raw_api_key)
    
    new_project = Project(
        name=project_in.name,
        api_key_hash=hashed_key,
        config_json={}
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    
    response_data = ProjectCreateResponse.model_validate(new_project)
    response_data.api_key = raw_api_key
    return response_data

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, current_project: Project = Depends(get_current_project)):
    if current_project.id != project_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")
    return current_project

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID, 
    project_update: ProjectUpdate, 
    db: AsyncSession = Depends(get_db),
    current_project: Project = Depends(get_current_project)
):
    if current_project.id != project_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    
    if project_update.is_active is not None:
        current_project.is_active = project_update.is_active
    if project_update.config_json is not None:
        current_project.config_json = project_update.config_json
        
    await db.commit()
    await db.refresh(current_project)
    return current_project
