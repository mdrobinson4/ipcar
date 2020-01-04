import cv2
import DataTransfer
import threading
import socket
import re

def main():
    GPIO.setmode(GPIO.BCM)
    host = 'localhost'
    port = 1050
    cap = cv2.VideoCapture(0)
    createThreads(host, port, cap)
    print('exit')

def createThreads(host, port, cap):
    frameThread = threading.Thread(target=sendFrames, args=(host, port, cap,))
    commandThread = threading.Thread(target=getCommands, args=(host, port + 1,))
    frameThread.start()
    commandThread.start()
    frameThread.join()
    commandThread.join()

def sendFrames(host, port, cap):
    socket, conn, addr = setupServer(host, port)
    transfer = DataTransfer.DataTransfer(socket, conn, addr)
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        if ret != True:
            break
        try:
            transfer.sendFrames(frame)
        except BrokenPipeError:
            break
        except ConnectionAbortedError:
            break
    socket.close()
    cap.release()
    cv2.destroyAllWindows()

def getCommands(host, port):
    socket, conn, addr = setupServer(host, port)
    data = ''
    prevComm = []
    while True:
        data = conn.recv(15)
        data = data.decode()
        if 'close' in data:
            break
        comm = re.findall("(?<=\:)(.*?)(?=\:)", data)
        if len(comm) > 0 and comm != prevComm:
            print('{}'.format(comm))
        prevComm = comm
    socket.close()

def setupServer(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    return sock, conn, addr

def setupMotor(input1, input2):
    GPIO.setup(input1, GPIO.OUT)
    GPIO.setup(input2, GPIO.OUT)
    pwm1 = GPIO.PWM(input1, 1000)
    pwm1.start



if __name__ == '__main__':
    main()
