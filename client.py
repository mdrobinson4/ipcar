import cv2
import DataTransfer
import Commands
import threading
import socket
from sys import exit

exitThread = None

def main():
    host = 'localhost'
    port = 1050
    createThreads(host, port)

def createThreads(host, port):
    global exitThread
    exitThread = False
    frameThread = threading.Thread(target=getFrames, args=(host, port, 'udp',))
    frameThread.start()
    sendCommands(host, port+1, 'tcp')
    frameThread.join()

def getFrames(host, port, protocol):
    global exitThread
    try:
        socket = setupClient(host, port, protocol)
    except KeyboardInterrupt:
        return
    transfer = DataTransfer.DataTransfer(socket, None, None, port, 'udp')
    while exitThread != True:
        frame = transfer.receiveFrames()
        cv2.imshow('client [receiver]', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def sendCommands(host, port, protocol):
    global exitThread
    socket = setupClient(host, port, protocol)
    command = Commands.Commands(socket)
    exitThread = True

def setupClient(host, port, protocol):
    sock = None
    if protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    # setup client to receive video frames
    elif protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
    return sock

if __name__ == '__main__':
    main()
