from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.log_parser import LogParseResult
from app.services.log_parser_service import analyze_log_file
from app.core.security import get_current_user

router = APIRouter(prefix="/logs", tags=["Log Parser"])


@router.post("/parse", response_model=LogParseResult)
def parse_log_file(
    log_file_path: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Parses the given log file for suspicious login activity and saves
    the summary to the database. Requires a valid JWT token.
    """
    return analyze_log_file(db, log_file_path)