import utime
from machine import I2C

# LTR390 I2C address and register definitions
LTR390_I2C_ADDR = 0x53
MAIN_CTRL = 0x00
MEAS_RATE = 0x04
GAIN = 0x05
UVS_DATA_0 = 0x10
UVS_DATA_1 = 0x11
UVS_DATA_2 = 0x12
MAIN_STATUS = 0x07

# Settings values
UVS_MODE = 0x0A  # UVS active mode
RESOLUTION_18BIT_TIME100MS = 0x20
GAIN_3X = 0x01

def write_reg(i2c, reg, val):
    reg_addr = bytearray([reg])
    data = bytearray([val])
    i2c.write(LTR390_I2C_ADDR, reg_addr, 1, data, 1)

def read_reg(i2c, reg):
    reg_addr = bytearray([reg])
    read_buf = bytearray(1)
    i2c.write(LTR390_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(LTR390_I2C_ADDR, b'', 0, read_buf, 1, 0)
    return read_buf[0]

def burst_read(i2c, start_reg, length):
    reg_addr = bytearray([start_reg])
    read_buf = bytearray(length)
    i2c.write(LTR390_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(LTR390_I2C_ADDR, b'', 0, read_buf, length, 0)
    return read_buf

if __name__ == '__main__':
    i2c = I2C(I2C.I2C0, I2C.FAST_MODE)

    # Configure sensor registers
    write_reg(i2c, MAIN_CTRL, UVS_MODE)
    write_reg(i2c, MEAS_RATE, RESOLUTION_18BIT_TIME100MS)
    write_reg(i2c, GAIN, GAIN_3X)

    utime.sleep_ms(100)

    while True:
        # Check if data is ready by reading status register and checking bit 3 (0x08)
        status = read_reg(i2c, MAIN_STATUS)
        if (status & 0x08) == 0:
            print("Data not ready, waiting...")
            utime.sleep_ms(1000)
            continue

        # Read three bytes UV data
        uv_bytes = burst_read(i2c, UVS_DATA_0, 3)

        # Combine the three bytes little endian (UVS_DATA_2 is highest byte)
        uv_index = (uv_bytes[2] << 16) | (uv_bytes[1] << 8) | uv_bytes[0]

        print("UV Index: {}".format(uv_index))

        utime.sleep_ms(1000)
