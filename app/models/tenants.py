from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, func, Index, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from app.db.database import Base

class TenantStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")
    IN_ACTIVE = ("in_active", "In Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    current_subscription_plan = Column(UUID(as_uuid=True), ForeignKey('tenant_subscription_history.id', ondelete='SET NULL'))
    status = Column(SqlEnum(TenantStatusEnum), default=TenantStatusEnum.ACTIVE,nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    subscription_history = relationship('TenantSubscriptionHistory', backref='tenant', lazy=True)

    __table_args__ = (
        Index('idx_tenants_name', 'name'),
        Index('idx_tenants_current_subscription_plan', 'current_subscription_plan'),
    )
