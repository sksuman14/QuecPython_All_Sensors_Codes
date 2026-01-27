# tilt_sensor.py  
from machine import I2C
import utime
import math

class TiltSensor:
    def __init__(self):
        self.i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        self.MPU_ADDR = 0x68

        self.TILT_THRESHOLD = 24
        self.REQUIRED_COUNTS = 20
        self.bad_tilt_count = 0
        self.alarm_active = False

    def toSigned(self, val):
        if val > 32767:
            val -= 65536
        return val

    def start(self):
        # Wake up MPU6050
        self.i2c.write(self.MPU_ADDR, bytearray([0x6B]), 1, bytearray([0x00]), 1)
        utime.sleep_ms(100)

        # Check connection
        whoami = bytearray(1)
        self.i2c.read(self.MPU_ADDR, bytearray([0x75]), 1, whoami, 1, 0)
        if whoami[0] != 0x68:
            print("ERROR: MPU6050 not found! Check wiring!")
            return

        print("MPU6050 connected! Tilt alarm ready!\n")

        while True:
            data = bytearray(6)
            try:
                self.i2c.read(self.MPU_ADDR, bytearray([0x3B]), 1, data, 6, 0)
            except:
                print("I2C read failed!", end="\r")
                utime.sleep(1)
                continue
            # Convert raw accelerometer data to g-forces values
            ax = self.toSigned((data[0] << 8) | data[1]) / 16384.0
            ay = self.toSigned((data[2] << 8) | data[3]) / 16384.0
            az = self.toSigned((data[4] << 8) | data[5]) / 16384.0
            
            # Calculate total acceleration magnitude
            total_g = math.sqrt(ax*ax + ay*ay + az*az)
            # Calculate tilt angle from vertical (Z-axis)
            tilt_angle = 0 if total_g < 0.01 else math.acos(az / total_g) * 180 / math.pi
            
            # Check if tilt exceeds threshold
            if tilt_angle >= self.TILT_THRESHOLD:
                self.bad_tilt_count += 1
                # Trigger alarm if tilt persists long enough
                if self.bad_tilt_count >= self.REQUIRED_COUNTS and not self.alarm_active:
                    self.alarm_active = True
                    print("\n\nALERT!!! TILT > 24° FOR 20+ SECONDS!!!\n")
            else:
                self.bad_tilt_count = 0
                if self.alarm_active:
                    self.alarm_active = False
                    print("\nTilt back to normal. Alarm cleared.\n")

            status = "DANGER" if self.alarm_active else "Normal "
            print("Tilt: {:3.0f}° | Count: {:2d}/20 | Status: {}    ".format(
                  tilt_angle, self.bad_tilt_count, status), end="\r")

            utime.sleep(1)


# Run the tilt sensor #
if __name__ == "__main__":
    sensor = TiltSensor() # Create TiltSensor object
    sensor.start()         # Start tilt monitoring



