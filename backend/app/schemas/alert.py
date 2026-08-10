from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int
    source: str
    severity: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}