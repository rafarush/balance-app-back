import uuid
from datetime import datetime

from sqlalchemy import UUID, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import timezone
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(tz=timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(tz=timezone.utc),
                                                 onupdate=lambda: datetime.now(tz=timezone.utc))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()