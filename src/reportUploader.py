from dataclasses import dataclass
import contextlib
import requests
from requests.adapters import HTTPAdapter, Retry
from http.client import responses

from report import Report
from logger import Logger

@dataclass
class ReportUploader:
    username: str
    password: str

    def upload(self, report: Report):
        Logger.logInfo("Sending report...")

        response = requests.get(
            "https://idokep.hu/sendws.php",
            params = {
                "user": self.username,
                "pass": self.password,
                "ev": report.datetime.year,
                "ho": report.datetime.month,
                "nap": report.datetime.day,
                "ora": report.datetime.hour,
                "perc": report.datetime.minute,
                "mp": report.datetime.second,
                "hom": report.outdoorTemperature,
                "rh": report.outdoorHumidity,
                "p": report.seaLevelAirPressure,
                "szelirany": report.windDirection,
                "szelero": report.windSpeed,
                "szellokes": report.gustSpeed,
                "csap": Report.getRainInLast24Hours(),
                "csap1h": Report.getRainInLastHour()
            }
        )

        with contextlib.suppress(requests.RequestException):
            requests.post(
                "http://127.0.0.1:57320",
                json = {
                    "id": report.id,
                    "timestamp": int(report.datetime.timestamp()),
                    "indoorTemperature": report.indoorTemperature,
                    "indoorHumidity": report.indoorHumidity,
                    "outdoorTemperature": report.outdoorTemperature,
                    "outdoorHumidity": report.outdoorHumidity,
                    "windSpeed": report.windSpeed,
                    "gustSpeed": report.gustSpeed,
                    "windDirection": report.windDirection,
                    "outdoorDewPoint": report.outdoorDewPoint,
                    "windChill": report.windChill,
                    "seaLevelAirPressure": report.seaLevelAirPressure,
                    "totalRain": report.allTimeRain,
                    "rainSinceLastUpdate": report.rainSinceLastUpdate
                }
            )

        if response.status_code != requests.status_codes.codes.OK:
            Logger.logError(f"Couldn't send report. Reason: \"{response.reason}\"  {response.status_code} {responses[response.status_code].upper()}")
        else:
            Logger.logInfo("Successfully sent report.")
