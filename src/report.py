from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import ClassVar
from math import floor

@dataclass
class Report:
    """Represents a weather report."""
    reportsInLastHour: ClassVar[list["Report"]] = []
    reportsInLast24Hours: ClassVar[list["Report"]] = []

    def getRainDuringTimeDelta(reports: list["Report"], timeDelta: timedelta):
        currentDatetime = datetime.now()
        hourlyRain = 0
        for i, report in reversed(tuple(enumerate(reports))):
            if currentDatetime - report.datetime > timeDelta:
                reports.pop(i)
            else:
                hourlyRain += report.rainSinceLastUpdate

        return hourlyRain
    
    def getRainInLastHour():
        """Returns the amount of rain that fell in the last hour in millimeters"""
        return Report.getRainDuringTimeDelta(Report.reportsInLastHour, timedelta(hours = 1))

    def getRainInLast24Hours():
        """Returns the amount of rain that fell in the last 24 hours in millimeters"""
        return Report.getRainDuringTimeDelta(Report.reportsInLast24Hours, timedelta(hours = 24))

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

    allTimeRain: float
    """The total amount of rain since the device was reset in millimeters."""

    rainSinceLastUpdate: float
    """The amount of rain that fell since the last update in millimeters."""

    def __post_init__(self):
        self.id = floor(self.datetime.timestamp() * 1000 + self.datetime.microsecond / 1000)

        Report.reportsInLastHour.append(self)
        Report.reportsInLast24Hours.append(self)

    def isValid(self, previousReport: "Report"):
        fieldValidities = [
            -100 <= self.indoorTemperature <= 100,
            0 <= self.indoorHumidity <= 100,
            -100 <= self.outdoorTemperature <= 100,
            0 <= self.outdoorHumidity <= 100,
            self.windSpeed >= 0,
            self.gustSpeed >= 0,
            0 <= self.windDirection < 360,
            750 <= self.seaLevelAirPressure <= 1250,
            self.allTimeRain >= 0,
            self.rainSinceLastUpdate >= 0
        ]
        if not all(fieldValidities):
            return False
        
        if self.datetime - previousReport.datetime > timedelta(minutes = 2):
            return True
        
        differenceValidities = [
            abs(self.indoorTemperature - previousReport.indoorTemperature) <= 5,
            abs(self.indoorHumidity - previousReport.indoorHumidity) <= 25,
            abs(self.outdoorTemperature - previousReport.outdoorTemperature) <= 2.5,
            abs(self.outdoorHumidity - previousReport.outdoorHumidity) <= 20,
            abs(self.allTimeRain - previousReport.allTimeRain) <= 10
        ]
        if not all(differenceValidities):
            return False
        
        return True