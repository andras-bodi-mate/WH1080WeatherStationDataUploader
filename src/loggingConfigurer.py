import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import sty

from config import Config

logger: logging.Logger = logging.getLogger(__name__)


class ColoredFormatter(logging.Formatter):
    levelColors = frozendict(
        {
            logging.DEBUG: sty.fg.grey,
            logging.INFO: sty.fg.green,
            logging.WARNING: sty.fg.yellow,
            logging.ERROR: sty.fg.red + sty.ef.bold,
            logging.CRITICAL: sty.fg.magenta + sty.ef.bold,
        }
    )

    def __init__(
        self, fmt=None, datefmt=None, style="%", validate=True, *, defaults=None
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: logging.LogRecord):
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
    @staticmethod
    def shutdownFileHandlers():
        logger = logging.getLogger()

        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)

    def __init__(self, config: Config):
        self.logDir = config.logDir

    def logFileNamer(self, defaultName):
        datePart = Path(defaultName).stem.split(".")[-1]
        return self.logDir / Path(datePart).with_suffix(".log")

    def configureLogging(self, quiet=False, verbose=False):
        level = logging.INFO
        if quiet:
            level = logging.ERROR
        elif verbose:
            level = logging.DEBUG

        loggingFormat = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s"
        dateFormat = "%H:%M:%S"

        console = logging.StreamHandler()
        console.setFormatter(
            ColoredFormatter(
                loggingFormat,
                datefmt=dateFormat,
            )
        )

        fileHandler = TimedRotatingFileHandler(
            self.logDir / "app.log", encoding="UTF-8", when="midnight", backupCount=5
        )
        fileHandler.suffix = "%Y.%m.%d"
        fileHandler.namer = self.logFileNamer
        fileHandler.setFormatter(
            logging.Formatter(
                loggingFormat,
                datefmt=dateFormat,
            )
        )

        logging.basicConfig(level=level, handlers=[console, fileHandler])

        logger.debug(f"Logs will be saved in {self.logDir}")
