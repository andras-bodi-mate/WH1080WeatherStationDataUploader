import argparse
import logging

from device import Device
from reportSaver import ReportSaver
from reportUploader import ReportUploader
from exceptions import InvalidReportError
from report import Report
from config import Config
from core import Core

class App:
    def __init__(self, args: argparse.Namespace, config: Config, username: str, password: str):
        self.args = args
        self.config = config
        self.uploadFrequency = config.uploadFrequency
        self.deviceConnectionRetryDelay = config.deviceConnectionRetryDelay
        self.reportSaver = ReportSaver(config)
        self.reportUploader = ReportUploader(config, username, password)
        self.previousReport: Report = None

    def collectDataAndSend(self, device: Device):
        report = device.getReport()
        if self.args.verbose:
            logging.debug(report)

        if previousReport and not report.isValid(previousReport):
            raise InvalidReportError("Report is not valid.")
        else:
            self.reportSaver.save(report)
            self.reportUploader.upload(report)
            previousReport = report

    def start(self):
        try:
            while True:
                try:
                    with Device(self.config) as device:
                        while True:
                            self.collectDataAndSend(device)
                            Core.sleep(self.uploadFrequency, "Getting next report in: {0} seconds...")
                except Exception as error:
                    logging.error(error)
                    Core.sleep(self.deviceConnectionRetryDelay, "Retrying in: {0} seconds...")
        except KeyboardInterrupt:
            logging.info("Exiting...")