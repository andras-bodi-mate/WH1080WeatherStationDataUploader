from pathlib import Path

from core import Core

class Cleaner:
    @staticmethod
    def clean():
        response = input("Are you sure you want to erase ALL weather data? ([Y]es/[N]o) ")
        if response.upper() == 'Y':
            for file in Path(Core.getPath("out")).iterdir():
                if file.name != ".gitignore" and file.suffix == ".csv":
                    file.unlink()
            print("Successfully cleaned data")
        else:
            print("Aborted.")