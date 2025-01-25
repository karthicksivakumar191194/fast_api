from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, func, Index, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from app.db.database import Base

class TeamStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(SqlEnum(TeamStatusEnum), default=TeamStatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    tenant = relationship('Tenant', backref='teams', lazy=True)
    location = relationship('Location', backref='teams', lazy=True)

    __table_args__ = (
        Index('idx_teams_tenant_id', 'tenant_id'),
        Index('idx_teams_location_id', 'location_id'),
        Index('idx_teams_name', 'name'),
    )
