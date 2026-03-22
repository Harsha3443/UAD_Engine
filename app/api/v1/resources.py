from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.project import Project
from app.models.registry import DynamicRecord, ResourceRegistry
from app.schemas.resource import DynamicRecordCreate, DynamicRecordUpdate, DynamicRecordResponse
from app.middleware.auth import get_current_project

router = APIRouter()

async def ensure_resource_registered(db: AsyncSession, project_id: UUID, resource_name: str):
    result = await db.execute(
        select(ResourceRegistry).filter_by(project_id=project_id, resource_name=resource_name)
    )
    if not result.scalars().first():
        new_registry = ResourceRegistry(project_id=project_id, resource_name=resource_name)
        db.add(new_registry)
        await db.flush()

@router.post("/{resource_name}", response_model=DynamicRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    resource_name: str,
    record_in: DynamicRecordCreate,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    await ensure_resource_registered(db, current_project.id, resource_name)
    
    new_record = DynamicRecord(
        project_id=current_project.id,
        resource_name=resource_name,
        data=record_in.data
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

@router.get("/{resource_name}", response_model=List[DynamicRecordResponse])
async def list_records(
    resource_name: str,
    skip: int = 0,
    limit: int = 100,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DynamicRecord)
        .filter_by(project_id=current_project.id, resource_name=resource_name)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/{resource_name}/{record_id}", response_model=DynamicRecordResponse)
async def get_record(
    resource_name: str,
    record_id: UUID,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DynamicRecord).filter_by(id=record_id, project_id=current_project.id, resource_name=resource_name)
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{resource_name}/{record_id}", response_model=DynamicRecordResponse)
async def update_record(
    resource_name: str,
    record_id: UUID,
    record_in: DynamicRecordUpdate,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DynamicRecord).filter_by(id=record_id, project_id=current_project.id, resource_name=resource_name)
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    record.data = record_in.data
    await db.commit()
    await db.refresh(record)
    return record

@router.delete("/{resource_name}/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    resource_name: str,
    record_id: UUID,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DynamicRecord).filter_by(id=record_id, project_id=current_project.id, resource_name=resource_name)
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    await db.delete(record)
    await db.commit()
    return None
