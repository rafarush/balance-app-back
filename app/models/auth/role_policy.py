import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RolePolicy(Base):
    __tablename__ = 'role_policy'

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("role.id"), primary_key=True, default=uuid.uuid4)
    policy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("policy.id"), primary_key=True, default=uuid.uuid4)
