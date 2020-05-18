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
                self.joystick[1] = self.mapRange(event.state,'y',(-100,100))
            # joystick x-axis
            elif event.code == 'ABS_X':
                # print(event.state)
                # adjust the range of values to -10 to 10
                self.joystick[0] = self.mapRange(event.state, 'x',(-100,100))
        # print((self.joystick[0], self.joystick[1]))
        # mix the controls for the x and y-axis
        return self.mixControls()
    
    ''' change the range of values to -10 to 10 '''
    def mapRange(self, input, axis, mapTo):
        mapFrom = None
        # desired range
        # compensate for slightly differnt x and y-axis ranges
        mapFrom = (-100, 100)
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
        x = self.joystick[0]
        y = self.joystick[1]
        v = (100-abs(x))*(y/100)+y
        w = (100-abs(y))*(x/100)+x
        right = self.mapRange((v-w)/2,None,(1000,2000))
        left = self.mapRange((v+w)/2,None,(1000,2000))
        #print((left, right))
        return (left, right)

'''
if __name__ == '__main__':
    xbox = XboxController()
    while True:
        xbox.readController()
'''
