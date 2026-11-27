## WH1080 Weather Station Data Uploader
This project was made to retrieve weather data from the indoor unit of the WH1080 Weather Station and upload it to the időkép.hu servers on set intervals (once a minute by default). It also saves all weather data so that further analyses can be performed in the future.

## Dependencies
This project uses uv as it's package manager, so you will have to install it following https://docs.astral.sh/uv/#installation. (uv will install the required python version along with the necessary packages.)

You *might* also have to download the HID (Human Interface Device) library (if it's not installed on your system) following this guide: https://pypi.org/project/hid/, however on Windows, you can skip this step as hidapi.dll comes packaged with this repo.

## Running
Start the program using uv: `uv run python src/main.py`.

The program then will ask for the username and password of the időkép account. After that, it will start uploading the weather data every minute.

## Arguments
You can pass the username and password as command line arguments with the -u/--username and -p/--password arguments.
The program can also be started in quiet and verbose mode using the -q/--quiet and -v/--verbose flags.
Take a look at the full argument list using `uv run python src/main.py --help`

## Deleting saved weather data
NOTE: This will remove ALL weather data that was saved. This can't be undone.

Start the `src/clean.py` script like so: `uv run python src/clean.py`