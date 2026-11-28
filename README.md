## WH1080 Weather Station Data Uploader
This project was made to retrieve weather data from the indoor unit of the WH1080 Weather Station and upload it to the időkép.hu servers on set intervals (once a minute by default). It also saves all weather data so that further analyses can be performed in the future.

## Dependencies
This project uses uv as it's package manager, so you will have to install it following https://docs.astral.sh/uv/#installation. (uv will install the required python version along with the necessary packages.)

You will also need to have gcc-c++ installed, because greenlet doesn't have prebuilt binary wheels, so it needs to be compiled when uv installs it.

You *might* also have to download the HID (Human Interface Device) library (if it's not installed on your system) following this guide: https://pypi.org/project/hid/, however on Windows, you can skip this step as hidapi.dll comes packaged with this repo. On most Linux distros it will be installed by default.

## Setup
On Linux, due to permission restrictions, you will need to configure the usb device to make it be accessable by non-root users. To do this, add a udev rule file to `/etc/udev/rules.d` named for example `70-wh1080.rules` and paste in this config:
```
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1941", ATTRS{idProduct}=="8021", MODE="0666"
```
After this, run `sudo udevadm control --reload` and `sudo udevadm trigger` to load the configuration.

## Running
Start the program using uv: `uv run python src/main.py`.

The program then will ask for the username and password of the időkép account. After that, it will start uploading the weather data.

## Arguments
You can pass the username and password as command line arguments with the `-u`/`--username` and `-p`/`--password` arguments.
The program can also be started in quiet and verbose mode using the `-q`/`--quiet` and `-v`/`--verbose` flags.
Take a look at the full argument list using `uv run python src/main.py --help`

# Config
The `config.toml` file in the project directory contains configuration options for the program that are usually only needed to be set up once.

These are the options that can be configured:

| Option | Description |
|---|---|
| station.altitude | Altitude of the sensor in meters above sea level |
| device.timeout | Max number of seconds with no response before closing connection |
| device.connection_retry_delay | How many seconds to wait before trying to connect again |
| upload.frequency | How many seconds to wait before reading and uploading new report |
| paths.log_dir | Path to directory where logs should be written |
| paths.database_file | Path to file where database should be stored |
| logging.backup_count | Number of backup log files to keep |

## Deleting saved weather data
> NOTE: This will remove ALL weather data that was saved. This can't be undone.

Start the `src/clean.py` script like so: `uv run python src/clean.py`