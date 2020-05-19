# Socket Car V1
Allows user to control rover through sockets

## Overview:
### controller (xbox one controller connected to laptop):
- sends commands [tcp] to the car and receives video stream [udp] from the car
- currently using an xbox one controller connected to my laptop to operate rover

### rover (raspberry pi driving motors)
- mixed motor controls are received from the controller
- streams video to the controller
- sends video frames from a webcam mounted on the car to the server
