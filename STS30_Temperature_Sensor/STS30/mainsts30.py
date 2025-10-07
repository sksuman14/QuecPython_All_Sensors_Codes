from machine import I2C
from usr.sts30 import STS30

# Init I2C
i2c = I2C(I2C.I2C0, I2C.FAST_MODE)

sensor = STS30(i2c, address=0x4A)

temp = sensor.get_temperature()
print("Temperature:", temp, "°C")
