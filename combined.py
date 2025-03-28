import pigpio
import time
import datetime
import board
import busio
import adafruit_bmp3xx
from adafruit_servokit import ServoKit
import mpu6050
import threading

GPIO_PIN = 12 #PPM
NUM_CHANNELS = 8
NUM_SERVOS = 16
FRAME_START_THRESHOLD = 6000
AILERON_CHANNEL = 1
ELEVATOR_CHANNEL = 2
THROTTLE_CHANNEL = 3
RUDDER_CHANNEL = 4
RUDDER_2_CHANNEL = 6
ESC_GPIO = 18
MAX_ANGLE_HORIZONTAL_TAIL = 43.59

#sensors
i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
mpu_sensor = mpu6050.mpu6050(0x68)

#servos
kit = ServoKit(channels = NUM_SERVOS)
pi = pigpio.pi()

if not pi.connected:
	exit()
	
	
pi.set_mode(ESC_GPIO,pigpio.OUTPUT)
pi.set_PWM_frequency(ESC_GPIO,50)


telemetry_file = "telemetry_data.csv"
with open(telemetry_file, "a") as file:
	file.write("Timestamp,Temperature,Pressure,X_acc,Y_acc,Z_acc,X_gyro,Y_gyro,Z_gyro\n")   

def log_data():
	while True:
		temperature = bmp.temperature
		pressure = bmp.pressure
		accel_data = mpu_sensor.get_accel_data()
		gyro_data = mpu_sensor.get_gyro_data()
		current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open(telemetry_file,"a") as file:
			file.write(f"{current_time},{temperature:.2f},{pressure:.2f},{accel_data['x']:.2f},{accel_data['y']:.2f},{accel_data['z']:.2f}, {gyro_data['x']:.2f},{gyro_data['y']:.2f},{gyro_data['z']:.2f}\n")
		time.sleep(2)	

def handle_ppm():
	start_tick = None
	durations = []
	frame_start_detected = False

	def set_esc_throttle(pulse_width):
		safe_pulse_width = max(1000, min(2000, pulse_width))
		pi.set_servo_pulsewidth(ESC_GPIO,safe_pulse_width)

	def cbf(gpio, level, tick):
		nonlocal start_tick, durations,frame_start_detected
		if start_tick is not None:
			duration = pigpio.tickDiff(start_tick, tick)
			
			if duration > FRAME_START_THRESHOLD:
				frame_start_detected = True
				durations = []
			elif frame_start_detected:
				durations.append(duration)
				if len(durations) == NUM_CHANNELS:
					#aileron_angle = duration_to_angle(durations[AILERON_CHANNEL - 1],136.41,170,151.23)
					#elevator_angle = duration_to_angle(durations[ELEVATOR_CHANNEL - 1],123,57,90)
					#rudder_angle = duration_to_angle(durations[RUDDER_CHANNEL - 1],49.18,0,23.29)
					#rudder_two_angle = duration_to_angle(durations[RUDDER_2_CHANNEL - 1],49.18,0,25.89)
					
					
					#throttle_pulse = durations[THROTTLE_CHANNEL - 1]
					
				
					#kit.servo[0].angle = aileron_angle
					#kit.servo[2].angle = elevator_angle
					#kit.servo[4].angle = rudder_angle
					#kit.servo[6].angle = rudder_two_angle
					kit.servo[0].angle = 0
					#set_esc_throttle(throttle_pulse)
					#print(f"Servo 1 set to {aileron_angle} degrees")
					#print(f"Servo 2 set to {elevator_angle} degrees")
					#print(f"Servo 3 set to {rudder_angle} degrees")
					#print(f"Servo 4 set to {rudder_two_angle} degrees")
					#print(f"Throttle set to {throttle_pulse} speed")
					 
		start_tick = tick


	def duration_to_angle(duration,MAX,MIN,REST):
		normalized_input = ((duration - 1000) / 1000.0)
		
		if normalized_input <0.5:
			
			angle = REST - (0.5 - normalized_input) * 2 * (REST-MIN)
		else:
			angle = REST +(normalized_input - 0.5) * 2 * (MAX - REST)
			
		angle = max(MIN,min(MAX,angle))
		return angle
		
		
	cb = pi.callback(GPIO_PIN, pigpio.RISING_EDGE, cbf)
	while True:
		time.sleep(1)

telemetry_thread = threading.Thread(target=log_data)
ppm_thread = threading.Thread(target=handle_ppm)

telemetry_thread.start()
ppm_thread.start()

telemetry_thread.join()
ppm_thread.join()
