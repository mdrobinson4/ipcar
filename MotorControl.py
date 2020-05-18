import RPi.GPIO as GPIO
import time
import threading
import pigpio


''' class to control individual motors '''
class Motor:
    def __init__(self, pin):
        self.exitThread = False
        self.pin = pin # signal gpio pin
        self.motor = pigpio.pi()
        self.motor.set_servo_pulsewidth(pin, 1500)
        
    ''' control the motor '''
    def drive(self, pulseWidth):
        pulseWidth = float(pulseWidth)
        if pulseWidth > 2000 or pulseWidth < 1000:
            return False
        self.motor.set_servo_pulsewidth(self.pin, pulseWidth) 
        return True
    
    ''' set the pulse width to idle '''
    def stop(self):
        self.motor.set_servo_pulsewidth(self.pin, 1500)
        self.exitThread = True