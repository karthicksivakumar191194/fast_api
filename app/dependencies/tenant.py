from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Tenant, TenantStatusEnum
from app.exceptions import NotFound


def get_not_verified_tenant(db: Session, tenant_id: UUID) -> Tenant:
    """
    Dependency to fetch tenant by ID and check if it's not_verified (i.e., NOT_VERIFIED).
    Raises HTTPException if tenant is not found or not_verified.
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id,
                                     Tenant.status == TenantStatusEnum.NOT_VERIFIED).first()

    if not tenant:
        raise NotFound("Tenant not found")

    return tenant
