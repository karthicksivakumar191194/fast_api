from sqlalchemy.orm import Session

from app.models import Tenant, Workspace, Location, Team

def create_default_team(db: Session, tenant: Tenant,  workspace: Workspace, location: Location) -> Team:
    """
    Create the default team under default workspace & default location.
    """
    team = Team(
        tenant_id=tenant.id,
        workspace_id=workspace.id,
        name="Default",
        is_default=True,
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    # TODO - Map team to default location

    return team
