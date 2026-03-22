from pydantic import BaseModel, ConfigDict
from typing import Dict

class EngineResourceCreate(BaseModel):
    resource_name: str
    schema_definition: Dict[str, str]

class EngineResourceResponse(BaseModel):
    resource_name: str
    schema_definition: Dict[str, str]
    
    model_config = ConfigDict(from_attributes=True)
