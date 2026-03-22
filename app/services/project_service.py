import secrets
from sqlalchemy.orm import Session

from app.models.UAD_Project import UADProject
from app.schemas.project import ProjectCreate

def create_project(db: Session, project_in: ProjectCreate):
    api_key = "uad_live_" + secrets.token_urlsafe(32)

    project = UADProject(
        name=project_in.name,
        config_json=project_in.config_json,
        api_key=api_key
    )

    try:
        db.add(project)
        db.commit()
        db.refresh(project)
    except:
        db.rollback()
        raise

    return project