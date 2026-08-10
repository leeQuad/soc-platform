from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.file_integrity import FileIntegrityResult
from app.services.file_integrity_service import check_file_integrity
from app.core.security import get_current_user

router = APIRouter(prefix="/integrity", tags=["File Integrity"])


@router.post("/check", response_model=FileIntegrityResult)
def check_integrity(
    folder_to_monitor: str,
    hash_file: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Checks the given folder for new, changed, or deleted files
    compared to the last saved snapshot, and saves the summary.
    Requires a valid JWT token.
    """
    return check_file_integrity(db, folder_to_monitor, hash_file)