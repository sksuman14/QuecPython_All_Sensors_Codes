from machine import I2C
from usr.stts751 import STTS751

# Init I2C (fast mode, like sht40main)
i2c = I2C(I2C.I2C0, I2C.FAST_MODE)

sensor = STTS751(i2c, address=0x48)  # Default I2C address

# Read temperature
temp = sensor.get_temperature()

print("Temperature:", temp, "°C")
