import tomllib
from pathlib import Path

from core import Core
from loggingConfigurer import LoggingConfigurer


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
            print("Successfully cleaned weather data.")
        else:
            print("No weather data was found that could be deleted.")

        if didDeleteAnyLogFile:
            print("Successfully cleaned logs.")
        else:
            print("No log was found that could be deleted.")


def main():
    clean()


if __name__ == "__main__":
    main()
