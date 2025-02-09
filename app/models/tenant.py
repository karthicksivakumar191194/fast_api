from sqlalchemy import Column, UUID, String, Text, DateTime, Boolean, func, Index, Enum
from enum import Enum as PyEnum
import uuid

from app.db.database import Base

class TenantStatusEnum(PyEnum):
    DELETED = "deleted"
    ACTIVE = "active"
    IN_ACTIVE = "in_active"
    NOT_VERIFIED = "not_verified"

    def __init__(self, value):
        self._value_ = value

    @classmethod
    def list(cls):
        return list(cls)

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    company_website = Column(String(255), nullable=True)
    company_logo = Column(String(512), nullable=True)
    company_size = Column(String(255), nullable=True)
    company_location = Column(Text, nullable=False)
    industry_type = Column(String(255), nullable=True)
    domain = Column(String(255), nullable=False)
    primary_language = Column(String(50), default="en", nullable=False)  # Example: 'en', 'fr', etc.
    date_format = Column(String(50), nullable=False)
    time_format = Column(String(50), nullable=False)
    time_zone = Column(String(50), nullable=False)
    currency = Column(String(3), nullable=False)
    enable_two_factor = Column(Boolean, default=False)
    status = Column(Enum(TenantStatusEnum), default=TenantStatusEnum.NOT_VERIFIED)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Indexes
    __table_args__ = (
        Index('idx_tenant_company_name', 'company_name'),
        Index('idx_tenant_domain', 'domain'),
        Index('idx_tenant_status', 'status'),
    )
