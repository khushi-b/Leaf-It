import RPi.GPIO as GPIO
import moisture_readings
from time import sleep
if __name__ =="__main__":
    while True:
        if moisture_readings.moisture()==1:  
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(3, GPIO.OUT)
            GPIO.setup(5, GPIO.OUT)
            GPIO.setup(7, GPIO.OUT)
            
            pwm=GPIO.PWM(7, 100)
            pwm.start(0)
            pwm.ChangeDutyCycle(10)
            GPIO.output(3, True)
            GPIO.output(5, False)
            pwm.ChangeDutyCycle(10)
            GPIO.output(7, True)
            sleep(5)
            print("here")
            pwm.stop()
            GPIO.cleanup()
