import logging
import sys

from argumentNamespace import ArgumentNamespace
from config import Config
from core import Core
from databaseManager import DatabaseManager
from device import Device
from readingUploader import ReadingUploader

logger = logging.getLogger(__name__)


class App:
    def __init__(
        self,
        args: ArgumentNamespace,
        config: Config,
        username: str | None,
        password: str | None,
    ):
        self.args = args
        self.config = config
        self.uploadFrequency = config.uploadFrequency
        self.deviceConnectionRetryDelay = config.deviceConnectionRetryDelay
        self.databaseManager = DatabaseManager(config.databaseFilePath)
        if username != None and password != None:
            self.readingUploader = ReadingUploader(config, username, password)
        else:
            self.readingUploader = None

    def collectDataAndSend(self, device: Device):
        reading = device.getReading()
        if self.args.verbose:
            logger.debug(reading)

        self.databaseManager.save(reading)
        rainInLastHour, rainInLast24Hours = (
            self.databaseManager.getRainInLastHour(),
            self.databaseManager.getRainInLast24Hours(),
        )

        if self.readingUploader:
            self.readingUploader.upload(reading, rainInLastHour, rainInLast24Hours)

    def start(self):
        try:
            while True:
                try:
                    with Device(self.config) as device:
                        while True:
                            self.collectDataAndSend(device)
                            Core.sleep(
                                self.uploadFrequency,
                                None
                                if self.args.quiet
                                else "Getting next reading in: {0} seconds...",
                            )
                except Exception as error:
                    if self.args.failEarly:
                        raise
                    else:
                        logger.error(error)
                        Core.sleep(
                            self.deviceConnectionRetryDelay,
                            None if self.args.quiet else "Retrying in: {0} seconds...",
                        )
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            sys.stdout.flush()
            sys.exit(130)
