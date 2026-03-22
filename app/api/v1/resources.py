from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.project import Project
from app.schemas.resource import DynamicRecordCreate, DynamicRecordUpdate, DynamicRecordResponse
from app.middleware.auth import get_current_project
from app.services.crud_engine import CRUDEngine

router = APIRouter()

@router.post("/{resource_name}", response_model=DynamicRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    resource_name: str,
    record_in: DynamicRecordCreate,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    return await CRUDEngine.create_record(db, current_project.id, resource_name, record_in.data)

@router.get("/{resource_name}", response_model=List[DynamicRecordResponse])
async def list_records(
    resource_name: str,
    skip: int = 0,
    limit: int = 100,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    return await CRUDEngine.get_records(db, current_project.id, resource_name, skip, limit)

@router.get("/{resource_name}/{record_id}", response_model=DynamicRecordResponse)
async def get_record(
    resource_name: str,
    record_id: UUID,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    return await CRUDEngine.get_record(db, current_project.id, resource_name, record_id)

@router.put("/{resource_name}/{record_id}", response_model=DynamicRecordResponse)
async def update_record(
    resource_name: str,
    record_id: UUID,
    record_in: DynamicRecordUpdate,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    return await CRUDEngine.update_record(db, current_project.id, resource_name, record_id, record_in.data)

@router.delete("/{resource_name}/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    resource_name: str,
    record_id: UUID,
    current_project: Project = Depends(get_current_project),
    db: AsyncSession = Depends(get_db)
):
    await CRUDEngine.delete_record(db, current_project.id, resource_name, record_id)
