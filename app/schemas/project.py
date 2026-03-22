from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    is_active: Optional[bool] = None
    config_json: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    is_active: bool
    config_json: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ProjectCreateResponse(ProjectResponse):
    api_key: str  # Only returned once on creation