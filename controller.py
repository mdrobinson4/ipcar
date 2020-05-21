import cv2
import inputs
import importlib
import pickle
import DataTransfer
import XboxController
import threading
import socket
from sys import exit

exitThread = None

def main():
    # rover and controller ip address
    IP = {'rover': 'localhost', 'controller': 'localhost'}
    # frame and command transfer port numbers
    PORT = {'frame': 1050, 'command': 1051}
    createThreads(IP, PORT)

def createThreads(IP, PORT):
    global exitThread
    exitThread = False
    # start receiving video from the rover
    frameThread = threading.Thread(target=getFrames, args=(IP['controller'], PORT['frame'], 'udp',))
    # start sending commands to the rover
    commandThread = threading.Thread(target=sendCommands, args=(IP, PORT, 'tcp',))
    powerThread = threading.Thread(target=power, args=())
    # start threads
    powerThread.start()
    frameThread.start()
    commandThread.start()
    # stop threads
    powerThread.join()
    frameThread.join()
    commandThread.join()

''' gets video frames from the rover '''
def getFrames(host, port, protocol):
    global exitThread
    # setup udp socket to receive video from rover
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.bind((host, port))
    # create transfer class to receive video
    transfer = DataTransfer.DataTransfer(sock, None, None, 'udp')
    while exitThread != True:
        # receive video frame from rover
        frame = transfer.receiveFrames()
        try:
            # show the rover video stream
            cv2.imshow('client [receiver]', frame)
            cv2.waitKey(1)
        except cv2.error:
            pass
        except KeyboardInterrupt:
            # force close
            exitThread = True

''' attempt to connect command stream with rover '''
def connectTCP(sock):
    global exitThread
    conn = None
    addr = None
    connected = False
    # try to connect until thread exits
    while exitThread != True and connected == False:
        connected = True
        try:
            conn, addr = sock.accept() # wait for connection request
        # try for 1 second, then restart
        # allows us to exit process if needed
        except socket.timeout:
            connected = False
    return (conn, addr)

''' send commands from controller to rover '''
def sendCommands(IP, PORT, protocol):
    global exitThread
    # setup tcp socket to send commands to control rover
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # xbox controller
    xbox = XboxController.XboxController()
    # read inputs from xbox one controller
    while exitThread != True:
        try:
            # get input from the xbox controller
            (l,r) = xbox.readController()
            # command to send to rover
            command = [l,r]
            # serialize data
            dataToSend = pickle.dumps(command)
        except (inputs.UnpluggedError, OSError):
            # reload inputs
            importlib.reload(inputs)
            # controller disconnected, stop the motors
            dataToSend = pickle.dumps([1500,1500])
        try:
            sock.sendto(dataToSend, (IP['rover'], PORT['command']))
        except (ConnectionResetError, OSError):
            print('lost connection to rover, reconnecting...')
            # listen for potential connections

''' causes all processes to end if 'q' is inputted into terminal '''
def power():
    global exitThread
    while exitThread != True:
        c = input() # get input from user
        # exit all threads
        if c == 'q':
            exitThread = True

if __name__ == '__main__':
    main()
