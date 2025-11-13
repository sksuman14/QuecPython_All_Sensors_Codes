# BME680 interfacing

## Overview:
The BME680 is a compact, high-performance environmental sensor manufactured by Bosch Sensortec.
It is an all-in-one sensor that measures following parameters:

Temperature(c)

Barometric Pressure (hPa)

Relative Humidity (%)

## Hardware Interfacing
The project utilizes the I2C communication protocol for interfacing the BME680 sensor with the Quectel EC200U board. The connection adheres to the standard I2C wiring convention and power supply.

## System Requirements
- **Hardware**:
  - Quectel EC200U GSM Modem
  
- **Software**:
  - Python environment compatible with QuecPython platform
  
 ## Oversampling in BME680

Oversampling involves taking multiple samples of a measurement (e.g., temperature, pressure, or humidity) during a single cycle and averaging them to reduce noise and enhance precision  

## Initialization:
    Write to the hum_reg (0x72) to set the oversampling rate for humidity (bits osrs_h<2:0>) .
    
    Configure Temperature and Pressure Oversampling.

    Set up the microcontroller's I2C communication with the BME680 at its slave address (e.g., 0x76) to enable data writing and reading (Section 5.1, page 27).
    Configure Humidity Oversampling:
    
    Write to the  temp_and_press_regr (0x74) to set oversampling for temperature (bits osrs_t<2:0>) and pressure (bits osrs_p<2:0>) from 1x (001) to 16x (101), per Table 7 (page 30).
       
    Set Operating Mode:
    Configure the ctrl_meas register (0x74) mode (bits mode<1:0>):.
    
    Initiate measurement by setting forced or continuous mode in ctrl_meas (0x74),  to complete the cycle (Section 3.3, page 17).

## Calibration

# Temperature and Pressure
    Raw temperature and pressure values are obtained by combining the MSB, LSB, and XLSB data from the respective data registers (Section 5.3.4, page 35) of BME680 datasheet.

    After acquiring these raw values, calibration formulas specified in Section 3.3.1 (page 17) for temperature and Section 3.3.2 (page 18) for pressure of the BME680 datasheet are applied using factory calibration parameters from the trim registers (Section 5.3.2, page 30) to convert the raw ADC outputs into compensated, physically meaningful measurements in c and hPa, respectively.

# Humidity
    Raw humidity values are derived by combining MSB and LSB data from registers 0x25-0x26 (Section 5.3.4, page 35). These raw values are then processed using the calibration formula in Section 3.3.3 (page 19) with factory parameters from the trim registers (Section 5.3.2, page 30) to yield a compensated percentage relative humidity.

# Calibration Parameters
    Each measurement type (temperature, pressure, and humidity) has its own set of calibration parameters, typically denoted with prefixes like "t" for temperature, "p" for pressure, and "h" for humidity, followed by numerical suffixes (e.g., t1, p1, h1). These parameters serve distinct roles:

    Baseline Parameters (e.g., t1, p1, h1): These are positive, unsigned values that establish a starting point or reference for the measurement, sourced from specific register pairs in the sensor's memory.

    Adjustment Parameters (e.g., t2, t3, p2, h2-h7): These are signed values ( capable of being positive or negative or Zero ) that fine-tune the readings, correcting for non-linearities, temperature influences, or other variations, and are stored in additional registers.