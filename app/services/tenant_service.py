import re
from sqlalchemy.orm import Session

from app.models.tenant import Tenant, TenantStatusEnum
from app.utils.helpers import generate_random_string


def create_tenant(
        db: Session,
        is_verified: bool,
        company_name: str,
) -> Tenant:
    """
    Creates a new tenant with the provided details.
    If is_verified, create domain using company name & set the tenant status as active
    """
    domain = ""
    currency = "USD"
    status = TenantStatusEnum.NOT_VERIFIED

    if is_verified:
        domain = get_tenant_domain(db, company_name)
        status = TenantStatusEnum.ACTIVE

    # Create the tenant object with all provided details
    tenant = Tenant(
        company_name=company_name,
        domain=domain,
        currency=currency,
        status=status
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


def update_tenant(
        db: Session,
        tenant: Tenant,
        company_name: str) -> Tenant:
    """
    Updates the tenant by generating a unique domain using the company name.
    Sets the tenant status to active.
    """
    domain = get_tenant_domain(db, company_name)
    status = TenantStatusEnum.ACTIVE

    # Update tenant details
    tenant.company_name = company_name
    tenant.domain = domain
    tenant.status = status
    db.commit()
    db.refresh(tenant)

    return tenant


def get_tenant_domain(db: Session, tenant_name: str) -> str:
    """
    Generates a unique domain for the tenant based on the tenant name. If the domain
    already exists, it appends a random string to ensure uniqueness.
    """
    # Sanitize the tenant name to create a domain-friendly format
    formatted_tenant_name = tenant_name.lower()
    formatted_tenant_name = formatted_tenant_name.replace(" ", "-")

    # Remove any non-alphanumeric characters (except hyphens)
    domain = re.sub(r'[^a-z0-9-]', '', formatted_tenant_name)

    # Check if the generated domain already exists in the database
    existing_tenant = db.query(Tenant).filter(Tenant.domain == domain).first()

    # If the domain already exists, append a random string to make it unique
    while existing_tenant:
        domain = f"{domain}{generate_random_string(4)}"
        existing_tenant = db.query(Tenant).filter(Tenant.domain == domain).first()

    return domain
