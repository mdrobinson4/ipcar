#!/usr/bin/env python
import inputs


class XboxController(object):
    def __init__(self):
        # x and y joystic values -10->10
        self.joystick = [0, 0]
        # range of joystick values (x-axis)
        self.xRange = (-32768, 32767)
        # range of joystick values (y-axis)
        self.yRange = (32767, -32768)
        
    ''' check the status of the controller '''
    def readController(self):
        # get the events for the first gamepad (xbox one controller) 
        events = inputs.get_gamepad()
        # access the joystick events
        for event in events:
            # joystick y-axis
            if event.code == 'ABS_Y':
                # adjust the range of values to -10 to 10
                self.joystick[1] = self.mapRange(event.state, 'y')
            # joystick x-axis
            elif event.code == 'ABS_X':
                # adjust the range of values to -10 to 10
                self.joystick[0] = self.mapRange(event.state, 'x')
        # mix the controls for the x and y-axis
        return self.mixControls()
    
    ''' change the range of values to -10 to 10 '''
    def mapRange(self, input, axis):
        mapFrom = None
        # desired range
        mapTo = (-10, 10)
        # compensate for slightly differnt x and y-axis ranges
        if axis == 'x':
            mapFrom = self.xRange
        elif axis == 'y':
            mapFrom = self.yRange
        # math stuff
        num = (input - mapFrom[0]) * (mapTo[1]- mapTo[0])
        denom = mapFrom[1] - mapFrom[0]
        t = mapTo[0] + (num / denom)
        return t
    
    ''' combine the x and y-axis controls into the corresponding
        left and right motor values '''
    def mixControls(self):
        k = 1 # scale
        left = None
        right = None
        # check to see if the resulting speed is too great
        if abs(self.joystick[1] + self.joystick[0]) > 10:
            # adjust scale
            k = 10 / abs(self.joystick[1] + self.joystick[0])
        # check to see if the resulting speed is too great
        elif abs(self.joystick[1] - self.joystick[0]) > 10:
            # adjust the scale
            k = 10 / abs(self.joystick[1] - self.joystick[0])
        # use calculated scale to set the left and right motor values
        left = k * (self.joystick[1] + self.joystick[0])
        right = k * (self.joystick[1] - self.joystick[0])
        return (left, right)