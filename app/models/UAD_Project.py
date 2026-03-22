import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text, func
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

from app.core.database import Base


class UADProject(Base):
    __tablename__ = "uad_projects"

    id = Column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    api_key = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    config_json = Column(
        Text,
        nullable=True
    )

    owner_user_id = Column(
        UNIQUEIDENTIFIER,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )