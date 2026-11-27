import logging
import tomllib
from pathlib import Path

from core import Core
from loggingConfigurer import LoggingConfigurer

logger = logging.getLogger(__name__)


def clean():
    with open(Core.getPath("config.toml"), "rb") as configFile:
        configToml = tomllib.load(configFile)

    databasePath = Path(configToml["paths"]["database_file"])

    response = input("Are you sure you want to erase ALL weather data and logs? [y/N] ")
    if response.upper() == "Y":
        weatherDatabaseExists = databasePath.exists()
        if weatherDatabaseExists:
            databasePath.unlink()

        LoggingConfigurer.shutdownFileHandlers()
        didDeleteAnyLogFile = False
        for file in Core.getPath("log").iterdir():
            if file.suffix == ".log":
                file.unlink()
                didDeleteAnyLogFile = True

        if weatherDatabaseExists:
            logger.info("Successfully cleaned weather data.")
        else:
            logger.info("No weather data was found that could be deleted.")

        if didDeleteAnyLogFile:
            logger.info("Successfully cleaned logs.")
        else:
            logger.info("No log was found that could be deleted.")
    else:
        print("Aborted.")


def main():
    clean()


if __name__ == "__main__":
    main()
