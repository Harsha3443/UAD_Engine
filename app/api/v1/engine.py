from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.project import Project
from app.models.registry import ResourceRegistry
from app.schemas.engine import EngineResourceCreate, EngineResourceResponse
from app.middleware.auth import get_current_project

router = APIRouter()

@router.post("/resource", response_model=EngineResourceResponse, status_code=status.HTTP_201_CREATED)
async def define_engine_resource(
    schema_in: EngineResourceCreate,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    """
    Explicitly defines a rigid schema structure for a dynamic resource.
    Acts like Firestore's Security/Validation Rules registry.
    """
    result = await db.execute(
        select(ResourceRegistry).filter_by(
            project_id=current_project.id, 
            resource_name=schema_in.resource_name
        )
    )
    registry = result.scalars().first()
    
    if registry:
        registry.schema_definition = schema_in.schema_definition
    else:
        registry = ResourceRegistry(
            project_id=current_project.id,
            resource_name=schema_in.resource_name,
            schema_definition=schema_in.schema_definition
        )
        db.add(registry)
        
    await db.commit()
    await db.refresh(registry)
    return registry

@router.get("/resource", response_model=list[EngineResourceResponse])
async def list_engine_resources(
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ResourceRegistry).filter_by(project_id=current_project.id)
    )
    return result.scalars().all()
