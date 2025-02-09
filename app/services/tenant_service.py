from sqlalchemy.orm import Session
from app.models import Tenant, TenantStatusEnum
from app.utils.helpers import generate_random_string
import re


def create_tenant(
        db: Session,
        company_name: str,
        company_website: str,
        company_size: str,
        company_location: str,
        industry_type: str,
        date_format: str,
        time_format: str,
        time_zone: str,
        is_verified: bool
) -> Tenant:
    """
    Creates a new tenant with the provided details.
    """

    # Generate a unique domain for the tenant using the company name
    domain = get_tenant_domain(db, company_name)

    # Set tenant status based on the verification flag
    status = TenantStatusEnum.NOT_VERIFIED
    if is_verified:
        status = TenantStatusEnum.ACTIVE

    # Create the tenant object with all provided details
    tenant = Tenant(
        company_name=company_name,
        company_website=company_website,
        company_size=company_size,
        company_location=company_location,
        industry_type=industry_type,
        date_format=date_format,
        time_format=time_format,
        time_zone=time_zone,
        domain=domain,
        status=status
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


def get_tenant_domain(db: Session, company_name: str) -> str:
    """
    Generates a unique domain for the tenant based on the company name. If the domain
    already exists, it appends a random string to ensure uniqueness.
    """
    # Sanitize the company name to create a domain-friendly format
    formatted_company_name = company_name.lower()
    formatted_company_name = formatted_company_name.replace(" ", "-")

    # Remove any non-alphanumeric characters (except hyphens)
    domain = re.sub(r'[^a-z0-9-]', '', formatted_company_name)

    # Check if the generated domain already exists in the database
    existing_tenant = db.query(Tenant).filter(Tenant.domain == domain).first()

    # If the domain already exists, append a random string to make it unique
    while existing_tenant:
        domain = f"{domain}{generate_random_string(4)}"
        existing_tenant = db.query(Tenant).filter(Tenant.domain == domain).first()

    return domain
