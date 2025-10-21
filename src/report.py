from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from math import floor

@dataclass
class Report:
    id: int = field(init = False)
    date: datetime
    indoorTemperature: float
    indoorHumidity: float
    outdoorTemperature: float
    outdoorHumidity: float
    windSpeed: float
    gustSpeed: float
    windDirection: float
    dewPoint: float
    windChill: float
    relativeAirPressure: float
    rain: Optional[float]

    def __post_init__(self):
        self.id = floor(self.date.timestamp() * 1000 + self.date.microsecond / 1000)