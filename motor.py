import RPi.GPIO as GPIO
import moisture_readings
from models import Plant
from __init__ import db
from datetime import datetime
from time import sleep
last_watered = datetime.now()
if __name__ == "__main__":
    print("top")
    while True:
        if moisture_readings.moisture()== 1:  
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(3, GPIO.OUT)
            GPIO.setup(5, GPIO.OUT)
            GPIO.setup(7, GPIO.OUT)
            
            pwm=GPIO.PWM(7, 100)
            pwm.start(0)
            pwm.ChangeDutyCycle(90)
            GPIO.output(3, True)
            GPIO.output(5, False)
            pwm.ChangeDutyCycle(90)
            GPIO.output(7, True)
            sleep(5)
            print("here")
            pwm.stop()
            GPIO.cleanup()
# 
#             now = datetime.now()
#             #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#             # add last watered reading here
#             last_watered(True,now)
#             
# def get_last_watered(update=False, value=0):
#     global last_watered
#     if update:
#         last_watered = value
#     else:
#         return last_watered