import time
import RPi.GPIO as GPIO


PWM_PIN = 15
PWM_MIN = 1000
PWM_MAX = 2000
RF_MIN = -100
RF_MAX = 100

def map_value (x, in_min, in_max, out_min, out_max):
	return (x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def read_pwm():
	pulse_start = 0;
	pulse_end = 0
	
	GPIO.wait_for_edge(PWM_PIN,GPIO.RISING)
	
	pulse_start = time.time()
	
	GPIO.wait_for_edge(PWM_PIN,GPIO.FALLING)
	
	pulse_end = time.time()
	
	pulse_duration = (pulse_end - pulse_start)* 1e6
	
	return pulse_duration
	
def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PWM_PIN, GPIO.IN)
	
	try:
		while True:
			pulse_width = read_pwm()
			RF_position = map_value(pulse_width,PWM_MIN,PWM_MAX,RF_MIN,RF_MAX)
			print("RF CONTROL",RF_position)
			time.sleep(0.1)
			
	except KeyboardInterrupt:
		print("Existing..")
		GPIO.cleanup()
		
if __name__ == "__main__":
        main()

