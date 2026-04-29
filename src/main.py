import argparse
import tomllib
import logging

import pwinput

from cleaner import Cleaner
from loggingConfigurer import LoggingConfigurer
from app import App
from config import Config
from core import Core

def main():
    parser = argparse.ArgumentParser(
        description = "Collects data from a WH1080 weather station connected via USB, and forwards the weather data to időkép.hu",
        epilog = "Use 'main.py <command> --help' for more information on a command."
    )
    subparser = parser.add_subparsers(dest = "command", required = True)
    cleanParser = subparser.add_parser("clean", help = "Delete all collected wheather data and logs")

    runParser = subparser.add_parser("run", help = "Run the program")
    runParser.add_argument("-u", "--username", help = "The username of the időkép account")
    runParser.add_argument("-p", "--password", help = "The password for the időkép account")

    verbosityGroup = parser.add_mutually_exclusive_group()
    verbosityGroup.add_argument("-q", "--quiet", action = "store_true", help = "Don't write anything to stdout")
    verbosityGroup.add_argument("-v", "--verbose", action = "store_true", help = "Print debug information")

    args = parser.parse_args()

    with open(Core.getPath("config.toml"), "rb") as configFile:
        configToml = tomllib.load(configFile)

    config = Config(
        stationAltitude=configToml["station"]["altitude"],
        deviceTimeout=configToml["device"]["timeout"],
        deviceConnectionRetryDelay=configToml["device"]["connection_retry_delay"],
        uploadFrequency=configToml["upload"]["frequency"],
        uploadLocalPort=configToml["upload"]["local_port"],
        logDir=Core.getPath(configToml["paths"]["log_dir"]),
        outputDir=Core.getPath(configToml["paths"]["output_dir"]),
        logBackupCount=configToml["logging"]["backup_count"]
    )

    LoggingConfigurer(config).configureLogging(
        quiet=args.quiet,
        verbose=args.verbose
    )

    logging.debug(f"The program will use the following config options:\n{config}")

    if args.command == "clean":
        cleaner = Cleaner()
        cleaner.clean()

    elif args.command == "run":
        username = args.username or input("időkép username: ")
        password = args.password or pwinput.pwinput("időkép password: ")

        app = App(args, config, username, password)
        app.start()

main()