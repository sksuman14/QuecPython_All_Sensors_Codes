## Overview

This file interfaces with the AHT20 temperature and humidity sensor using the I2C protocol. 
It initializes the sensor, checks its status, triggers a measurement, and reads calibrated humidity and temperature data.

## Features

Initializes AHT20 sensor registers.

Verifies sensor readiness through status register.

Performs measurement command for humidity and temperature.

Extracts and calculates humidity and temperature from raw data using bit manipulation.

## Requirements

# Hardware:
AHT20 sensor module connected via I2C.

# Software:

Quecpython environment compatible with EC200U.

machine, utime, and log modules supported.


## Code Workflow

Initialize I2C:

i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)


# Check Sensor Status:

Sends command 0x71 to read status.

If status byte equals 0x18, sensor is ready.

Otherwise, execute register initialization.

Initialize Registers (if needed):

Sends sequence [0x1B, 0x1C, 0x1E] to prepare the sensor.

# Trigger Measurement:

Sends command [0xAC, 0x33, 0x00] to start reading humidity and temperature.

Read and Process Data:

Reads 8 bytes of data.

Extracts humidity and temperature raw values.

Converts them into human-readable values:

humidity_new = (humidity_raw / 1048576) * 100
temperature_new = (temperature_raw / 1048576) * (200 - 50)


# Display Results:

Prints humidity and temperature 10 times for monitoring.