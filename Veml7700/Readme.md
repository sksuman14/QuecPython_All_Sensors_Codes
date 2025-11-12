## VEML7700 Ambient Light Sensor (Quecpython)

This file provides the necessary Quecpython I2C communication and logic to read raw and calculated ambient light levels (Lux) from the VEML7700 sensor.

# Overview

The code initializes an I2C connection, configures the VEML7700 with specific settings for gain and integration time, and then continuously reads the 16-bit light data to calculate the final Lux value.


# Hardware

Quectel EC200 U board

VEML7700 Ambient Light Sensor Module (I2C)

Dependencies

machine (for I2C communication)

utime (for timing and delays)

 Wiring (I2C)

Connect the VEML7700 module to your microcontroller's I2C pins:

 # Sensor Configuration

The file uses the following configuration settings defined in config_cmd = bytearray([0x10, 0x00]) for the Configuration Register (0x00).

Setting

Value in Code

Description

ALS_GAIN

1/8 ,Gain setting (reduces sensitivity)

ALS_IT

100 ms Integration Time (conversion speed)

ALS_SD, 0, Shutdown mode (0 = normal operation)


I2C Address

0x10

Default 7-bit I2C address for VEML7700

 Code Logic Explained

I2C Setup and Write

i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)
# Configure ALS_GAIN=1/8, ALS_IT=100ms, ALS_SD=0
i2c_obj.write(veml7700_slave_address, register_add, 1, config_cmd, 2)
utime.sleep_ms(200) # Wait for initialization


The sensor is initialized and configured to start measurements.

Data Read and Bit Shifting

The raw light data is read from the ALS Data Register (0x04) which returns 2 bytes (16 bits):

# Raw data is read into 'data' bytearray: [LSB, MSB]
i2c_obj.read(veml7700_slave_address, read_reg, 1, data, 2, 0)
lux_lsb=data[0]
lux_msb=data[1]
# Reconstruct 16-bit value: MSB (shifted 8 bits left) OR LSB
raw_lux_data=(lux_msb<<8|lux_lsb)


This bit shifting operation correctly combines the LSB and MSB bytes into a single 16-bit integer value (raw_lux_data).

Lux Calibration Formula

# The final Lux value is calculated using the following formula:

Light level [lx] is (ALS OUTPUT DATA [dec.] / ALS Gain x responsivity).