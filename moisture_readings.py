# External module imp 
# When working on mac/windows, use this import:
import FakeRPi.GPIO as GPIO
# On Pi, use this import:
#import RPi.GPIO as GPIO
import signal
import sys
import time
import spidev
from datetime import datetime
from flask_login import login_required, current_user
from models import Plant
from __init__ import db

# Pin 15 on Raspberry Pi corresponds to GPIO 22
LED1 = 15
# Pin 16 on Raspberry Pi corresponds to GPIO 23
LED2 = 16

spi_ch = 0

#Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# set up GPIO output channel
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

def close(signal, frame):
    GPIO.output(LED1, 0)
    GPIO.output(LED2, 0)
    sys.exit(0)

signal.signal(signal.SIGINT, close)

def valmap(value, istart, istop, ostart, ostop):
    value = ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
    if value > ostop:
       value = ostop
    return value

def get_adc(channel):

    # Make sure ADC channel is 0 or 1
    if channel != 0:
        channel = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + channel) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    # considering the soil moisture sensor is working at 5V
    voltage = (5 * adc) / 1024

    return voltage

def moisture():
    # Report the channel 0 and channel 1 voltages to the terminal
    GPIO.setmode(GPIO.BOARD)
    try:
        while True:
            adc_0 = get_adc(0)
            adc_1 = get_adc(1)
            sensor1 = round(adc_0, 2)
            
            if sensor1 < 0.5:
                moisture1 = 0
            else:
                moisture1 = round(valmap(sensor1, 5, 3.5, 0, 100), 0)
            sensor2 = round(adc_1, 2)
           
            if sensor2 < 0.5:
              moisture2 = 0
            else:
                moisture2 = round(valmap(sensor2, 0, 3.5, 0, 100), 0)
               
                moisture2=100-moisture2
            print("Soil Moisture Sensor:", moisture2, "%")
            if moisture2 < 40:
                print("Low")
                return 1
            elif moisture2 > 60:
                print("High")
                return 2
            else:
                print("Good")
                return 3
            #if moisture1 < 40 or moisture2 < 40:
             #   GPIO.output(LED1, 1)
              #  GPIO.output(LED2, 0)
            #else:
             #   GPIO.output(LED1, 0)
              #  GPIO.output(LED2, 1)
            time.sleep(0.5)
    finally:
        GPIO.cleanup()

print("working!")

#if __name__=="__main__":
 #   moisture()
def moisture_levels():
    print("moisture_levels called")
    # return moisture readings to display on web server
    plant = Plant.query.filter_by(user_id=current_user.id).first()
    print(plant)
    # add moisture level reading here
    moisture_level = "Low"
    plant.moisture_level = moisture_level
    db.session.add(plant)
    db.session.commit()

def last_watered():
    # return the last watered date and time
    plant = Plant.query.filter_by(user_id=current_user.id).first()
    print(plant)
    now = datetime.now()
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # add last watered reading here
    last_watered = now
    print(last_watered)
    plant.last_watered = last_watered
    db.session.add(plant)
    db.session.commit()