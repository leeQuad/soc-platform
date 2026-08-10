from datetime import datetime

from pydantic import BaseModel


class ThreatResponse(BaseModel):
    id: int
    alert_id: int
    reason: str
    created_at: datetime

    model_config = {"from_attributes": True}