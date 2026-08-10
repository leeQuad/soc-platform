from datetime import datetime

from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LogParse(Base):
    __tablename__ = "log_parses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    log_file_path: Mapped[str] = mapped_column(String, nullable=False)
    success_count: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False)
    unique_suspicious_ips: Mapped[int] = mapped_column(Integer, nullable=False)
    most_attacked_ip: Mapped[str] = mapped_column(String, nullable=True)
    most_attacked_ip_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)