from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.types import JSON
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class ResourceRegistry(Base):
    __tablename__ = "resource_registry"

    project_id = Column(UNIQUEIDENTIFIER(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    resource_name = Column(String(255), primary_key=True)
    schema_definition = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DynamicRecord(Base):
    __tablename__ = "dynamic_records"

    id = Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UNIQUEIDENTIFIER(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True, nullable=False)
    resource_name = Column(String(255), index=True, nullable=False)
    data = Column(JSON, default={}, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
