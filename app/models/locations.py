from sqlalchemy import Column, UUID, ForeignKey, String, DateTime, func, Index, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from app.db.database import Base

class LocationStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(SqlEnum(LocationStatusEnum), default=LocationStatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='locations', lazy=True)

    __table_args__ = (
        Index('idx_locations_tenant_id', 'tenant_id'),
        Index('idx_locations_name', 'name'),
    )
