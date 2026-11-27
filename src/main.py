import argparse
import logging
import signal
import sys
import tomllib

from pwinput import pwinput

from app import App
from argumentNamespace import ArgumentNamespace
from config import Config
from core import Core
from loggingConfigurer import LoggingConfigurer

logger: logging.Logger = logging.getLogger(__name__)

def signalHandler(signalNumber, _frame):
    if signalNumber == signal.SIGINT:
        sys.stdout.write("\n")
        sys.stdout.flush()
        sys.exit(130)

def main():
    parser = argparse.ArgumentParser(
        description="Collects data from a WH1080 weather station connected via USB, and forwards the weather data to időkép.hu",
        epilog="Use 'main.py <command> --help' for more information on a command.",
    )

    parser.add_argument("-u", "--username", help="The username of the időkép account")
    parser.add_argument("-p", "--password", help="The password for the időkép account")
    parser.add_argument(
        "-f",
        "--fail-early",
        dest="failEarly",
        action="store_true",
        help="Do not catch runtime exceptions",
    )
    parser.add_argument(
        "-n",
        "--no-upload",
        dest="noUpload",
        action="store_true",
        help="Do not upload weather data",
    )

    verbosityGroup = parser.add_mutually_exclusive_group()
    verbosityGroup.add_argument(
        "-q", "--quiet", action="store_true", help="Don't write anything to stdout"
    )
    verbosityGroup.add_argument(
        "-v", "--verbose", action="store_true", help="Print debug information"
    )

    namespace = ArgumentNamespace()
    args = parser.parse_args(namespace=namespace)

    logger.debug(f"The program will use the following arguments: {args}")

    with open(Core.getPath("config.toml"), "rb") as configFile:
        configToml = tomllib.load(configFile)

    config = Config(
        stationAltitude=configToml["station"]["altitude"],
        deviceTimeout=configToml["device"]["timeout"],
        deviceConnectionRetryDelay=configToml["device"]["connection_retry_delay"],
        uploadFrequency=configToml["upload"]["frequency"],
        uploadLocalPort=configToml["upload"]["local_port"],
        logDir=Core.getPath(configToml["paths"]["log_dir"]),
        databaseFilePath=Core.getPath(configToml["paths"]["database_file"]),
        logBackupCount=configToml["logging"]["backup_count"],
    )

    LoggingConfigurer(config).configureLogging(quiet=args.quiet, verbose=args.verbose)

    logger.debug(f"The program will use the following config options:\n{config}")

    if not args.noUpload:
        username: str = args.username or input("időkép username: ")
        password: str = args.password or pwinput("időkép password: ")
    else:
        username = None
        password = None

    signal.signal(signal.SIGINT, signalHandler)

    app = App(args, config, username, password)
    app.start()


if __name__ == "__main__":
    main()
