## LIS3DH Accelerometer Sensor Project

LIS3DH Accelerometer Sensor Project! This code enables us  to read acceleration data (x, y, and z axes) from the LIS3DH, a 3-axis accelerometer by STMicroelectronics, commonly used in devices like wearables and IoT projects. 

# LIS3DH
Measures acceleration along the x, y, and z axes to detect movement or tilt.

# Uses
Ideal for motion detection, orientation sensing, or step counting in applications like smartwatches.

## How to Set It Up

# Hardware: 
Connect the LIS3DH to Quectel EC200U, using the address 0x19.

# Software: 
Use a Quecpython environment. Import required libraries (machine, utime) and run the file.

# Configuration:
 The code initializes the sensor and sets the control register (0x20) to 0x17 for enabling the axes .

## How It Works

# Data Reading:
 The file reads raw acceleration data from registers:

X-axis: 0x28 (LSB) and 0x29 (MSB)
Y-axis: 0x2A (LSB) and 0x2B (MSB)
Z-axis: 0x2C (LSB) and 0x2D (MSB)


# Processing: 
Combines LSB and MSB via bit shifting , checks the most significant bit (MSB) to determine if the value is positive or negative (using 0x8000 mask), and applies a conversion factor (0.00059815) to convert to g units.

# Multiplication factor
The multiplication by 0.00059815 in  LIS3DH accelerometer code is used to convert the raw acceleration data (in digital counts) into a meaningful physical unit, specifically gravitational acceleration (g), where 1 g = 9.8 m/s sq. 

# Output:
Prints signed acceleration values for x, y, and z axes , e.g., "x: 0.0012 | y: -0.0009 | z: 0.0021".