from sqlalchemy.orm import Session
from app.models import Location

def create_default_location(db: Session, tenant_id: str,  workspace_id: str) -> Location:
    """
    Create the default location for the newly onboarded account.
    """
    location = Location(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        name="Default",
        is_default=True,
    )
    db.add(location)
    db.commit()
    db.refresh(location)

    return location
