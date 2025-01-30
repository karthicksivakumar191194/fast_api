from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, func, Index, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from app.db.database import Base

class RoleStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(SqlEnum(RoleStatusEnum), default=RoleStatusEnum.ACTIVE, nullable=False)
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', backref='roles', lazy=True)
    team = relationship('Team', backref='roles', lazy=True)
    parent_role = relationship('Role', backref='sub_roles', lazy=True)

    __table_args__ = (
        Index('idx_roles_user_id', 'user_id'),
        Index('idx_roles_team_id', 'team_id'),
        Index('idx_roles_name', 'name'),
        Index('idx_roles_parent_role_id', 'parent_role_id'),
    )
