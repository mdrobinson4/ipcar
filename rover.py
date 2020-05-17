import cv2
import DataTransfer
import threading
import socket
import re
from sys import exit
import RPi.GPIO as GPIO
import motorControl

exitThread = None

def main():
    # rover and controller ip address
    IP = {'rover': 'localhost', 'controller': 'localhost'}
    # frame and command transfer port numbers
    PORT = {'frame': 1050, 'command': 1051}
    # receive video from webcam
    cap = cv2.VideoCapture(0)
    # start the threads
    createThreads(IP, PORT, cap)

''' create separate processes to stream video, receive commands, etc '''
def createThreads(IP, PORT, cap):
    global exitThread
    exitThread = False
    # send video from rover to cotroller
    frameThread = threading.Thread(target=sendFrames, args=(IP['controller'], PORT['frame'], cap, 'udp',))
    # receive controls from controller
    commandThread = threading.Thread(target=getCommands, args=(IP['controller'], PORT['command'], 'tcp',))
    powerThread = threading.Thread(target=power, args=())
    # begin waiting for input
    powerThread.start()
    # begin streaming video
    frameThread.start()
    # begin receiving commands
    commandThread.start()
    powerThread.join()
    frameThread.join()
    commandThread.join()

''' stream video from the rover to the controller '''
def sendFrames(host, port, cap, protocol):
    global exitThread
    # setup udp socket to send video from webcam, to controller
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # setup video streaming class
    transfer = DataTransfer.DataTransfer(sock, host, port, protocol)
    # send video to the controller
    try:
        while cap != False and cap.isOpened() and exitThread != True:
            ret, frame = cap.read()
            if ret == True:
                # send the frame to the controller
                transfer.sendFrames(frame)
    except KeyboardInterrupt:
        print('keyboard interrupt')
    except BrokenPipeError:
        print('broken pipe')
    except ConnectionAbortedError:
        print('connection aborted')
        
    # stop all threads and clean everything up
    exitThread = True
    sock.close()
    cap.release()
    cv2.destroyAllWindows()

''' receive commands from the controller '''
def getCommands(host, port, protocol):
    global exitThread
    connected = False
    # setup tcp socket to receive commands from
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the controller
    while connected == False and exitThread != True:
        connected = True
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            connected = False
        except KeyboardInterrupt:
            exitThread = True
            return
    if connected:
        sock.close()

''' causes all processes to end if 'q' is inputted into terminal '''
def power():
    global exitThread
    while exitThread != True:
        c = input()
        if c == 'q':
            exitThread = True


if __name__ == '__main__':
    main()
