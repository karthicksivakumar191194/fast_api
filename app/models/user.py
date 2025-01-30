from sqlalchemy import Column, UUID, String, DateTime, func, Index, Enum as SqlEnum
from enum import Enum
import uuid

from app.db.database import Base

class UserStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")
    InACTIVE = ("in_active", "In Active")
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
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone_number = Column(String(15), nullable=False)
    password = Column(String(255), nullable=False)
    status = Column(SqlEnum(UserStatusEnum), default=UserStatusEnum.NOT_VERIFIED, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_phone_number', 'phone_number'),
    )
