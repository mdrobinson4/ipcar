import cv2
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
    commandThread = threading.Thread(target=sendCommands, args=(IP['controller'], PORT['command'], 'tcp',))
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
    sock.bind((host, port))
    # create transfer class to receive video
    transfer = DataTransfer.DataTransfer(sock, None, None, 'udp')
    try:
        while exitThread != True:
            # receive video frame from rover
            frame = transfer.receiveFrames()
            # show the received video frame
            cv2.imshow('client [receiver]', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        exitThread = True

''' send commands from controller to rover '''
def sendCommands(host, port, protocol):
    global exitThread
    conn = None
    addr = None
    # setup tcp socket to send commands to control rover
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to controller
    sock.bind((host, port))
    # listen for potential connections
    sock.listen()
    # wait for the rover to connect
    conn, addr = sock.accept()
    # xbox controller
    xbox = XboxController.XboxController()
    # read inputs from xbox one controller
    while exitThread != True:
        # get input from the xbox controller
        (l, r) = xbox.readController()
        # command to send to rover
        command = [l, r]
        # serialize data
        dataToSend = pickle.dumps(command)
        # send data to rover
        conn.send(dataToSend)
    # close the socket
    conn.close()

''' causes all processes to end if 'q' is inputted into terminal '''
def power():
    global exitThread
    while exitThread != True:
        c = input()
        if c == 'q':
            exitThread = True

if __name__ == '__main__':
    main()
