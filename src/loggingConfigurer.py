import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import sty

from core import Core

class ColoredFormatter(logging.Formatter):
    levelColors = {
        logging.DEBUG: sty.fg.grey,
        logging.INFO: sty.fg.green,
        logging.WARNING: sty.fg.yellow,
        logging.ERROR: sty.fg.red + sty.ef.bold,
        logging.CRITICAL: sty.fg.magenta + sty.ef.bold,
    }

    def __init__(self, fmt = None, datefmt = None, style = "%", validate = True, *, defaults = None):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record):
        color = self.levelColors.get(record.levelno, "")
        reset = sty.rs.all

        originalLevelName = record.levelname
        originalMessage = record.msg

        record.levelname = f"{color}{record.levelname}{reset}"
        record.msg = f"{record.msg}"

        result = super().format(record)

        record.levelname = originalLevelName
        record.msg = originalMessage

        return result


class LoggingConfigurer:
    logPath = Core.getPath("log")

    @staticmethod
    def logFileNamer(defaultName):
        datePart = Path(defaultName).stem.split(".")[-1]
        return LoggingConfigurer.logPath / Path(datePart).with_suffix(".log")

    @staticmethod
    def configureLogging(quiet=False, verbose=False):
        level = logging.INFO
        if quiet:
            level = logging.ERROR
        elif verbose:
            level = logging.DEBUG

        console = logging.StreamHandler()
        console.setFormatter(
            ColoredFormatter(
                "[%(filename)s] (%(asctime)s) %(levelname)s: %(message)s",
                datefmt="%H:%M:%S"
            )
        )

        fileHandler = TimedRotatingFileHandler(
            LoggingConfigurer.logPath / "app.log",
            encoding="UTF-8",
            when="midnight",
            backupCount=5
        )
        fileHandler.suffix = "%Y.%m.%d"
        fileHandler.namer = LoggingConfigurer.logFileNamer
        fileHandler.setFormatter(
            logging.Formatter(
                "[%(filename)s] (%(asctime)s) %(levelname)s: %(message)s",
                datefmt="%H:%M:%S"
            )
        )

        logging.basicConfig(level=level, handlers=[console, fileHandler])

    @staticmethod
    def shutdownFileHandlers():
        logger = logging.getLogger()

        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)
    