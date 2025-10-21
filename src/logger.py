import sty
from inspect import stack
import pathlib
from datetime import datetime

from strip_ansi import strip_ansi

class Logger:
    @staticmethod
    def log(message: str, level: str):
        callerStackFrame = stack()[2]
        callerFile = callerStackFrame.filename
        callerFileName = f"[{pathlib.Path(callerFile).name}]"
        for lineIndex, line in enumerate(message.split('\n')):
            now = datetime.now()
            logInfo = f"{callerFileName} ({now.hour:02d}:{now.minute:02d}:{now.second:02d}) {level}:  "

            if lineIndex == 0:
                print(f"{logInfo} {line}")
            else:
                print(f"{len(strip_ansi(logInfo)) * ' '} {line}")

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

    @staticmethod
    def logError(*values):
        Logger.log(sty.fg.red + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.red + sty.ef.bold + "ERROR" + sty.rs.all)

    @staticmethod
    def logCriticalError(*values):
        Logger.log(sty.fg.magenta + sty.ef.bold + Logger.getMessageFromValues(values) + sty.rs.all, sty.fg.magenta + sty.ef.bold + "CRITICAL ERROR" + sty.rs.all)
