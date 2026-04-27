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

            didDeleteAnyLogFile = False
            for file in Core.getPath("log").iterdir():
                if file.suffix == ".log":
                    file.unlink()
                    didDeleteAnyLogFile = True

            if didDeleteAnyWeatherData:
                print("Successfully cleaned weather data.")
            else:
                print("No weather data was found that could be deleted.")

            if didDeleteAnyLogFile:
                print("Successfully cleaned error logs.")
            else:
                print("No log was found that could be deleted.")
        else:
            print("Aborted.")