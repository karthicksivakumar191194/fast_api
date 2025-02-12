from sqlalchemy.orm import Session
from app.models import Tenant, Workspace

def create_default_workspace(db: Session, tenant: Tenant) -> Workspace:
    """
    Create the default workspace for the tenant.
    """
    workspace = Workspace(
        tenant_id=tenant.id,
        name="Default",
        is_default=True,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    return workspace
