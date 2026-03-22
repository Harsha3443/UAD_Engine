from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.project import Project
from app.core.security import get_api_key_hash

async def get_current_project(
    x_api_key: str = Header(..., description="API Key for the project"),
    db: AsyncSession = Depends(get_db)
) -> Project:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API Key header missing")
        
    hashed_key = get_api_key_hash(x_api_key)
    
    result = await db.execute(select(Project).filter(Project.api_key_hash == hashed_key))
    project = result.scalars().first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    if not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project is inactive"
        )

    return project
