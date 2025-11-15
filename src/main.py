import sys

import pwinput

from device import Device
from reportSaver import ReportSaver
from reportUploader import ReportUploader
from logger import Logger
from cleaner import Cleaner
from exceptions import DeviceConnectionError, InvalidReportError
from core import Core

def main():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "clean":
                cleaner = Cleaner()
                cleaner.clean()
    else:
        username = input("időkép username: ")
        password = pwinput.pwinput("időkép password: ")
        reportSaver = ReportSaver(Core.getPath("out"))
        reportUploader = ReportUploader(username, password)
        previousReport = None
        try:
            while True:
                try:
                    with Device() as device:
                        while True:
                            report = device.getReport()
                            if previousReport and not report.isValid(previousReport):
                                raise InvalidReportError("Report is not valid.")
                            else:
                                reportSaver.save(report)
                                reportUploader.upload(report)
                                previousReport = report
                            Core.sleep(60, "Getting next report in: {0} seconds...")
                except Exception as error:
                    Logger.logError(error)
                    Core.sleep(5, "Retrying in: {0} seconds...")
        except KeyboardInterrupt:
            Logger.logInfo("Exiting...")

main()