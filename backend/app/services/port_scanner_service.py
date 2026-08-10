from sqlalchemy.orm import Session

from app.existing_modules.port_scanner import scan_ports
from app.schemas.port_scanner import PortScanResult
from app.models.port_scan import PortScan


def run_port_scan(
    db: Session,
    target: str,
    start_port: int = 1,
    end_port: int = 1000,
    timeout: float = 0.5,
) -> PortScanResult:
    """
    Runs the existing port scanner, saves the result to the database,
    and returns a validated PortScanResult for the API to send back.
    """
    open_ports = scan_ports(target, start_port, end_port, timeout)

    db_record = PortScan(
        target=target,
        start_port=start_port,
        end_port=end_port,
        open_ports=",".join(str(p) for p in open_ports),
    )
    db.add(db_record)
    db.commit()

    return PortScanResult(
        target=target,
        start_port=start_port,
        end_port=end_port,
        open_ports=open_ports,
    )