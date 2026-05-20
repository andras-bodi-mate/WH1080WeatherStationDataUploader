import requests
from http.client import responses
import logging

from weatherReading import WeatherReading
from config import Config

class ReadingUploader:
    def __init__(self, config: Config, username: str, password: str):
        self.frequency = config.uploadFrequency
        self.localPort = config.uploadLocalPort
        self.username = username
        self.password = password

    def upload(self, reading: WeatherReading):
        logging.info("Sending reading...")

        response = requests.get(
            "https://idokep.hu/sendws.php",
            params = {
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
                "csap": WeatherReading.getRainInLast24Hours(),
                "csap1h": WeatherReading.getRainInLastHour()
            }
        )

        if response.status_code != requests.status_codes.codes.OK:
            logging.error(f"Couldn't send reading. Reason: \
                          \"{response.reason}\"  {response.status_code} {responses[response.status_code].upper()}")
        else:
            logging.info("Successfully sent reading.")
