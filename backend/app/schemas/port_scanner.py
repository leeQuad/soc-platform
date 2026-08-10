from pydantic import BaseModel


class PortScanResult(BaseModel):
    target: str
    start_port: int
    end_port: int
    open_ports: list[int]