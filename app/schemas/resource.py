from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class DynamicRecordCreate(BaseModel):
    data: Dict[str, Any]

class DynamicRecordUpdate(BaseModel):
    data: Dict[str, Any]

class DynamicRecordResponse(BaseModel):
    id: UUID
    project_id: UUID
    resource_name: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
