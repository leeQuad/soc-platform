from pydantic import BaseModel


class SuspiciousIP(BaseModel):
    ip: str
    count: int
    level: str
    first_seen: str

class LogParseResult(BaseModel):
    success_count: int
    failed_count: int
    total_attempts: int
    success_rate: float
    unique_suspicious_ips: int
    most_attacked_ip: str | None
    most_attacked_ip_count: int
    suspicious_ips: list[SuspiciousIP]