from datetime import datetime
from sqlmodel import SQLModel, Field

class WeatherReading(SQLModel, table = True):
    id: int = Field(default = None, primary_key = True)
    """Auto-generated unique identifier"""

    measuredAt: datetime
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
    """The wind direction in degrees (0 is north and 90 is east)."""

    outdoorDewPoint: float
    """The outdoor dew point in degrees celsius."""

    windChill: float
    """The wind chill factor in degrees celsius (it takes into account the effect of wind in cold environments feeling like as if it was colder)."""

    seaLevelAirPressure: float
    """What the air pressure would be at sea level in kPa."""

    allTimeRain: float
    """The total amount of rain since the device was reset, in millimeters."""

    rainSinceLastUpdate: float
    """The amount of rain that fell since the last update, in millimeters."""