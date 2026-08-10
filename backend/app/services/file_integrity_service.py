from sqlalchemy.orm import Session

from app.existing_modules.file_integrity_monitor import run_integrity_check
from app.schemas.file_integrity import FileIntegrityResult
from app.models.file_integrity import FileIntegrity
from app.services.alert_engine import check_file_integrity_for_alerts


def check_file_integrity(db: Session, folder_to_monitor: str, hash_file: str) -> FileIntegrityResult:
    """
    Calls the existing file integrity monitor, saves the summary to the
    database, generates alerts for changed/deleted files, and returns a
    validated FileIntegrityResult for the API.
    """
    raw_result = run_integrity_check(folder_to_monitor, hash_file)

    db_record = FileIntegrity(
        folder_checked=folder_to_monitor,
        new_files=",".join(raw_result["new_files"]),
        changed_files=",".join(raw_result["changed_files"]),
        deleted_files=",".join(raw_result["deleted_files"]),
    )
    db.add(db_record)
    db.commit()

    check_file_integrity_for_alerts(db, raw_result)

    return FileIntegrityResult(
        new_files=raw_result["new_files"],
        changed_files=raw_result["changed_files"],
        deleted_files=raw_result["deleted_files"],
    )