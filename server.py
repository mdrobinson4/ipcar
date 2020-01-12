import cv2
import DataTransfer
import threading
import socket
import re
from sys import exit
try:
    from adafruit_motorkit import MotorKit
except:
    pass
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

def main():
    host = 'localhost'
    port = 1050
    cap = cv2.VideoCapture(0)
    createThreads(host, port, cap)
    print('exit')

def createThreads(host, port, cap):
    frameThread = threading.Thread(target=sendFrames, args=(host, port, cap, 'udp',))
    commandThread = threading.Thread(target=getCommands, args=(host, port + 1, 'tcp',))
    frameThread.start()
    commandThread.start()
    frameThread.join()
    commandThread.join()

def sendFrames(host, port, cap, protocol):
    socket, conn, addr = setupServer(host, port, protocol)
    transfer = DataTransfer.DataTransfer(socket, conn, addr, port, 'udp')
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        if ret != True:
            break
        try:
            cv2.imshow('server [sender]', frame)
            transfer.sendFrames(frame)
        except BrokenPipeError:
            print('broken pipe')
            break
        except ConnectionAbortedError:
            break
        except KeyboardInterrupt:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    socket.close()
    cap.release()
    cv2.destroyAllWindows()

def getCommands(host, port, protocol):
    socket, conn, addr = setupServer(host, port, protocol)
    data = ''
    prevComm = []
    kit = None
    steer = None
    lastSpeed = 0
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)
        steer = GPIO.PWM(2, 50)
        steer.start(7.5)
        kit = MotorKit()
    except NameError:
        pass
    while True:
        data = conn.recv(15)
        data = data.decode()
        if 'close' in data:
            break
        comm = re.findall("(?<=\:)(.*?)(?=\:)", data)
        if len(comm) > 0 and comm != prevComm:
            lastSpeed = performCommand(kit, steer, lastSpeed comm)
        prevComm = comm
    socket.close()

def performCommand(kit, steer, lastSpeed, comm):
    speed = None
    direction = None
    steerPos = 7.5
    print('{}'.format(comm))
    if kit == None or steer == None or comm == None:
        return
    for command in comm:
        if command.isdigit():
            speed = int(command)
        if command == 'Up':
            direction = 1
        elif command == 'Down':
            direction = -1
        elif command == 'Left':
            steerPos = 0
        elif command == 'Right':
            steerPos = 12.5
    steer.steerPos(steerPos)
    if direction:
        if speed == None:
            speed = lastSpeed
        kit.motor1.throttle(direction * (speed / 10.0))
    return speed


def setupServer(host, port, protocol):
    sock = None
    conn = None
    addr = None
    if protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()
    # setup server to send video frames
    elif protocol == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind((host, port))
    return sock, conn, addr



if __name__ == '__main__':
    main()
