import cv2
import DataTransfer
import threading
import socket

def main():
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
    while True:
        data = conn.recv(10)
        data = data.decode()
        data = data.replace('0', '')
        if 'close' in data:
            break
        comm1, _, comm2 = data.partition(':')
        if len(data) > 0:
            print('{} - {}'.format(comm1, comm2))
    socket.close()

def setupServer(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    return sock, conn, addr


if __name__ == '__main__':
    main()
