from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.types import JSON
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    api_key_hash = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    config_json = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
