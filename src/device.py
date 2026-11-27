import datetime
import logging
import math
import os
import platform
import struct

from config import Config
from core import Core
from exceptions import NoSensorConnectionError
from weatherReading import WeatherReading

if platform.system() == "Windows":
    with os.add_dll_directory(Core.getPath("lib")) as _:  # ty: ignore[missing-attribute]
        import hid
else:
    import hid


logger: logging.Logger = logging.getLogger(__name__)


class Device:
    windDirections = (
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    )

    maxRainJump = 10
    """Maximum difference between two consecutive total rain readings in millimeters"""

    altitude = 240
    """Device altitude in meters above sea level"""

    @staticmethod
    def getDewPoint(temperature: float, humidity: float) -> float:
        """
        Using the supplied temperature and humidity to calculate the dew point
        """
        humidity /= 100.0
        gamma = (17.271 * temperature) / (237.7 + temperature) + math.log(humidity)
        return (237.7 * gamma) / (17.271 - gamma)

    @staticmethod
    def getWindChill(temperature: float, wind: float) -> float:
        """
        Using the supplied temperature and wind speed to calculate the wind chill
        factor.
        From Wikipedia: Wind-chill or windchill, (popularly wind chill factor) is
        the perceived decrease in air temperature felt by the body on exposed skin
        due to the flow of air
        """
        windKph = 3.6 * wind

        # Low wind speed, or high temperature, negates any perceived wind chill
        if (windKph <= 4.8) or (temperature > 10.0):
            return temperature

        windChill = (
            13.12
            + (0.6215 * temperature)
            - (11.37 * (windKph**0.16))
            + (0.3965 * temperature * (windKph**0.16))
        )

        # Return the lower of temperature or wind chill temperature
        if windChill < temperature:
            return windChill
        else:
            return temperature

    @staticmethod
    def getSeaLevelAirPressure(airPressure, temperature) -> float:
        """Calculate sea level pressure from relative pressure in kPa and temperature in celsius using

        P0 = P * exp((M * g * h) / (R * T))

        where:
            - P: Reference atmospheric pressure at altitude h
            - P0: Atmospheric pressure at sea level.
            - M: Molar mass of dry air (0.0289644 kg/mol).
            - g: Acceleration due to gravity (9.80665 m/s²).
            - h: Altitude (height above sea level) in meters.
            - R: Ideal gas constant (8.31446261815324 J/(mol·K)).
            - T: Absolute temperature in Kelvin

        Air pressure is in kPa.
        """
        return airPressure * math.exp(
            (0.0289644 * 9.8069 * Device.altitude)
            / (8.31446261815324 * (temperature + 273.15))
        )

    def __init__(self, config: Config, vendorId: int = 0x1941, productId: int = 0x8021):
        self.vendorId = vendorId
        self.productId = productId
        self.timeout = config.deviceTimeout
        self.previousRain = 0

    def __enter__(self):
        self.device = hid.Device(self.vendorId, self.productId)
        logger.info("Successfully connected to device.")

        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.device.close()

    def readBlock(self, offset: int) -> bytearray:
        """
        Read a block of data from the device, starting at the given offset in bytes
        """

        # Construct a binary message
        request = struct.pack(">BHBBHB", 0xA1, offset, 0x20, 0xA1, offset, 0x20)

        self.device.write(bytes([0x00]) + request)

        block = bytearray()
        while len(block) < 32:
            chunk: bytes | None = self.device.read(8, self.timeout * 1000)
            if not chunk:
                raise OSError("Timed out while reading from weather station")
            block.extend(chunk)

        if len(block) > 32:
            raise OSError("Device returned too much data")

        return block

    def getReading(self) -> WeatherReading:
        # Huge thank you to whoever made https://www.theapplebyclan.com/Richard/Weatherstation/WeatherStationMemoryMap.pdf
        # this would not have been possible without it

        fixedBlock = self.readBlock(0)

        # Check that we have good data
        if fixedBlock[0] != 0x55:
            raise ValueError("Bad data returned")

        # Bytes 31 and 32 when combined create an unsigned short int
        # that tells us where to find the weather data we want
        currentPosition = struct.unpack("<H", fixedBlock[30:32])[0]
        currentBlock = self.readBlock(currentPosition)

        # byte 15 describes the status of the device:
        # bit 6: loss of contact with sensor
        # bit 7: rain counter overflow
        noSensorContact = bool(currentBlock[15] & 0x40)
        totalRainOverflowed = bool(currentBlock[15] & 0x80)

        if noSensorContact:
            raise NoSensorConnectionError(
                "The indoor unit couldn't recieve signal from the outdoor sensor"
            )

        # Indoor information
        indoorHumidity = currentBlock[1]
        # temperature is encoded in a 2 byte signed short starting at byte 2
        indoorTemperature = struct.unpack("<h", currentBlock[2:4])[0] * 0.1

        # Outdoor information
        outdoorHumidity = currentBlock[4]
        outdoorTemperature = struct.unpack("<h", currentBlock[5:7])[0] * 0.1

        # Absolute air pressure is encoded in an unsigned short int starting at byte 7
        # that we multiply by 0.1 to find the absolute pressure
        absoluteAirPressure = struct.unpack("<H", currentBlock[7:9])[0] * 0.1
        seaLevelAirPressure = Device.getSeaLevelAirPressure(
            absoluteAirPressure, outdoorTemperature
        )

        # Bytes 9 and 10 store the low bits of the wind and gust speed
        # and byte 11 stores the high bits
        wind = currentBlock[9]
        gust = currentBlock[10]
        windExtra = currentBlock[11]
        windDirection = currentBlock[12]
        windDirectionDegrees = windDirection * 22.5

        # Bytes 14 and 15  when combined create an unsigned short int
        # that we multiply by 0.3 to find the total rain
        allTimeRain = struct.unpack("<H", currentBlock[13:15])[0] * 0.3

        # Calculate wind speeds
        windSpeed = (wind + ((windExtra & 0x0F) << 8)) * 0.38
        gustSpeed = (gust + ((windExtra & 0xF0) << 4)) * 0.38

        outdoorDewPoint = Device.getDewPoint(outdoorTemperature, outdoorHumidity)
        windChill = Device.getWindChill(outdoorTemperature, windSpeed)

        # In the first run there is no previous value, so we set it to the total amount of rain
        if self.previousRain == 0 or totalRainOverflowed:
            self.previousRain = allTimeRain

        rainSinceLastUpdate = (
            allTimeRain - self.previousRain
        )  # Calculate the amount of rain that has fallen since last update
        if rainSinceLastUpdate > Device.maxRainJump:  # Filter rainfall spikes
            rainSinceLastUpdate = 0
            allTimeRain = self.previousRain

        self.previousRain = allTimeRain

        date = datetime.datetime.now()

        reading = WeatherReading(
            measuredAt=date,
            indoorTemperature=indoorTemperature,
            indoorHumidity=indoorHumidity,
            outdoorTemperature=outdoorTemperature,
            outdoorHumidity=outdoorHumidity,
            windSpeed=windSpeed,
            gustSpeed=gustSpeed,
            windDirection=windDirectionDegrees,
            outdoorDewPoint=outdoorDewPoint,
            windChill=windChill,
            seaLevelAirPressure=seaLevelAirPressure,
            allTimeRain=allTimeRain,
            rainSinceLastUpdate=rainSinceLastUpdate,
        )

        logger.debug(
            "Recieved reading:\n"
            + (
                " ".join(
                    [
                        str(date),
                        f"indoor humidity: {indoorHumidity},",
                        f"outdoor humidity: {outdoorHumidity},",
                        f"indoor temperature: {indoorTemperature:2.1f},",
                        f"outdoor temperature: {outdoorTemperature:2.1f},",
                        f"outdoor dew point: {outdoorDewPoint:2.2f},",
                        f"wind chill temp: {windChill:2.1f},",
                        f"wind speed: {windSpeed:2.1f},",
                        f"gust speed: {gustSpeed:2.1f},",
                        f"wind direction: {Device.windDirections[windDirection]},",
                        f"rain since last update: {rainSinceLastUpdate:2.1f},",
                        f"total rain since weather station reset: {allTimeRain:3.1f},",
                        f"air pressure at sea level: {seaLevelAirPressure:4.1f}",
                    ]
                )
            )
        )

        return reading
