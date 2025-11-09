from dataclasses import dataclass, field
from datetime import datetime
from math import floor

@dataclass
class Report:
    """Represents a weather report."""

    id: int = field(init = False)
    """Auto-generated unique identifier (calculated from the date and time of the report)"""

    datetime: datetime
    """Date and time when the weather data was read from the weather station."""

    indoorTemperature: float
    """The indoor temperature in degrees celsius."""

    indoorHumidity: float
    """The indoor relative humidity in percentages."""

    outdoorTemperature: float
    """The outdoor temperature in degrees celsius."""

    outdoorHumidity: float
    """The outdoor relative humidity in percentages."""

    windSpeed: float
    """The wind speed in kilometers per hour (wind speed averaged over a 2 minute period)."""

    gustSpeed: float
    """The gust speed in kilometers per hour (wind speed averaged over a 20 second period)."""
    
    windDirection: float
    """The wind direction in degrees (0 is north)."""

    outdoorDewPoint: float
    """The outdoor dew point in degrees celsius."""

    windChill: float
    """The wind chill factor in degrees celsius (it takes into account the effect of wind in cold environments feeling like as if it was colder)."""

    seaLevelAirPressure: float
    """What the air pressure would be at sea level."""

    totalRain: float
    """The total amount of rain since the device was reset in millimeters."""

    rainSinceLastUpdate: float
    """The amount of rain that fell since the last update in millimeters."""

    def __post_init__(self):
        self.id = floor(self.datetime.timestamp() * 1000 + self.datetime.microsecond / 1000)