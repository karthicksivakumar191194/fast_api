from sqlalchemy.orm import Session

from app.models import Tenant, Role


def create_default_roles(db: Session, tenant: Tenant) -> None:
    """
    Create the default roles(Admin, Manager, Operator, Sales, Technician)  for the tenant.
    """
    default_roles = [
        Role(
            tenant_id=tenant.id,
            name='Admin',
            is_default=True,
        ),
        Role(
            tenant_id=tenant.id,
            name='Manager',
            is_default=False,
        ),
        Role(
            tenant_id=tenant.id,
            name='Operator',
            is_default=False,
        ),
        Role(
            tenant_id=tenant.id,
            name='Sales',
            is_default=False,
        ),
        Role(
            tenant_id=tenant.id,
            name='Technician',
            is_default=False,
        ),
    ]

    # Bulk insert the roles into the database
    db.bulk_save_objects(default_roles)
    db.commit()

