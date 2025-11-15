from core import Core

class Cleaner:
    @staticmethod
    def clean():
        response = input("Are you sure you want to erase ALL weather data? ([Y]es/[N]o) ")
        if response.upper() == 'Y':
            didDeleteAnyFile = False
            for file in Core.getPath("out").iterdir():
                if file.name != ".gitignore" and file.suffix == ".csv":
                    file.unlink()
                    didDeleteAnyFile = True
            if didDeleteAnyFile:
                print("Successfully cleaned weather data.")
            else:
                print("No weather data was found that could be deleted.")
        else:
            print("Aborted.")

        response = input("Do you want to erase ALL error logs? ([Y]es/[N]o) ")
        if response.upper() == 'Y':
            didDeleteAnyFile = False
            for file in Core.getPath("log").iterdir():
                if file.name != ".gitignore" and file.suffix == ".log":
                    file.unlink()
                    didDeleteAnyFile = True
            if didDeleteAnyFile:
                print("Successfully cleaned error logs.")
            else:
                print("No log was found that could be deleted.")
        else:
            print("Aborted.")