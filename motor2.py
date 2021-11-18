import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1 = 16
Motor2 = 18
Motor3 = 22

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)

print("FORWARD MOTION")

GPIO.setup(Motor1, GPIO.HIGH)
GPIO.setup(Motor2, GPIO.LOW)
GPIO.setup(Motor3, GPIO.HIGH)

sleep(3)

print("BACKWARD MOTION")

GPIO.setup(Motor1, GPIO.LOW)
GPIO.setup(Motor2, GPIO.HIGH)
GPIO.setup(Motor3, GPIO.HIGH)

sleep(3)

print("STOP")
GPIO.output(Motor3,GPIO.LOW)

GPIO.cleanup()
