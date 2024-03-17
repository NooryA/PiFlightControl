import time
import board
import adafruit_bmp3xx
import busio
import adafruit_mpu6050
import datetime

i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
mpu = adafruit_mpu6050.MPU6050(i2c)
telemetry_file = "telemetry_data.csv"

        
        
def log_data(timestamp,temperature,pressure,x_acc,y_acc,z_acc,x_gyro,y_gyro,z_gyro):
        with open(telemetry_file, "a") as file:
                file.write(f"{timestamp},{temperature},{pressure},{x_acc},{y_acc},{z_acc},{x_gyro},{y_gyro},{z_gyro}\n")        
                
with open(telemetry_file, "w") as file:
        file.write("Timestamp,Temperature,Pressure,X_Acceleration, Y_Acceleration, Z_Acceleration, X_Gryo, Y_Gryo, Z_Gryo\n")

def main():
        while True:
                temperature_celcius = bmp.temperature
                pressure = bmp.pressure
                print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
                print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
                print(f'Temperature {temperature_celcius:.2f}°C')
                print(f'Pressure {pressure:.2f} hPa')
                print(mpu.acceleration)
                x_acc = "{:.2f}".format(mpu.acceleration[0])
                y_acc ="{:.2f}".format(mpu.acceleration[1])
                z_acc = "{:.2f}".format(mpu.acceleration[2])
                x_gyro = "{:.2f}".format(mpu.gyro[0])
                y_gyro = "{:.2f}".format(mpu.gyro[1])
                z_gyro = "{:.2f}".format(mpu.gyro[2])
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                temperature_formatted = "{:.2f}".format(temperature_celcius)
                pressure_formatted = "{:.2f}".format(pressure)
                log_data(current_time,temperature_formatted,pressure_formatted,x_acc,y_acc,z_acc,x_gyro,y_gyro,z_gyro)
                
                time.sleep(2)

if __name__ == "__main__":
        main()
