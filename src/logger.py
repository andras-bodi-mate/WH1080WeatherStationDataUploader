import sty
import sys
from inspect import stack
from pathlib import Path
from datetime import datetime, date, timedelta
from enum import Enum

from strip_ansi import strip_ansi

from core import Core

class LogLevel(Enum):
    Debug = 1
    Info = 2
    Warning = 3
    Error = 4
    Critical = 5

class Logger:
    loggingDirectory: Path = Core.getPath("log")
    daysToKeepLogsAroundFor = 5
    loggingLevel = LogLevel.Info

    @staticmethod
    def configure(quiet = False, verbose = False, daysToKeepLogsAroundFor = 5):
        if quiet:
            Logger.loggingLevel = LogLevel.Error
        elif verbose:
            Logger.loggingLevel = LogLevel.Debug
        else:
            Logger.loggingLevel = LogLevel.Info
        
        Logger.daysToKeepLogsAroundFor = daysToKeepLogsAroundFor

    @staticmethod
    def logToStdout(level: LogLevel, message: str, levelStr: str, file = None):
        callerStackFrame = stack()[2]
        callerFile = callerStackFrame.filename
        callerFileName = f"[{Path(callerFile).name}]"
        for lineIndex, line in enumerate(message.split('\n')):
            now = datetime.now()
            logInfo = f"{callerFileName} ({now.hour:02d}:{now.minute:02d}:{now.second:02d}) {levelStr}:  "

            if file is None and level.value >= LogLevel.Error.value:
                file = sys.stderr

            if lineIndex == 0:
                print(f"{logInfo} {line}", file = file)
            else:
                print(f"{len(strip_ansi(logInfo)) * ' '} {line}", file = file)

    @staticmethod
    def logToFile(level: LogLevel, message: str, levelStr: str):
        file = (Logger.loggingDirectory / date.today().isoformat()).with_suffix(".log")
        file.touch()

        currentDatetime = date.today()
        for file in Logger.loggingDirectory.iterdir():
            if file.suffix == ".log" and currentDatetime - date.fromisoformat(file.stem) > timedelta(days = Logger.daysToKeepLogsAroundFor):
                file.unlink()

        with open(file, "a") as file:
            Logger.logToStdout(level, message, levelStr, file)

    @staticmethod
    def log(level: LogLevel, message: str, levelStr: str):
        Logger.logToStdout(level, message, levelStr)
        Logger.logToFile(level, message, levelStr)

    @staticmethod
    def getMessageFromValues(values):
        return ' '.join(map(str, values))

    @staticmethod
    def logDebug(*values):
        Logger.log(
            sty.fg.grey + Logger.getMessageFromValues(values) + sty.rs.all,
            sty.fg.li_cyan + "DEBUG" + sty.rs.all
        )

    @staticmethod
    def logInfo(*values):
        Logger.log(
            LogLevel.Info,
            sty.fg.li_grey + Logger.getMessageFromValues(values) + sty.rs.all,
            sty.fg.green + "INFO" + sty.rs.all
        )

    @staticmethod
    def logWarning(*values):
        Logger.log(
            LogLevel.Warning,
            sty.fg.yellow + Logger.getMessageFromValues(values) + sty.rs.all,
            sty.fg.yellow + sty.ef.bold + "WARNING" + sty.rs.all
        )

    @staticmethod
    def logError(*values):
        Logger.log(
            LogLevel.Error,
            sty.fg.red + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all,
            sty.fg.red + sty.ef.bold + "ERROR" + sty.rs.all
        )

    @staticmethod
    def logCritical(*values):
        Logger.log(
            LogLevel.Critical,
            sty.fg.magenta + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all,
            sty.fg.magenta + sty.ef.bold + "CRITICAL ERROR" + sty.rs.all
        )