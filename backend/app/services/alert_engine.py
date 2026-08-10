from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.threat import Threat
import re


def create_alert(db: Session, source: str, severity: str, message: str) -> Alert:
    """
    Saves a new alert to the database, and escalates it to a Threat
    if it meets the HIGH severity criteria or shows a repeat-offender pattern.
    """
    alert = Alert(source=source, severity=severity, message=message)
    db.add(alert)
    db.commit()

    escalate_high_severity_alert(db, alert)
    check_repeat_offender(db, alert)

    return alert


def check_log_parse_for_alerts(db: Session, log_result: dict) -> None:
    """
    Inspects a log parse result and creates alerts for any suspicious IPs
    found, using the same severity levels the log parser already assigns.
    """
    for entry in log_result["suspicious_ips"]:
        clean_ip = entry["ip"].replace("ip=", "")
        create_alert(
            db,
            source="log_parser",
            severity=entry["level"],
            message=f"IP {clean_ip} made {entry['count']} failed login attempts",
        )


def check_file_integrity_for_alerts(db: Session, integrity_result: dict) -> None:
    """
    Inspects a file integrity result and creates alerts for any changed
    or deleted files (new files are informational, not alerted on).
    """
    for filename in integrity_result["changed_files"]:
        create_alert(
            db,
            source="file_integrity",
            severity="MEDIUM",
            message=f"File '{filename}' was modified",
        )

    for filename in integrity_result["deleted_files"]:
        create_alert(
            db,
            source="file_integrity",
            severity="HIGH",
            message=f"File '{filename}' was deleted",
        )
def list_alerts(db: Session, limit: int = 50):
    """
    Returns the most recent alerts, newest first.
    """
    return db.query(Alert).order_by(Alert.created_at.desc()).limit(limit).all()
from app.models.threat import Threat


def escalate_high_severity_alert(db: Session, alert: Alert) -> None:
    """
    If an alert is HIGH severity, automatically creates a corresponding
    Threat record, flagging it for priority attention.
    """
    if alert.severity == "HIGH":
        threat = Threat(
            alert_id=alert.id,
            reason="HIGH severity alert auto-escalated",
        )
        db.add(threat)
        db.commit()
def extract_ip(message: str) -> str | None:
    """
    Pulls an IPv4 address out of an alert message, if present.
    Returns None if no IP pattern is found (e.g. file integrity alerts).
    """
    match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", message)
    return match.group(0) if match else None


def check_repeat_offender(db: Session, alert: Alert) -> None:
    """
    If the same IP has appeared in 3 or more alerts, escalate it as a
    repeat-offender threat (in addition to any single-alert HIGH escalation).
    """
    ip = extract_ip(alert.message)
    if not ip:
        return

    matching_alerts = db.query(Alert).filter(Alert.message.contains(ip)).all()

    if len(matching_alerts) >= 3:
        already_flagged = (
            db.query(Threat)
            .filter(Threat.reason == f"Repeat offender: {ip} appeared in 3+ alerts")
            .first()
        )
        if not already_flagged:
            threat = Threat(
                alert_id=alert.id,
                reason=f"Repeat offender: {ip} appeared in 3+ alerts",
            )
            db.add(threat)
            db.commit()

def list_threats(db: Session, limit: int = 50):
    """
    Returns the most recent escalated threats, newest first.
    """
    return db.query(Threat).order_by(Threat.created_at.desc()).limit(limit).all()