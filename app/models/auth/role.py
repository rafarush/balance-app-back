from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.auth.role_policy import RolePolicy


class Role(Base):
    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="role",
                                               cascade="all, delete-orphan")
    policies: Mapped[list["Policy"]] = relationship(
        secondary=RolePolicy.__table__,
        primaryjoin="Role.id == RolePolicy.role_id",
        secondaryjoin="Policy.id == RolePolicy.policy_id"
    )
