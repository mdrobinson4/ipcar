import cv2
import DataTransfer
import Commands
import threading
import socket

exitThread = None

def main():
    host = 'localhost'
    port = 1050
    createThreads(host, port)

def createThreads(host, port):
    global exitThread
    exitThread = False
    frameThread = threading.Thread(target=getFrames, args=(host, port,))
    frameThread.start()
    sendCommands(host, port+1)
    frameThread.join()
    print('exit')

def getFrames(host, port):
    global exitThread
    socket = setupClient(host, port)
    transfer = DataTransfer.DataTransfer(socket, None, None)
    while exitThread != True:
        frame = transfer.receiveFrames()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def sendCommands(host, port):
    global exitThread
    socket = setupClient(host, port)
    command = Commands.Commands(socket)
    exitThread = True

def setupClient(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


if __name__ == '__main__':
    main()
