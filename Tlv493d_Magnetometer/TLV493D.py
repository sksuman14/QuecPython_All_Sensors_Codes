import utime
from machine import I2C

TLV493D_I2C_ADDR = 0x5E  # most common address (7-bit)

# Register map
DATA_REG_START = 0x00   # Bx, By, Bz, Temp registers start here (6 bytes)

def write_reg(i2c, reg, val):
    reg_addr = bytearray([reg])
    data = bytearray([val])
    i2c.write(TLV493D_I2C_ADDR, reg_addr, 1, data, 1)

def read_reg(i2c, reg):
    reg_addr = bytearray([reg])
    read_buf = bytearray(1)
    i2c.write(TLV493D_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(TLV493D_I2C_ADDR, b'', 0, read_buf, 1, 0)
    return read_buf[0]

def burst_read(i2c, start_reg, length):
    reg_addr = bytearray([start_reg])
    read_buf = bytearray(length)
    i2c.write(TLV493D_I2C_ADDR, b'', 0, reg_addr, 1)
    utime.sleep_ms(1)
    i2c.read(TLV493D_I2C_ADDR, b'', 0, read_buf, length, 0)
    return read_buf

def twos_complement(val, bits):
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

if __name__ == '__main__':
    i2c = I2C(I2C.I2C0, I2C.FAST_MODE)

    print("TLV493D 3D Magnetic Sensor Demo")

    while True:
        # Read 6 bytes starting from 0x00
        data = burst_read(i2c, DATA_REG_START, 6)

        # 12-bit values packed: (Bx, By, Bz, Temp)
        bx = ((data[0] << 4) | (data[4] & 0x0F))
        by = ((data[1] << 4) | (data[4] >> 4))
        bz = ((data[2] << 4) | (data[5] & 0x0F))

        # Convert from 12-bit two's complement
        bx = twos_complement(bx, 12)
        by = twos_complement(by, 12)
        bz = twos_complement(bz, 12)

        # Scale to physical units
        bx_mT = bx * 0.098   # mT
        by_mT = by * 0.098
        bz_mT = bz * 0.098

        print("x: {:.2f} mT, y: {:.2f} mT, z: {:.2f} mT"
              .format(bx_mT, by_mT, bz_mT))

        utime.sleep_ms(500)

