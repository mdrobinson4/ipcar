import RPi.GPIO as GPIO
from time import sleep

in1 = 2
in2 = 3
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

m1 = GPIO.PWM(in1, 1000)
m2 = GPIO.PWM(in2, 1000)

m1.start(25)
m2.start(25)

sleep(2)
m1.ChangeDutyCycle(50)
