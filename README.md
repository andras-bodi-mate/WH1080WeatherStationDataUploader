## WH1080 Weather Station Data Uploader
This project was made to retrieve weather data from the indoor unit of the WH1080 Weather Station and upload it to the időkép.hu servers on set intervals (once a minute by default). It also saves all weather data so that further analyses can be performed in the future.

## Running
On Linux: Just start the run.sh bash script inside the scripts directory.

On Windows: Just start the run.bat file located in  the scripts directory.

## Deleting saved weather data
NOTE: This will remove ALL weather data that was saved. This can't be undone.

On Linux: Just start the clean.sh bash script inside the scripts directory.

On Windows: Just start the clean.bat file located in  the scripts directory.

## Note on running scripts
Since this project uses uv as it's package manager, if a script can't find uv on your system, it will automatically install it. You will then need to rerun the script to continue.