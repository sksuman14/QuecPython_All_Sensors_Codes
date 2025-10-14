import utime
from machine import I2C

# VL53L0X I2C address
VL53L0X_I2C_ADDR = 0x29  # 7-bit address

# Register definitions
SYSRANGE_START          = 0x00
RESULT_RANGE_STATUS     = 0x14
SYSTEM_INTERRUPT_CLEAR  = 0x0B
FINAL_RANGE_MSB         = 0x1E
FINAL_RANGE_LSB         = 0x1F

def write_reg(i2c, reg, val):
    reg_addr = bytearray([reg])
    data = bytearray([val])
    i2c.write(VL53L0X_I2C_ADDR, reg_addr, 1, data, 1)

def read_reg(i2c, reg):
    reg_addr = bytearray([reg])
    read_buf = bytearray(1)
    i2c.write(VL53L0X_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(VL53L0X_I2C_ADDR, b'', 0, read_buf, 1, 0)
    return read_buf[0]

def burst_read(i2c, start_reg, length):
    reg_addr = bytearray([start_reg])
    read_buf = bytearray(length)
    i2c.write(VL53L0X_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(VL53L0X_I2C_ADDR, b'', 0, read_buf, length, 0)
    return read_buf

if __name__ == '__main__':
    i2c = I2C(I2C.I2C0, I2C.FAST_MODE)

    print("VL53L0X simple ranging demo")

    while True:
        # Start single ranging measurement
        write_reg(i2c, SYSRANGE_START, 0x01)

        # Instead of waiting for status, just sleep (typical measurement time ~33ms)
        utime.sleep_ms(50)

        # Read distance result (2 bytes)
        dist_bytes = burst_read(i2c, FINAL_RANGE_MSB, 2)
        distance_mm = (dist_bytes[0] << 8) | dist_bytes[1]
        distance_cm = distance_mm / 10.0
        print("Distance is {:.2f} cm".format(distance_cm))

        # Clear interrupt just in case
        write_reg(i2c, SYSTEM_INTERRUPT_CLEAR, 0x01)

        utime.sleep_ms(500)
