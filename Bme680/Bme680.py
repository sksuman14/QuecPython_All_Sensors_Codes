import log
from machine import I2C
import utime

tfine=0

# if __name__ == '__main__':
i2c_obj = I2C(I2C.I2C0, I2C.STANDARD_MODE)



class BME:

    def __init__(self):
        print("Sensor Initialized")
    def read_Temperature_and_Pressure(self):
        global tfine 
        BME680_slave_address = 0x76   #BME680 I2C  address 

        temp_and_press_reg=bytearray([0x74])  # Temperature and pressure register address

        temp_and_press_cmd=bytearray([0x25])  # Temperature and pressure register command keeping oversampling value=1 .                   
        # Oversampling  BME680 is taking  multiple readings of a value like tempertature or pressure and average them out together.
        # Oversampling increases measurement accuracy.


        # write command for temperature and Pressure
        # Parameters parsed :
        # BME680 i2C address, lsb/msb for temperature ,temperature lsb/msb register address , command to read temperature and pressure 

        i2c_obj.write(BME680_slave_address, temp_and_press_reg, 1, temp_and_press_cmd , 1)
        utime.sleep_ms(100)

        # register address for temperature MSB,LSB and XSLB

        temp_msb=bytearray([0x22])
        temp_lsb=bytearray([0x23])
        temp_xlsb=bytearray([0x24])

        # variables of type bytearray and length=1  to store out MSB, LSB and XLSB for temperature

        data_msb=bytearray(1)
        data_lsb=bytearray(1)
        data_xlsb=bytearray(1)


        # read command for temperature MSB, LSB and XLSB
        # Parameters parsed :
        # BME680 i2C address, lsb/msb for temperature ,temperature lsb/msb register address , data variables to store temperature lsb/msb data , delay

        i2c_obj.read(BME680_slave_address, temp_msb, 1, data_msb, 1,0)
        # print(data_msb)
        i2c_obj.read(BME680_slave_address, temp_lsb, 1, data_lsb, 1,0)
        # print(data_lsb)
        i2c_obj.read(BME680_slave_address, temp_xlsb, 1, data_xlsb, 1,0)
        # print(data_xlsb)

        # extracting MSB,LSB and XLSB from bytearray to integer  to perform bit shifting

        data_h=data_msb[0]
        data_l=data_lsb[0]
        data_xl=data_xlsb[0]

        # performing bit shifting on MSB,LSB and XLSB 

        temp_raw=(data_h<<12)|(data_l<<4)|(data_xl>>4)
        # print(temp_raw) # Getting the value of temperature in raw format here

        # calibration process for temperature

        # t1, t2 and t3 are calibration parameters for temperature , they are write only registers for temperature calibration
        #signed= Positive , Negative or Zero
        #Unsigned= Only Positive
        # signed and unsigned nature of these parameters depend how they are further used in caluculation


        #reading out msb and lsb for t1

        par_t1_msb=bytearray([0xEA])    
        par_t1_lsb=bytearray([0XE9])

        # defining a variable of type bytearray , length 1 to store msb and lsb data for t1

        data_msb=bytearray(1)
        data_lsb=bytearray(1)

        # reading lsb and msb for t1

        i2c_obj.read(BME680_slave_address,par_t1_lsb,1,data_lsb,1,0)
        i2c_obj.read(BME680_slave_address,par_t1_msb,1,data_msb,1,0)

        # extracting t1 data from bytearray to perform bit shifting

        t1_lsb=data_lsb[0]
        t1_msb=data_msb[0]
        t1_par=(t1_msb<<8)|t1_lsb
        # print(t1_par)

        # reading out msb and lsb registers for t2 

        par_t2_msb=bytearray([0X8B])
        par_t2_lsb=bytearray([0X8A])

        # defining a variable of type bytearray , length 1 to store msb and lsb data for t2

        t2_data_msb=bytearray(1)
        t2_data_lsb=bytearray(1)

        #  reading  msb and lsb for t2

        i2c_obj.read(BME680_slave_address,par_t2_msb,1,t2_data_msb,1,0)
        i2c_obj.read(BME680_slave_address,par_t2_lsb,1,t2_data_lsb,1,0)

        #  Extracting t2 lsb and msb to perform bit shifting

        t2_lsb=t2_data_lsb[0]
        t2_msb=t2_data_msb[0]
        t2_par=(t2_msb<<8)|(t2_lsb)
        # print(t2_par)

        # reading t3 lsb 
        par_t3_lsb=bytearray([0x8C])

        # data to store t3 lsb 
        data_t3_lsb=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_t3_lsb,1,data_t3_lsb,1,0)

        # extracting t3 data from lsb
        t3_lsb=data_t3_lsb[0]
        # print(t3_lsb)

        # calibration formula to calculate temperature

        var1=((temp_raw/16384.0)-(t1_par/1024.0)) * t2_par
        var2=((temp_raw/131072.0)-(t1_par/8192.0))**2  *(t3_lsb*16.0)

        # tfine variable to be used in pressure and humidity calibration

        tfine=var1+var2


        Temperature=(tfine/5120.0)


        # print("Temperature",Temperature,"c") # Temperature output after calibration

        #  calculating pressure

        # register address for msb,lsb and xlsb for pressure

        press_msb=bytearray([0x1F])
        press_lsb=bytearray([0x20])
        press_xlsb=bytearray([0x21])

        # bytearray variale of length=1 to store msb,lsb and xlsb data obtained from these registers

        data_press_msb=bytearray(1)
        data_press_lsb=bytearray(1)
        data_press_xlsb=bytearray(1)

        # reading msb, lsb and xlsb register address for pressure

        i2c_obj.read(BME680_slave_address,press_msb,1,data_press_msb,1,0)
        # print(data_press_msb)
        i2c_obj.read(BME680_slave_address,press_lsb,1,data_press_lsb,1,0)
        # print(data_press_lsb)
        i2c_obj.read(BME680_slave_address,press_xlsb, 1, data_press_xlsb, 1,0)
        # print(data_press_xlsb)

        # variable to store extracted data from bytearray variable to perform bit shifting

        data_msb_p=data_press_msb[0]
        data_lsb_p=data_press_lsb[0]
        data_xlsb_p=data_press_xlsb[0]

        pressure_raw=(data_msb_p<<12)|(data_lsb_p<<4)|(data_xlsb_p>>4)
        # print("This is raw pressure",pressure_raw) # Pressure output obtained in raw format

        # Calibration Parameters
        # par_p1,par_p2,par_p3.....par_p10  are calibration parameters 
        # reading lsb and msb for these parameters 
        # the below mentioned parameters are write only registers for pressure to be used further in calculation
        # p1, p2 , p3...p10 are calibration parameters for temperature , they are write only registers for temperature calibration
        #signed= Positive , Negative or Zero
        #Unsigned= Only Positive
        # signed and unsigned nature of these parameters depend how they are further used in caluculation
        # If the parameter is subtracted or multiplied in the formula then its signed
        # If its only added in caibration formula then its unsigned

        par_p1_lsb=bytearray([0x8E])
        par_p1_msb=bytearray([0x8F])
        par_p1_lsb_data=bytearray(1)
        par_p1_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p1_lsb,1,par_p1_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p1_msb,1,par_p1_msb_data,1,0)
        par_p1_h=par_p1_msb_data[0]
        par_p1_l=par_p1_lsb_data[0]
        par_p1=par_p1_h<<8|par_p1_l
        # print("par_p1",par_p1)

        par_p2_lsb=bytearray([0x90])
        par_p2_msb=bytearray([0x91])
        par_p2_lsb_data=bytearray(1)
        par_p2_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p2_lsb,1,par_p2_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p2_msb,1,par_p2_msb_data,1,0)
        par_p2_h=par_p2_msb_data[0]
        par_p2_l=par_p2_lsb_data[0]
        par_p2=par_p2_h<<8|par_p2_l
        # print("par_p2",par_p2)
        if par_p2 & 0x8000:
            par_p2_signed=par_p2-65536
        else:
            par_p2_signed=par_p2


        # par_p2_lsb=bytearray([0x90])
        par_p3=bytearray([0x92])
        par_p3_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p3,1,par_p3_data,1,0)
        par_p3_d=par_p3_data[0]
        # print("par_p3",par_p3_d)

        par_p4_lsb=bytearray([0x94])
        par_p4_msb=bytearray([0x95])
        par_p4_lsb_data=bytearray(1)
        par_p4_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p4_lsb,1,par_p4_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p4_msb,1,par_p4_msb_data,1,0)
        par_p4_h=par_p4_msb_data[0]
        par_p4_l=par_p4_lsb_data[0]
        par_p4=par_p4_h<<8|par_p4_l
        # print("par_p4",par_p4)
        if par_p4 & 0x8000:
            par_p4_signed=par_p4-65536
        else:
            par_p4_signed=par_p4

        par_p5_lsb=bytearray([0x96])
        par_p5_msb=bytearray([0x97])
        par_p5_lsb_data=bytearray(1)
        par_p5_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p5_lsb,1,par_p5_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p5_msb,1,par_p5_msb_data,1,0)
        par_p5_h=par_p5_msb_data[0]
        par_p5_l=par_p5_lsb_data[0]
        par_p5=par_p5_h<<8|par_p5_l
        # print("par_p5",par_p5)
        if par_p5 & 0x8000:
            par_p5_signed=par_p5-65536
        else:
            par_p5_signed=par_p5

        par_p6=bytearray([0x99])
        par_p6_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p6,1,par_p6_data,1,0)   
        par_p6_d=par_p6_data[0]
        # print("par_p6_d",par_p6_d)

        par_p7=bytearray([0x98])
        par_p7_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p7,1,par_p7_data,1,0)   
        par_p7_d=par_p7_data[0]
        # print("par_p7",par_p7_d)

        par_p8_lsb=bytearray([0x9C])
        par_p8_msb=bytearray([0x9D])
        par_p8_lsb_data=bytearray(1)
        par_p8_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p8_lsb,1,par_p8_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p8_msb,1,par_p8_msb_data,1,0)
        par_p8_h=par_p8_msb_data[0]
        par_p8_l=par_p8_lsb_data[0]
        par_p8=par_p8_h<<8|par_p8_l
        # print("par p8",par_p8)
        if par_p8 & 0x8000:
            par_p8_signed=par_p8-65536
        else:
            par_p8_signed=par_p8

        par_p9_lsb=bytearray([0x9E])
        par_p9_msb=bytearray([0x9F])
        par_p9_lsb_data=bytearray(1)
        par_p9_msb_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p9_lsb,1,par_p9_lsb_data,1,0)
        i2c_obj.read(BME680_slave_address,par_p9_msb,1,par_p9_msb_data,1,0)
        par_p9_h=par_p9_msb_data[0]
        par_p9_l=par_p9_lsb_data[0]
        par_p9=par_p9_h<<8|par_p9_l
        # print("par p9",par_p9)
        if par_p9 & 0x8000:
            par_p9_signed=par_p9-65536
        else:
            par_p9_signed=par_p9

        par_p10=bytearray([0xA0])
        par_p10_data=bytearray(1)
        i2c_obj.read(BME680_slave_address,par_p10,1,par_p10_data,1,0)   
        par_p10_d=par_p10_data[0]
        # print("par p10",par_p10_d)
        if par_p10_d & 0x8000:
            par_p10_d_signed=par_p10_d-65536
        else:
            par_p10_d_signed=par_p10_d


        # calibration formula for pressure as per datasheet

        pres_ovf_check=0x40000000
        var1 = (int(tfine) >> 1) - 64000
        var1_t_term = var1 
        var2_p6_term = (((var1_t_term >> 2) * (var1_t_term >> 2)) >> 11) * par_p6_d
        var2 = var2_p6_term >> 2
        var2 = var2 + (var1_t_term * int(par_p5_signed) << 1)
        var2 = (var2 >> 2) + int(par_p4_signed << 16)
        var1_temp = ((((var1_t_term >> 2) * (var1_t_term >> 2)) >> 13) * (int(par_p3_d) << 5)) >> 3
        var1_temp = var1_temp + (int(par_p2_signed * var1_t_term) >> 1)
        var1_temp = var1_temp >> 18
        var1_div_factor = (32768 + var1_temp) * int(par_p1) >> 15

        # pressure_raw is the raw value of presssure after calibration

        press_comp = 1048576 - pressure_raw
        press_comp = (press_comp - (var2 >> 12)) * 3125

        if var1_div_factor == 0:
            press_comp = 0 
        elif press_comp >= pres_ovf_check: 

            press_comp = ((press_comp // var1_div_factor) << 1)
        else:

            press_comp = ((press_comp << 1) // var1_div_factor)


        var1 = (int(par_p9_signed) * (((press_comp >> 3) * (press_comp >> 3)) >> 13)) >> 12
        var2 = (press_comp >> 2) *int(par_p8_signed) >> 13
        var3_intermediate = (press_comp >> 8) * (press_comp >> 8) * (press_comp >> 8) * int(par_p10_d_signed)
        var3 = var3_intermediate >> 17
        final_correction_sum = var1 + var2 + var3 +    int (par_p7_d << 7)
        press_comp = press_comp + (final_correction_sum >> 4)

        press_comp/100
        Pressure=press_comp
        # print(Pressure) # press_comp is the final pressure output  obtained after calibration
        return Temperature , Pressure

    # Calculating humidity

    def read_humidity(self):
        global tfine

        BME680_slave_address = 0x76 

        hum_reg=bytearray([0x72]) # register address to read humidity                            #
        hum_cmd=bytearray([0x71]) # command to read humidity from the particular register

        # reading lsb and msb humidity register address

        hum_lsb=bytearray([0x26])
        hum_msb=bytearray([0x25])

        # variables to hold lsb and msb values obtained from particular registers
        data_hum_lsb=bytearray(1)
        data_hum_msb=bytearray(1)

        # write command for humidity

        i2c_obj.write(BME680_slave_address, hum_reg, 1, hum_cmd, 1)
        utime.sleep_ms(100)

        i2c_obj.read(BME680_slave_address, hum_msb, 1, data_hum_msb, 1,0)
        # print(data_hum_msb)
        i2c_obj.read(BME680_slave_address, hum_lsb, 1, data_hum_lsb, 1,0)
        # print(data_hum_lsb)

        # Extracting low and high bytes from bytearray and keeping in integer array to perform bit shifting 

        data_hum_l=data_hum_lsb[0]
        data_hum_m=data_hum_msb[0]

        # performing bit shifting on low and high byte for humidity

        hum_raw=data_hum_m<<8|data_hum_l
        # print(hum_raw)


        # calibrating humidity

        par_h1_lsb=bytearray([0xE2])
        par_h1_msb=bytearray([0xE3])
        data_par_h1_lsb=bytearray(1)
        data_par_h1_msb=bytearray(1)

        i2c_obj.read(BME680_slave_address, par_h1_lsb, 1, data_par_h1_lsb, 1,0)
        i2c_obj.read(BME680_slave_address, par_h1_msb, 1, data_par_h1_msb, 1,0)

        # par_h1 , par_h2 ..... par_h7 are calibration parameters to calculate humidity
        # they are write only registers used to calibrate humidity
         # h1, h2 , h3...h7 are calibration parameters for humidity , they are write only registers for temperature calibration
        #signed= Positive , Negative or Zero
        #Unsigned= Only Positive
        # signed and unsigned nature of these parameters depend how they are further used in caluculation
        # If the parameter is subtracted or multiplied in the formula then its signed
        # If its only added in caibration formula then its unsigned

        data_h1_l=data_par_h1_lsb[0]
        data_h1_h=data_par_h1_msb[0]
        par_h1=data_h1_h<<4|data_h1_l
        # print("data h1",par_h1)
        # if par_h1 & 0x800:
        #     par_h1_signed=par_h1-4095
        # else: 
        #     par_h1_signed=par_h1

        par_h2_lsb=bytearray([0xE2])
        par_h2_msb=bytearray([0xE1])
        data_par_h2_lsb=bytearray(1)
        data_par_h2_msb=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h2_lsb, 1, data_par_h2_lsb, 1,0)
        i2c_obj.read(BME680_slave_address, par_h2_msb, 1, data_par_h2_msb, 1,0)
        par_h2_data_h=data_par_h2_msb[0]
        par_h2_masking_lsb=data_par_h2_lsb[0]
        par_h2_masking=par_h2_masking_lsb & 0xF0
        par_h2_shifted=par_h2_masking>>4


        par_h2 = par_h2_data_h << 4 | par_h2_shifted

        # print("data h2",par_h2)
        # if par_h2 & 0x800:
        #     par_h2_signed=par_h2-4095
        # else:
        #     par_h2_signed=par_h2 

        par_h3=bytearray([0xE4])
        data_par_h3=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h3, 1, data_par_h3, 1,0)
        data_par_h3_final=data_par_h3[0]
        # print("data for h3",data_par_h3_final)
        if data_par_h3_final & 0x80:
            data_par_h3_final_signed=data_par_h3_final-256
        else:
            data_par_h3_final_signed=data_par_h3_final



        par_h4=bytearray([0xE5])
        data_par_h4=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h4, 1, data_par_h4, 1,0)
        data_par_h4_final=data_par_h4[0]
        # print("data for h4",data_par_h4_final)
        if data_par_h4_final & 0x80:
            data_par_h4_final_signed=data_par_h4_final-256
        else:
            data_par_h4_final_signed=data_par_h4_final

        par_h5=bytearray([0xE6])
        data_par_h5=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h5, 1, data_par_h5, 1,0)
        data_par_h5_final=data_par_h5[0]
        # print("data for h5", data_par_h5_final)
        if data_par_h5_final & 0x80:
            data_par_h5_final_signed=data_par_h5_final-256
        else:
            data_par_h5_final_signed=data_par_h5_final

        par_h6=bytearray([0xE7]) 
        data_par_h6=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h6, 1, data_par_h6, 1,0)
        data_par_h6_final=data_par_h6[0]
        # print("data for h6", data_par_h6_final)
        if data_par_h6_final & 0x80:
            data_par_h6_final_signed=data_par_h6_final-256
        else:
            data_par_h6_final_signed=data_par_h6_final


        par_h7=bytearray([0xE8])
        data_par_h7=bytearray(1)
        i2c_obj.read(BME680_slave_address, par_h7, 1, data_par_h7, 1,0)
        data_par_h7_final=data_par_h7[0]
        # print("data for h7",data_par_h7_final)
        if data_par_h7_final & 0x80:
            data_par_h7_final_signed=data_par_h7_final-256
        else:
            data_par_h7_final_signed=data_par_h7_final

        tfine_int = int(tfine)
        temp_scaled = (((tfine_int * 5) + 128) >> 8)
        # print(,tfine_int)

        # calibration for humidity as specified in the datasheet

        var1_h1_term = par_h1 * 16
        var1_h3_term = ((temp_scaled * data_par_h3_final_signed) // 100) >> 1
        var1 = hum_raw - var1_h1_term - var1_h3_term
        var2_h4_part = (temp_scaled * data_par_h4_final_signed) // 100
        var2_h5_term_inner = (temp_scaled * data_par_h5_final_signed) // 100
        var2_h5_part = ((temp_scaled * var2_h5_term_inner) >> 6) // 100

        var2_intermediate_sum = var2_h4_part + var2_h5_part + (1 << 14)
        var2 = (par_h2 * var2_intermediate_sum) >> 10
        var3 = var1 * var2 

        var4 = data_par_h6_final_signed << 7 
        var4_p7_term = (temp_scaled * data_par_h7_final_signed) // 100
        var4 = (var4 + var4_p7_term) >> 4 

        var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
        var6 = (var4 * var5) >> 1

        hum_comp = (((var3 + var6) >> 10) * 1000) >> 12
        # print("hum_comp raw value:", hum_comp)

        if hum_comp > 100000:
            hum_comp = 100000
        elif hum_comp < 0:
            hum_comp = 0

        final_relative_humidity = hum_comp / 1000.0

        # print(" Humidity:", final_relative_humidity, "%")
        return final_relative_humidity


my_sensor=BME()

Temperature,Pressure=my_sensor.read_Temperature_and_Pressure()
Humidity=my_sensor.read_humidity()

# Initialize I2C
while True:
    Temperature,Pressure=my_sensor.read_Temperature_and_Pressure()
    Humidity=my_sensor.read_humidity()
    print("Temperature {:.2f}C".format(Temperature))
    print("Pressure {:.2f}hpa".format(Pressure/100))
    print("Humidity {:.2f}%".format(Humidity))
    utime.sleep(2)   


