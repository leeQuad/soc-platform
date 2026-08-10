from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PortScan(Base):
    __tablename__ = "port_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target: Mapped[str] = mapped_column(String, nullable=False)
    start_port: Mapped[int] = mapped_column(Integer, nullable=False)
    end_port: Mapped[int] = mapped_column(Integer, nullable=False)
    open_ports: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)