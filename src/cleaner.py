import logging

from core import Core
from loggingConfigurer import LoggingConfigurer

logger = logging.getLogger(__name__)

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
                logger.info("Successfully cleaned weather data.")
            else:
                logger.info("No weather data was found that could be deleted.")

            if didDeleteAnyLogFile:
                logger.info("Successfully cleaned logs.")
            else:
                logger.info("No log was found that could be deleted.")
        else:
            print("Aborted.")