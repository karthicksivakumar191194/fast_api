from sqlalchemy.orm import Session

from app.models import Workspace, Tenant, Location

def create_default_location(db: Session, tenant: Tenant,  workspace: Workspace) -> Location:
    """
    Create the default location under default workspace.
    """
    location = Location(
        tenant_id=tenant.id,
        workspace_id=workspace.id,
        name="Default",
        is_default=True,
    )
    db.add(location)
    db.commit()
    db.refresh(location)

    return location
