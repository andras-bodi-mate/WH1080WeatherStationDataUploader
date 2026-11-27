import logging
from http.client import OK, responses

import requests

from config import Config
from weatherReading import WeatherReading

logger: logging.Logger = logging.getLogger(__name__)


class ReadingUploader:
    def __init__(self, config: Config, username: str, password: str):
        self.frequency = config.uploadFrequency
        self.localPort = config.uploadLocalPort
        self.username = username
        self.password = password

    def upload(
        self, reading: WeatherReading, rainInLastHour: float, rainInLast24Hours: float
    ):
        logger.info("Sending reading...")

        response = requests.get(
            "https://idokep.hu/sendws.php",
            params={
                "user": self.username,
                "pass": self.password,
                "ev": reading.measuredAt.year,
                "ho": reading.measuredAt.month,
                "nap": reading.measuredAt.day,
                "ora": reading.measuredAt.hour,
                "perc": reading.measuredAt.minute,
                "mp": reading.measuredAt.second,
                "hom": reading.outdoorTemperature,
                "rh": reading.outdoorHumidity,
                "p": reading.seaLevelAirPressure,
                "szelirany": reading.windDirection,
                "szelero": reading.windSpeed,
                "szellokes": reading.gustSpeed,
                "csap": rainInLast24Hours,
                "csap1h": rainInLastHour,
            },
        )

        if response.status_code != OK:
            logger.error(
                f'Couldn\'t send reading. Reason: \
                          "{response.reason}"  {response.status_code} {responses[response.status_code].upper()}'
            )
        else:
            logger.info("Successfully sent reading.")
