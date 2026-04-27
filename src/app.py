import argparse
import logging

from device import Device
from reportSaver import ReportSaver
from reportUploader import ReportUploader
from exceptions import DeviceConnectionError, InvalidReportError
from core import Core

class App:
    def __init__(self, args: argparse.Namespace, username: str, password: str):
        self.args = args
        self.reportSaver = ReportSaver(Core.getPath("out"))
        self.reportUploader = ReportUploader(username, password)
        self.previousReport = None

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
                    with Device() as device:
                        while True:
                            self.collectDataAndSend(device)
                            Core.sleep(60, "Getting next report in: {0} seconds...")
                except Exception as error:
                    logging.error(error)
                    Core.sleep(5, "Retrying in: {0} seconds...")
        except KeyboardInterrupt:
            logging.info("Exiting...")