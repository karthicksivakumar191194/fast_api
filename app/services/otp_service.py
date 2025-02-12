from uuid import UUID
from sqlalchemy.orm import Session

from app.exceptions import NotFound, BadRequest
from app.models.tenant import Tenant, TenantStatusEnum


def generate_tenant_verification_otp(db: Session, tenant: Tenant) -> str:
    """
    Generate & Save Tenant Verification OTP.
    """
    tenant.generate_otp()

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant.otp


def validate_tenant_verification_otp(tenant: Tenant, otp: str) -> str:
    """
    Validate Tenant Verification OTP.
    """
    # Check if the OTP is invalid or expired
    if tenant.otp != otp or tenant.is_otp_expired():
        raise BadRequest("Invalid OTP.")

    return "Valid OTP."

