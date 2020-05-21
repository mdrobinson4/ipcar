import cv2
import pickle
import DataTransfer
import MotorControl
import threading
import socket
import re
from sys import exit
import time
import warnings
import RPi.GPIO as GPIO

exitThread = None

def main():
    # rover and controller ip address
    IP = {'rover': '192.168.2.8', 'controller': '192.168.2.5'}
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
    # listen for inputs from user to quit
    powerThread = threading.Thread(target=power, args=())
    # begin processes
    powerThread.start()
    frameThread.start()
    commandThread.start()
    # wait till all processes to end before continuing
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
    while exitThread != True:
        ret, frame = cap.read()
        if ret == True:
            try:
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

''' attempt to create tcp connection '''
def connectTCP(sock, host, port):
    global exitThread
    connected = False
    # connect to the controller
    while connected == False and exitThread != True:
        connected = True
        try:
            sock.connect((host, port))
        except (OSError, ConnectionRefusedError):
            connected = False
        except KeyboardInterrupt:
            exitThread = True
            return
    return sock

''' receive commands from the controller and send to motors '''
def getCommands(host, port, protocol):
    global exitThread
    motorCommand = None
    motor = [None, None]
    # setup motors
    motor[0] = MotorControl.Motor(17)
    motor[1] = MotorControl.Motor(18)
    # setup tcp socket to receive commands from
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the controller
    sock = connectTCP(sock, host, port)
        
    while exitThread != True:
        # receive command from controller
        data = sock.recv(34)
        try:
            # decode data sent from controller
            motorCommand = pickle.loads(data)
            # send command to the left motor
            m0 = motor[0].drive(motorCommand[0])
            # send command to the right motor
            m1 = motor[1].drive(motorCommand[1])
        except (EOFError,pickle.UnpicklingError):
            print('lost controller connection')
            # set motors to idle
            motor[0].stop()
            motor[1].stop()
            # attempt to reconnect to controller
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = connectTCP(sock, host, port)
            pass
    # stop both motors
    motor[0].stop()
    motor[1].stop()
    
    if sock:
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
