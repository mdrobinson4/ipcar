import cv2
import DataTransfer


def main():
    host = 'localhost'
    port = 1050
    state = 'server'

    cap = cv2.VideoCapture(0)
    sendFrames(host, port, cap)
    sendCommands(host, port)

def sendFrames(server, cap):
    socket, conn, addr = setupServer((host, port))
    transer = DataTransfer.DataTransfer(socket, conn, addr)
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            transfer.sendFrames(frame)
        else:
            break

def sendCommands(host, port):
    socket, conn, addr = setupServer((host, port+1))
    while True:
        data = sock.recv(10)
        data = data.decode()
        data = data.replace('0', '')
        comm1, _, comm2 = data.partition(':')

def setupServer(locaion):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(location)
    socket.listen()
    conn, addr = socket.accept()
    return socket, conn, addr


if __name__ == '__main__':
    main()
