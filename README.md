## WH1080 Weather Station Data Uploader
This project was made to retrieve weather data from the indoor unit of the WH1080 Weather Station and upload it to the időkép.hu servers on set intervals (once a minute by default). It also saves all weather data so that further analyses can be performed in the future.

## Dependencies
This project uses uv as it's package manager, so you will have to install it following https://docs.astral.sh/uv/#installation. (uv will install the required python version along with the necessary packages.)

NOTE: On Windows, you can skip the next step as hidapi.dll comes packaged with this repo.
You will also have to download the HID (Human Interface Device) shared library following this guide: https://pypi.org/project/hid/

## Running
Start the program using uv: `uv run python src/main.py run`.

The program then will ask for the username and password of the időkép account. After that, it will start uploading the weather data every minute.

## Deleting saved weather data
NOTE: This will remove ALL weather data that was saved. This can't be undone.

Start the program using the `clean` command like so: `uv run python src/main.py clean`
