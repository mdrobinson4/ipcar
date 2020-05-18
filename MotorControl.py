import RPi.GPIO as GPIO
import time
import threading


''' class to control individual motors '''
class Motor:
    def __init__(self, pin, pwmIdle, pwMax):
        self.exitThread = False
        self.pin = pin # signal gpio pin
        self.pwRange = (0, pwMax-pwmIdle) # motor pulse width range (seconds)
        self.inputRange = (0, 10) # minimum input value
        self.pwIdle = pwmIdle
        self.pw = pwmIdle
        # run pulse width modulation in the background
        t1 = threading.Thread(target=self.run, args=())
        t1.start()
    
    def run(self):
        GPIO.setmode(GPIO.BCM) # set the rpi pin mode
        GPIO.setup(self.pin, GPIO.OUT) # set the motor signal pin as output
        # continue running pwm till end of program
        while self.exitThread != True:
            # throttle the signal based on the pulse widths
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.pw)
            GPIO.output(self.pin, GPIO.LOW)
        print('stopping motor')
            
    ''' convert the speed range (0, 10) to the pulse width range (pwMin, pwMax) '''
    def mapRange(self, value):
        num = (value - self.inputRange[0]) * (self.pwRange[1]- self.pwRange[0])
        denom = self.inputRange[1] - self.inputRange[0]
        t = self.pwRange[0] + (num / denom)
        return t
        
    ''' control the motor '''
    def drive(self, value):
        value = float(value)
        if value > 10 or value < -10:
            return False
        self.pw = self.pwIdle + self.mapRange(value)
        return self.pw
    
    ''' set the pulse width to idle '''
    def stop(self):
        self.pw = self.pwIdle
        self.exitThread = True

'''
if __name__ == "__main__":
    motor = Motor(18, 0.0014, 0.002)
    try:
        while True:
            val = input()
            resp = motor.drive(val)
            print(resp)
    except KeyboardInterrupt:
        resp = motor.drive(0)
        print(resp)
        motor.stop()
'''         

