import sys

from device import Device
from reportSaver import ReportSaver
from reportUploader import ReportUploader
from logger import Logger
from cleaner import Cleaner
from core import Core

def main():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "clean":
                cleaner = Cleaner()
                cleaner.clean()
    else:
        reportSaver = ReportSaver(Core.getPath("out"))
        reportUploader = ReportUploader("<username>", "<password>")

        try:
            while True:
                try:
                    with Device() as device:
                        while True:
                            report = device.getReport()
                            reportSaver.save(report)
                            reportUploader.upload(report)
                            Core.sleep(60, "Getting next report in: {0} seconds")
                except Exception as error:
                    Logger.logError(error)
                    Core.sleep(5, "Retrying in: {0} seconds")
        except KeyboardInterrupt:
            Logger.logInfo("Exiting...")

main()