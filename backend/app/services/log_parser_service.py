from sqlalchemy.orm import Session

from app.existing_modules.log_parser import parse_logs
from app.schemas.log_parser import LogParseResult
from app.models.log_parse import LogParse
from app.services.alert_engine import check_log_parse_for_alerts


def analyze_log_file(db: Session, log_file_path: str) -> LogParseResult:
    """
    Calls the existing log parser, saves the summary to the database,
    generates alerts for suspicious IPs, and returns a validated
    LogParseResult object the API can safely return.
    """
    raw_result = parse_logs(log_file_path, report_path=None)

    db_record = LogParse(
        log_file_path=log_file_path,
        success_count=raw_result["success_count"],
        failed_count=raw_result["failed_count"],
        total_attempts=raw_result["total_attempts"],
        success_rate=raw_result["success_rate"],
        unique_suspicious_ips=raw_result["unique_suspicious_ips"],
        most_attacked_ip=raw_result["most_attacked_ip"],
        most_attacked_ip_count=raw_result["most_attacked_ip_count"],
    )
    db.add(db_record)
    db.commit()

    check_log_parse_for_alerts(db, raw_result)

    return LogParseResult(
        success_count=raw_result["success_count"],
        failed_count=raw_result["failed_count"],
        total_attempts=raw_result["total_attempts"],
        success_rate=raw_result["success_rate"],
        unique_suspicious_ips=raw_result["unique_suspicious_ips"],
        most_attacked_ip=raw_result["most_attacked_ip"],
        most_attacked_ip_count=raw_result["most_attacked_ip_count"],
        suspicious_ips=raw_result["suspicious_ips"],
    )