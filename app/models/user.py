from sqlalchemy import Column, UUID, String, Boolean, DateTime, func, ForeignKey, Index, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
import uuid

from app.db.database import Base
from app.models import user_team_association, user_workspace_association, user_location_association


class UserStatusEnum(PyEnum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")
    INACTIVE = ("inactive", "Inactive")
    NOT_VERIFIED = ("not_verified", "Not Verified")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(30), nullable=False)
    password = Column(String(255), nullable=False)
    image = Column(String(512), nullable=True)
    designation = Column(String(255), nullable=False)
    is_account_owner = Column(Boolean, default=False)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.NOT_VERIFIED)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    role = relationship("Role", back_populates="users")
    teams = relationship("Team", secondary=user_team_association, back_populates="users")
    workspaces = relationship("Workspace", secondary=user_workspace_association, back_populates="users")
    locations = relationship("Location", secondary=user_location_association, back_populates="users")

    # Indexes
    __table_args__ = (
        Index('idx_user_tenant_id', 'tenant_id'),
        Index('idx_user_email', 'email'),
        Index('idx_user_phone_number', 'phone_number'),
    )
