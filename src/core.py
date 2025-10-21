from pathlib import Path, PurePosixPath
import time
import math

class Core:
    projectDir = Path(__file__).resolve().parent.parent

    @staticmethod
    def getPath(path: str | Path):
        if isinstance(path, Path) and path.exists():
            return path
        else:
            return Core.projectDir / PurePosixPath(path)
        
    @staticmethod
    def sleep(seconds: float, message: str = None):
        padding = ' ' * 10

        if message:
            print(message.format(math.floor(seconds)) + padding, end = '\r')
            for i in range(math.floor(seconds)):
                time.sleep(1)
                print(message.format(seconds - i - 1) + padding, end = '\r')
            time.sleep(seconds % 1)
        else:
            time.sleep(seconds)