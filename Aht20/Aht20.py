import log
from machine import I2C
import utime
from machine import Pin

def initialize_registers(): # function to initialize registers
    initialize_cmd=bytearray([0x1B, 0x1C, 0x1E]) # initialization command in bytearray format
    i2c_obj.write(AHt20_SLAVE_ADDR, b'', 0,  initialize_cmd, 3) # write command for initialization
    return initialize_registers

def read_status(): 
    status_cmd = bytearray([0x71]) # register to read status once sensor is powered on in bytearray format
    # status= bytearray([0x18])
    # print()
    i2c_obj.write(AHt20_SLAVE_ADDR, b'', 0, status_cmd, 1)  # write command for AHt20
    utime.sleep_ms(200)
    # i2c_obj.write(AHt20_SLAVE_ADDR, b'', 0, status, 1)                          
    status = bytearray(1) # vaue of write command stored in bytearray format
    i2c_obj.read(AHt20_SLAVE_ADDR, b'', 0, status, 1, 0) # command to read status value
    # i2c_obj.read(AHt20_SLAVE_ADDR, b'', 0, status, 1, 0)
    return status
if __name__ == '__main__':
    i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE) # creates and initializes an I2C communication object
    utime.sleep_ms(100) # delay after initialization
    AHt20_SLAVE_ADDR = 0x38 # Aht20 i2c address
    status_check=read_status() # passing the value  obtained from read_status function to status_check variable
    x = bytearray([0x18]) # value in hex that should match with read_status command
    print(status_check)
    if (status_check==x): 
        print("I am ready")
    else:
        initialize_registers() # calling function to execute sensor initialization
        print("sensors initialized pls proceed")
        utime.sleep_ms(10) 
    #  measurement command
    utime.sleep_ms(10)
    direct_cmd = bytearray([0xAC]) # register address for temperature and humidity measurement
    measurement_cmd=bytearray([0x33,0x00])   # command for temperature and humidity measurement
    while True:
        i2c_obj.write(AHt20_SLAVE_ADDR, direct_cmd, 1, measurement_cmd, 2) # write command for temperature and humidity measurement
        utime.sleep(1) # delay after write command
        read_measurement=bytearray(7) # value of temperature and humidity measurement ontained in bytearray format
        i2c_obj.read(AHt20_SLAVE_ADDR, b'', 0, read_measurement, 7,0)
        utime.sleep(1)
         # print("current measurement",read_measurement ) # Temperature and humidity measurement obtained in raw format
        my_data=read_measurement # extracting read measurement data obtained in bytearray format to integer variable  to perform bit manipulation
        # print(my_data[1])
        # print(my_data[2])
        # print(my_data[3])
        # performing bit manipulation
        humidity_raw=(my_data[1]<<12)|(my_data[2]<<4)|(my_data[3]>>4) # bit manipulation to get raw humidity data in digital format
        temperature_raw=(my_data[3] & 0x0F )<<16| (my_data[4]<<8)|(my_data[5])# bit manipulation to get raw temperature data in digital format
         # print("this is raw value for temperatue",temperature_raw)
         # print("this is humidity raw", humidity_raw)
        humidity_new=(humidity_raw/1048576)*100 # callibration as specified in the datasheet of AHT20 sensor
        temperature_new=(temperature_raw/1048576)*200-50 # callibration as specified in the datasheet AHT20 sensor   
        print("the  humidity is {:.2f} %".format(humidity_new)) # calibrated humidity data
        print("the  temperature is {:.2f} C".format(temperature_new)) # calibrated temperature data
        utime.sleep(1)
        
        