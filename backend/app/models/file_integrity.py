from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class FileIntegrity(Base):
    __tablename__ = "file_integrity_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    folder_checked: Mapped[str] = mapped_column(String, nullable=False)
    new_files: Mapped[str] = mapped_column(String, nullable=False)
    changed_files: Mapped[str] = mapped_column(String, nullable=False)
    deleted_files: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)