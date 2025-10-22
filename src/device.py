import os
import struct
import math
import datetime

from core import Core
from report import Report
from logger import Logger

with os.add_dll_directory(Core.getPath("lib")) as _:
    import hid

class Device:
    windDirections = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    maxRainJump = 10

    def getDewPoint(temperature: float, humidity: float):
        """
        Using the supplied temperature and humidity to calculate the dew point
        """
        humidity /= 100.0
        gamma = (17.271 * temperature) / (237.7 + temperature) + math.log(humidity)
        return (237.7 * gamma) / (17.271 - gamma)

    def getWindChill(temperature: float, wind: float):
        """
        Using the supplied temperature and wind speed to calculate the wind chill
        factor.
        From Wikipedia: Wind-chill or windchill, (popularly wind chill factor) is
        the perceived decrease in air temperature felt by the body on exposed skin
        due to the flow of air
        """
        windKph = 3.6 * wind

        # Low wind speed, or high temperature, negates any perceived wind chill
        if ((windKph <= 4.8) or (temperature > 10.0)):
            return temperature

        windChill = 13.12 + (0.6215 * temperature) - \
            (11.37 * (windKph ** 0.16)) + \
            (0.3965 * temperature * (windKph ** 0.16))

        # Return the lower of temperature or wind chill temperature
        if (windChill < temperature):
            return windChill
        else:
            return temperature

    def __init__(self, vendorId = 0x1941, productId = 0x8021):
        self.vendorId = vendorId
        self.productId = productId
        self.previousRain = 0

    def __enter__(self):
        try:
            self.device = hid.Device(self.vendorId, self.productId)
            Logger.logInfo("Successfully connected to device.")
        except hid.HIDException as error:
            if error.args[0] == "unable to open device":
                raise ConnectionError("Couldn't connect to device.")
            else:
                raise error
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.device.close()

    def readBlock(self, offset):
        """
        Read a block of data from the specified device, starting at the given offset in bytes
        """

        leastSignificantBit = offset & 0xFF
        mostSignificantBit = offset >> 8 & 0xFF

        # Construct a binary message
        tbuf = struct.pack(
            "BBBBBBBB",
            0xA1,
            mostSignificantBit,
            leastSignificantBit,
            32,
            0xA1,
            mostSignificantBit,
            leastSignificantBit,
            32
        )

        timeout = 1000  # Milliseconds

        self.device.write(bytes([0x01]) + tbuf)

        block = bytearray()
        while len(block) < 32:
            chunk = self.device.read(8, timeout)
            if not chunk:
                raise IOError("Timed out while reading from weather station")
            block.extend(chunk)

        if len(block) > 32:
            raise IOError("Device returned too much data")

        return block

    def getReport(self):
        fixedBlock = self.readBlock(0)

        # Check that we have good data
        if (fixedBlock[0] != 0x55):
            raise ValueError("Bad data returned")

        # Bytes 31 and 32 when combined create an unsigned short int
        # that tells us where to find the weather data we want
        currentPosition = struct.unpack("H", fixedBlock[30:32])[0]
        currentBlock = self.readBlock(currentPosition)

        # Indoor information
        indoorHumidity = currentBlock[1]
        tlsb = currentBlock[2]
        tmsb = currentBlock[3] & 0x7f
        temperatureSign = currentBlock[3] >> 7
        indoorTemperature = (tmsb * 256 + tlsb) * 0.1
        # Check if temperature is less than zero
        if temperatureSign:
            indoorTemperature *= -1

        # Outdoor information
        outdoorHumidity = currentBlock[4]
        tlsb = currentBlock[5]
        tmsb = currentBlock[6] & 0x7f
        temperatureSign = currentBlock[6] >> 7
        outdoorTemperature = (tmsb * 256 + tlsb) * 0.1
        # Check if temperature is less than zero
        if temperatureSign:
            outdoorTemperature *= -1

        # Bytes 8 and 9 when combined create an unsigned short int
        # that we multiply by 0.1 to find the absolute pressure
        absoluteAirPressure = struct.unpack("H", currentBlock[7:9])[0]*0.1
        
        wind = currentBlock[9]
        gust = currentBlock[10]
        windExtra = currentBlock[11]
        windDirection = currentBlock[12]
        
        # Bytes 14 and 15  when combined create an unsigned short int
        # that we multiply by 0.3 to find the total rain
        # I"m not confident that this is correct. Neither abs_pressure nor
        # total_rain are returning sane values. In fact total_rain has
        # stayed static despite rainfall
        # Looks like I fixed it. They used fixed_block instead of current_block
        totalRain = struct.unpack("H", currentBlock[13:15])[0]*0.3

        # Calculate wind speeds
        windSpeed = (wind + ((windExtra & 0x0F) << 8)) * 0.38  # Was 0.1
        gustSpeed = (gust + ((windExtra & 0xF0) << 4)) * 0.38  # Was 0.1

        outdoorDewPoint = Device.getDewPoint(outdoorTemperature, outdoorHumidity)
        windChill = Device.getWindChill(outdoorTemperature, windSpeed)

        # In the first run there is no previous value, so we set it to the total amount of rain
        if self.previousRain == 0:
            self.previousRain = totalRain

        rainDiff = totalRain - self.previousRain # Calculate the amount of rain that has fallen since last update
        if rainDiff > Device.maxRainJump:  # Filter rainfall spikes
            rainDiff = 0
            totalRain = self.previousRain

        self.previousRain = totalRain

        date = datetime.datetime.now()

        report = Report(
            date,
            indoorTemperature,
            indoorHumidity,
            outdoorTemperature,
            outdoorHumidity,
            windSpeed,
            gustSpeed,
            windDirection,
            outdoorDewPoint,
            windChill,
            absoluteAirPressure,
            rainDiff
        )

        Logger.logInfo(" ".join([
            format(str(date)),
            format("indoor humidity: %i," %indoorHumidity),
            format("outdoor humidity: %i," %outdoorHumidity),
            format("indoor temperature: %2.1f," %indoorTemperature),
            format("outdoor temperature: %2.1f," %outdoorTemperature),
            format("outdoor dew point: %2.2f," %outdoorDewPoint),
            format("wind chill temp: %2.1f," %windChill),
            format("wind speed: %2.1f," %windSpeed),
            format("gust speed: %2.1f," %gustSpeed),
            format("wind direction: %s," %Device.windDirections[windDirection]),
            format("rain since last update: %2.1f," %rainDiff),
            format("total rain since weather station reset: %3.1f," %totalRain),
            format("absolute pressure: %4.1f," %absoluteAirPressure)
        ]))

        return report