from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.alert import AlertResponse
from app.services.alert_engine import list_alerts
from app.core.security import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict  = Depends(get_current_user),
):
    """
    Returns the most recent alerts, newest first. Requires a valid JWT token.
    """
    return list_alerts(db, limit)