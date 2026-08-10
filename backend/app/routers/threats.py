from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.threat import ThreatResponse
from app.services.alert_engine import list_threats
from app.core.security import require_admin


router = APIRouter(prefix="/threats", tags=["Threats"])


@router.get("/", response_model=List[ThreatResponse])
def get_threats(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """
    Returns the most recent escalated threats, newest first. Requires a valid JWT token.
    """
    return list_threats(db, limit)