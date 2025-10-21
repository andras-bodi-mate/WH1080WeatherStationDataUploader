from dataclasses import dataclass

import requests
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
                "ev": report.date.year,
                "ho": report.date.month,
                "nap": report.date.day,
                "ora": report.date.hour,
                "perc": report.date.minute,
                "mp": report.date.second,
                "hom": report.outdoorTemperature,
                "rh": report.outdoorHumidity,
                "p": report.relativeAirPressure,
                "szelirany": report.windDirection,
                "szelero": report.windSpeed,
                "csap": report.rain
            }
        )

        if response.status_code != requests.status_codes.codes.OK:
            Logger.logError(f"Couldn't send report. Reason: \"{response.reason}\"  {response.status_code} {responses[response.status_code].upper()}")
        else:
            Logger.logInfo("Successfully sent report.")
