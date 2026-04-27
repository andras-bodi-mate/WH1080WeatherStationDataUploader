import logging

from loggingConfigurer import LoggingConfigurer
from core import Core

class Cleaner:
    @staticmethod
    def clean():
        response = input("Are you sure you want to erase ALL weather data and logs? ([Y]es/[N]o) ")
        if response.upper() == 'Y':
            didDeleteAnyWeatherData = False
            for file in Core.getPath("out").iterdir():
                if file.suffix == ".csv":
                    file.unlink()
                    didDeleteAnyWeatherData = True

            LoggingConfigurer.shutdownFileHandlers()
            didDeleteAnyLogFile = False
            for file in Core.getPath("log").iterdir():
                if file.suffix == ".log":
                    file.unlink()
                    didDeleteAnyLogFile = True

            if didDeleteAnyWeatherData:
                logging.info("Successfully cleaned weather data.")
            else:
                logging.info("No weather data was found that could be deleted.")

            if didDeleteAnyLogFile:
                logging.info("Successfully cleaned logs.")
            else:
                logging.info("No log was found that could be deleted.")
        else:
            print("Aborted.")