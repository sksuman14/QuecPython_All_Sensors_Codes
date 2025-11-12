import log
from machine import I2C
import utime

if __name__ == '__main__':
    i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE) #
    veml7700_slave_address = 0x10  # veml 7700 I2C  address
    # Configure config_cmd with ALS_GAIN=(1/8), ALS_IT=100ms, ALS_SD=0 , ALS Persistence=1 (Parameters as specified in the veml7700 datasheet)
    register_add = bytearray([0x00]) # register address
    config_cmd = bytearray([0x10, 0x00])  # configuration  cmd 
    # Commmands to set other specific gainS
    # ([0x00,0x00]) gain=1
    # ([0x08,0x00]) gain=2
    # ([0x10,0x00]) gain=1/8 (current)
    # ([0X18,0X00]) gain=1/4

    i2c_obj.write(veml7700_slave_address, register_add, 1, config_cmd, 2)
    utime.sleep_ms(200)  # delay
    # Read ALS data (register 0x04, 2 bytes)
    read_reg = bytearray([0x04])
    data = bytearray(2)
    while True:
        i2c_obj.read(veml7700_slave_address, read_reg, 1, data, 2, 0)
        # print("Raw data:", data) # printing raw data
        # Performing bit shifting and extracting lsb and msb data
        lux_lsb=data[0]
        lux_msb=data[1]
        raw_lux_data=(lux_msb<<8|lux_lsb) # Performing bit shifting
        # print(raw_lux_data) # printing raw_lux_data
        Light_level  = (raw_lux_data / 1/8) * (10 / 100 ) # calibration formula for lux
        utime.sleep(1)
        print("The light level is", Light_level,"lux") # lux level






    
