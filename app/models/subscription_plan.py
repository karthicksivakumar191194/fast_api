from sqlalchemy import Column, UUID, Integer, String, Text, DateTime, Numeric, func, Index, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum
import uuid

from app.db.database import Base

class SubscriptionPlanTypeEnum(Enum):
    FREE_PLAN = ("free_plan", "Free Plan")
    PAID_PLAN = ("paid_plan", "Paid Plan")
    CUSTOM_PLAN = ("custom_plan", "Custom Plan")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class SubscriptionPlanStatusEnum(Enum):
    DELETED = ("deleted", "Deleted")
    ACTIVE = ("active", "Active")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def list(cls):
        return list(cls)

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price_month_rupee = Column(Numeric(10, 2), nullable=False)
    price_year_rupee = Column(Numeric(10, 2), nullable=False)
    price_month_dollar = Column(Numeric(10, 2), nullable=False)
    price_year_dollar = Column(Numeric(10, 2), nullable=False)
    order = Column(Integer, default=0)
    details = Column(JSONB, default={})
    details_content = Column(JSONB, default=[])
    plan_type = Column(SqlEnum(SubscriptionPlanTypeEnum), nullable=False)
    expiry_days = Column(Integer, nullable=True)
    status = Column(SqlEnum(SubscriptionPlanStatusEnum), default=SubscriptionPlanStatusEnum.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    __table_args__ = (
        Index('idx_subscription_plans_name', 'name'),
        Index('idx_subscription_plans_plan_type', 'plan_type'),
    )
