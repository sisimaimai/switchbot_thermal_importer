import datetime
from pydantic import BaseModel, field_serializer
from typing import Optional

from utils import logger

LOGGER = logger.get_logger(__name__)


class ThermalInfo(BaseModel):
    device_id: str
    measured_at: datetime.datetime
    temperature: Optional[float]
    humidity: Optional[float]

    def validate(self):
        if self.temperature is None or self.humidity is None:
            LOGGER.warning(f"Attribute is set to None.")

    @field_serializer("measured_at")
    def serialize_dt(self, measured_at: datetime.datetime) -> str:
        return measured_at.replace(tzinfo=None).isoformat()  # タイムゾーンを削除してシリアライズ
