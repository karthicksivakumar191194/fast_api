from sqlalchemy.orm import Session
from app.models import Workspace

def create_default_workspace(db: Session, tenant_id: str) -> Workspace:
    """
    Create the default workspace for the newly onboarded account.
    """
    workspace = Workspace(
        tenant_id=tenant_id,
        name="Default",
        is_default=True,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace
