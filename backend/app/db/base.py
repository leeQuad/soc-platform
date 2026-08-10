from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Shared declarative base for all SQLAlchemy models.

    Every model in app/models/ must inherit from this class so that
    Alembic (migrations) and metadata.create_all() can discover them.
    """
    pass