from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from uuid import UUID

from app.models.registry import ResourceRegistry

class ResourceResolver:
    """
    Acts as the main registry router. In a massive multi-tenant environment, this service 
    looks up the project schema mapping and injects execution rules for the CRUD Engine.
    """
    @staticmethod
    async def resolve_or_create(db: AsyncSession, project_id: UUID, resource_name: str) -> ResourceRegistry:
        result = await db.execute(
            select(ResourceRegistry).filter_by(project_id=project_id, resource_name=resource_name)
        )
        registry = result.scalars().first()
        
        if not registry:
            # Auto-create loosely without strict schema
            registry = ResourceRegistry(
                project_id=project_id,
                resource_name=resource_name,
                schema_definition={}
            )
            db.add(registry)
            await db.commit()
            await db.refresh(registry)
            
        return registry

    @staticmethod
    async def get_schema(db: AsyncSession, project_id: UUID, resource_name: str) -> dict:
        registry = await ResourceResolver.resolve_or_create(db, project_id, resource_name)
        return registry.schema_definition
