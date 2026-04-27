from pathlib import Path
import csv
import logging

from report import Report

class ReportSaver:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents = True, exist_ok = True)

    def save(self, report: Report):
        logging.info("Saving report...")

        path = (self.directory / report.datetime.date().isoformat()).with_suffix(".csv")
        if not path.exists():
            path.touch()
            with open(path, "w", encoding = "utf-8", newline = '') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "id",
                    "datetime",
                    "indoorTemperature",
                    "indoorHumidity",
                    "outdoorTemperature",
                    "outdoorHumidity",
                    "windSpeed",
                    "gustSpeed",
                    "windDirection",
                    "outdoorDewPoint",
                    "windChill",
                    "seaLevelAirPressure",
                    "totalRain",
                    "rainSinceLastUpdate"
                ])

        with open(path, "a", encoding = "utf-8", newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([
                report.id,
                report.datetime,
                report.indoorTemperature,
                report.indoorHumidity,
                report.outdoorTemperature,
                report.outdoorHumidity,
                report.windSpeed,
                report.gustSpeed,
                report.windDirection,
                report.outdoorDewPoint,
                report.windChill,
                report.seaLevelAirPressure,
                report.allTimeRain,
                report.rainSinceLastUpdate
            ])
        
        logging.info("Successfully saved report.")
