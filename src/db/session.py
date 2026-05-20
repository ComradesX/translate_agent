from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config.database_config import DatabaseConfig


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DatabaseConfig.database_url(),
    poolclass=QueuePool,
    pool_size=DatabaseConfig.pool_size(),
    max_overflow=DatabaseConfig.max_overflow(),
    pool_timeout=DatabaseConfig.pool_timeout(),
    pool_recycle=DatabaseConfig.pool_recycle(),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
