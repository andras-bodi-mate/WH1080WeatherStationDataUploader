import argparse
import logging

from device import Device
from readingUploader import ReadingUploader
from databaseManager import DatabaseManager
from config import Config
from core import Core

class App:
    def __init__(self, args: argparse.Namespace, config: Config, username: str, password: str):
        self.args = args
        self.config = config
        self.uploadFrequency = config.uploadFrequency
        self.deviceConnectionRetryDelay = config.deviceConnectionRetryDelay
        self.databaseManager = DatabaseManager(config.outputDir / "database.db")
        self.readingUploader = ReadingUploader(config, username, password)

    def collectDataAndSend(self, device: Device):
        reading = device.getReading()
        if self.args.verbose:
            logging.debug(reading)

        self.databaseManager.save(reading)
        self.readingUploader.upload(reading)

    def start(self):
        try:
            while True:
                try:
                    with Device(self.config) as device:
                        while True:
                            self.collectDataAndSend(device)
                            Core.sleep(self.uploadFrequency, "Getting next reading in: {0} seconds...")
                except Exception as error:
                    logging.error(error)
                    Core.sleep(self.deviceConnectionRetryDelay, "Retrying in: {0} seconds...")
        except KeyboardInterrupt:
            logging.info("Exiting...")