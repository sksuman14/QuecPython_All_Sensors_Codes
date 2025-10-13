## Overview

This project demonstrates how to interface the SHT40 temperature and humidity sensor with Quectel EC-200u microcontroller using the I2C protocol in Quecpython. The code initializes communication with the SHT40 sensor, triggers  temperature and humidity measurement, and converts the raw data into human-readable values  for temperature and for humidity.

# Initilization 

Initializes the SHT40 sensor over the I2C bus.

Triggers  temperature and humidity measurements.

Reads and converts raw data to calibrated temperature (c) and humidity (%RH) values.


# Code Explanation

1. Library Imports

The following QuecPython libraries are used:

machine.I2C: Establishes I2C communication with the SHT40 sensor.

utime: Provides delay functions for timing control.

2. Main Program Execution

Initializes I2C communication on port I2C0 in standard mode.

Defines the SHT40 sensor's I2C address (0x44).

3. Trigger and Read Measurement

Sends the measurement command (0xFD) to the sensor.

Waits 200ms for the sensor to process the measurement.

Reads 6 bytes of data (temperature, humidity, and CRC).

4. Data Conversion

Extracts raw temperature (bytes 0-1) and humidity (bytes 3-4) values.

Converts raw data to human-readable values using the SHT40 datasheet formulas:

# Overview
Prints the temperature and humidity values.

