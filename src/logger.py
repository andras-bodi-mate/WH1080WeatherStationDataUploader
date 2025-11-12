import sty
from inspect import stack
from pathlib import Path
from datetime import datetime, timedelta

from strip_ansi import strip_ansi

from core import Core

class Logger:
    loggingDirectory: Path = Core.getPath("log")
    daysToKeepLogsAroundFor = 5

    @staticmethod
    def log(message: str, level: str, file = None):
        callerStackFrame = stack()[2]
        callerFile = callerStackFrame.filename
        callerFileName = f"[{Path(callerFile).name}]"
        for lineIndex, line in enumerate(message.split('\n')):
            now = datetime.now()
            logInfo = f"{callerFileName} ({now.hour:02d}:{now.minute:02d}:{now.second:02d}) {level}:  "

            if lineIndex == 0:
                print(f"{logInfo} {line}", file = file)
            else:
                print(f"{len(strip_ansi(logInfo)) * ' '} {line}", file = file)

    @staticmethod
    def logToFile(message: str, level: str):
        file = (Logger.loggingDirectory / datetime.now().isoformat()).with_suffix(".log")
        file.touch()

        currentDatetime = datetime.now()
        for file in Logger.loggingDirectory.iterdir():
            if currentDatetime - datetime.fromisoformat(file.stem) > timedelta(days = Logger.daysToKeepLogsAroundFor):
                file.unlink()

        with open(file, "a") as file:
            Logger.log(message, level, file)

    @staticmethod
    def getMessageFromValues(values):
        return ' '.join(map(str, values))

    @staticmethod
    def logDebug(*values):
        Logger.log(sty.fg.grey + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.li_cyan + "DEBUG" + sty.rs.all)

    @staticmethod
    def logInfo(*values):
        Logger.log(sty.fg.li_grey + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.green + "INFO" + sty.rs.all)

    @staticmethod
    def logWarning(*values):
        Logger.log(sty.fg.yellow + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.yellow + sty.ef.bold + "WARNING" + sty.rs.all)
        Logger.logToFile(Logger.getMessageFromValues(values), "WARNING")

    @staticmethod
    def logError(*values):
        Logger.log(sty.fg.red + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.red + sty.ef.bold + "ERROR" + sty.rs.all)
        Logger.logToFile(Logger.getMessageFromValues(values), "ERROR")

    @staticmethod
    def logCriticalError(*values):
        Logger.log(sty.fg.magenta + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.magenta + sty.ef.bold + "CRITICAL ERROR" + sty.rs.all)
        Logger.logToFile(Logger.getMessageFromValues(values), "CRITICAL ERROR")

    def __init__(self):
        Logger.loggingDirectory.mkdir(exist_ok = True)