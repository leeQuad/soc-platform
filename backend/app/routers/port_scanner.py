from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.port_scanner import PortScanResult
from app.services.port_scanner_service import run_port_scan
from app.core.security import get_current_user

router = APIRouter(prefix="/scan", tags=["Port Scanner"])


@router.post("/", response_model=PortScanResult)
def scan_target(
    target: str,
    start_port: int = 1,
    end_port: int = 1000,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Runs a port scan against the given target and saves the result.
    Requires a valid JWT token.
    """
    return run_port_scan(db, target, start_port, end_port)