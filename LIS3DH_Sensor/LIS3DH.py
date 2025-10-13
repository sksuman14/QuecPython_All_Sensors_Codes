import log
from machine import I2C
import utime
# import ctypes

def read_acceleration_axis(): # Function to read x, y and z axis acceleration data   
        
        global x_axis, y_axis, z_axis # making axes  data global , so they can be called outside the function , when required

        global x_axis_signed,y_axis_signed,z_axis_signed # variables to store positive and negative values
        
        CTRL_REG1 =bytearray([0x20])   # register address where axes data is stored

        CTRL_REG1_enable=bytearray([0x17]) # command to enable axes data

        #write command to enables axes reading from specific register address
        i2c_obj.write(lis3dh_SLAVE_ADDR , CTRL_REG1, 1, CTRL_REG1_enable, 1)

        utime.sleep_ms(100) # providing 100ms delay after write command

        # print( CTRL_REG1)
        # print( CTRL_REG1_enable)
     
        # defining variable of type bytearray to store low/high data for x axis in byteaaray format
        OUT_X_L=bytearray([0x28])     
        OUT_X_H=bytearray([0x29])     
        
        i2c_obj.write(lis3dh_SLAVE_ADDR , b'', 0,  OUT_X_L, 1) # write cmd for lsb x axis
        utime.sleep_ms(100)
        # print(OUT_X_L)
        OUT_X_L_read=bytearray(1) # defining variable in bytearray format

        i2c_obj.read(lis3dh_SLAVE_ADDR , b'', 0, OUT_X_L_read, 1,0) # read cmd to read msb using OUT_X_L_read variable
        # print("lower aacn read",OUT_X_L_read) 
        i2c_obj.write(lis3dh_SLAVE_ADDR , b'', 0, OUT_X_H, 1)
        utime.sleep_ms(100)
        # print(OUT_X_H)
        OUT_X_H_read=bytearray(1) # defining variable in bytearray format

        i2c_obj.read(lis3dh_SLAVE_ADDR , b'', 0, OUT_X_H_read, 1,0) # read cmd to read msb using OUT_X_H_read variable
        # print("higher aacn read",OUT_X_H_read) 

        # Extracting high and low data from bytearray into integer to perform bit shifting
        x_low= OUT_X_L_read[0]
        X_high=OUT_X_H_read[0]
        x_axis=(X_high<<8)|x_low
        # print("this is combined data",x_axis)
        # print("this is binary of combined",bin(x_axis))

        #if MSB is 1 ,then it is a negative number and subsequently after which we perform 2's complement sbustraction to differentiate positive and negative numbers
        if x_axis & 0x8000:  # if MSB is set
                x_axis_signed = x_axis - 65536
                print("we are getting negative values")
                print(x_axis_signed)
        else:
                x_axis_signed = x_axis # else number is positive and assign as it is to z_axis_signed
                print("we are getting posititve values")
                print(x_axis_signed)    

        # reading Y axis data 
        # command to write msb/lsb (L/H) data in bytearrray format
        OUT_Y_L=bytearray([0X2A])
        OUT_Y_H=bytearray([0X2B])
        i2c_obj.write(lis3dh_SLAVE_ADDR,b'',0, OUT_Y_L,1)
        i2c_obj.write(lis3dh_SLAVE_ADDR,b'',0,OUT_Y_H,1)

        utime.sleep_ms(100) # Providing 100 ms delay after write command

        # defining variables to store data in bytearry format
        OUT_Y_L_read=bytearray(1)
        OUT_Y_H_read=bytearray(1)
        i2c_obj.read(lis3dh_SLAVE_ADDR,b'',0,OUT_Y_L_read,1,0)
        i2c_obj.read(lis3dh_SLAVE_ADDR,b'',0,OUT_Y_H_read,1,0)
        # print("raw y axis low",OUT_Y_L_read)
        # print("raw y axis high", OUT_Y_H_read)

        # Extracting data from bytearrray format to integer variable to perform bit shifting
        y_low=OUT_Y_L_read[0]
        y_high=OUT_Y_H_read[0]
        y_axis=(y_low<<8)|y_high

        # comapring y axis data if MSB=1 then the number is negative and subsequently after which bit shifting will be performed
        if y_axis & 0x8000:  
                y_axis_signed = y_axis - 65536
                print("we are getting negative values of Y")
                print(y_axis_signed)
        else:
                y_axis_signed = y_axis # else number is positive and assign as it is to y_axis_signed
                print("we are getting posititve values of Y")
                print(y_axis_signed) 
        # print("Y axis data", y_axis)

        # now reading z axis data
        # Taking z axis lsb/msb(L/H) data in bytearray format
        OUT_Z_L=bytearray([0X2C])
        OUT_Z_H=bytearray([0X2D])

        # write command to store z axis low and high data
        i2c_obj.write(lis3dh_SLAVE_ADDR,b'',0, OUT_Z_L,1)
        i2c_obj.write(lis3dh_SLAVE_ADDR,b'',0,OUT_Z_H,1)
        utime.sleep_ms(100)

        # defining variables of  lsb/msb(L/h) data in bytearray format
        OUT_Z_L_read=bytearray(1)
        OUT_Z_H_read=bytearray(1)
        i2c_obj.read(lis3dh_SLAVE_ADDR,b'',0,OUT_Z_L_read,1,0)
        i2c_obj.read(lis3dh_SLAVE_ADDR,b'',0,OUT_Z_H_read,1,0)
        # print("raw z axis low",OUT_Z_L_read)
        # print("raw z axis low",OUT_Z_H_read)

        # Extracting the variables from byearray to integer format to perform bit shifting 
        z_low=OUT_Z_L_read[0]
        z_high=OUT_Z_H_read[0]
        z_axis=(z_low<<8)|z_high
        # print("Z axis data", z_axis)

        # comparing z_axis output 
        #if MSB is 1 ,then it is a negative number and subsequently after which we perform 2's complement sbustraction to differentiate positive and negative numbers
        if z_axis & 0x8000:  # 
                z_axis_signed = z_axis - 65536
                print("we are getting negative values of z")
                print(z_axis_signed)
        else:
                z_axis_signed = z_axis # else number is positive and assign as it is to z_axis_signed
                print("we are getting posititve values of z")
                print(z_axis_signed) 
       
        return 0



if __name__ == '__main__':
        i2c_obj = I2C(I2C.I2C0, I2C.FAST_MODE) 
        lis3dh_SLAVE_ADDR = 0x19 # I2C device address 
        while True:
                read_acceleration_axis() # calling variable to read x ,y and z axis data
                utime.sleep(1)
                print("x: {} | y: {} | z: {}\n\r".format(x_axis_signed*0.00059815, y_axis_signed*0.00059815, z_axis_signed*0.00059815))

           
                
