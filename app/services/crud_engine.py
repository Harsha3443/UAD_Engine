from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Dict, Any, List

from app.models.registry import DynamicRecord
from app.services.resource_resolver import ResourceResolver
from app.services.schema_validator import SchemaValidator
from fastapi import HTTPException

class CRUDEngine:
    """
    The heart of the Dynamic Storage platform. Only executes operations after
    perfect API Key validation binding and schema enforcement. 
    """
    @staticmethod
    async def create_record(db: AsyncSession, project_id: UUID, resource_name: str, payload: Dict[str, Any]) -> DynamicRecord:
        schema = await ResourceResolver.get_schema(db, project_id, resource_name)
        SchemaValidator.validate_payload(schema, payload)
        
        new_record = DynamicRecord(
            project_id=project_id,
            resource_name=resource_name,
            data=payload
        )
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
        return new_record

    @staticmethod
    async def get_records(db: AsyncSession, project_id: UUID, resource_name: str, skip: int = 0, limit: int = 100) -> List[DynamicRecord]:
        result = await db.execute(
            select(DynamicRecord)
            .filter_by(project_id=project_id, resource_name=resource_name)
            .offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_record(db: AsyncSession, project_id: UUID, resource_name: str, record_id: UUID) -> DynamicRecord:
        result = await db.execute(
            select(DynamicRecord).filter_by(id=record_id, project_id=project_id, resource_name=resource_name)
        )
        record = result.scalars().first()
        if not record:
            raise HTTPException(status_code=404, detail="Resource record not found")
        return record

    @staticmethod
    async def update_record(db: AsyncSession, project_id: UUID, resource_name: str, record_id: UUID, payload: Dict[str, Any]) -> DynamicRecord:
        schema = await ResourceResolver.get_schema(db, project_id, resource_name)
        SchemaValidator.validate_payload(schema, payload)
        
        record = await CRUDEngine.get_record(db, project_id, resource_name, record_id)
        record.data = payload
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def delete_record(db: AsyncSession, project_id: UUID, resource_name: str, record_id: UUID) -> None:
        record = await CRUDEngine.get_record(db, project_id, resource_name, record_id)
        await db.delete(record)
        await db.commit()
