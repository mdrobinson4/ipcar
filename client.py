import cv2
import socket
from io import BytesIO
import numpy as np

def main():
    host = '192.168.1.228'
    port = 1050
    header = 10
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    getFrames(sock)

def getFrames(sock):
    while True:
        receive(sock)

def receive(sock):
    while True:
        length = None
        buffer = b''
        while True:
            data = sock.recv(1024)
            if length == None:
                dataLen, ignored, buffer = ultimate_buffer.partition(b':')
                length = int(dataLen)
            else:
                buffer += data
            print('total: {}, buffer: {}'.format(dataLen, len(buffer)))
            if len(buffer) >= dataLen:
                break
        print(buffer)
        final_image = np.load(BytesIO(buffer))['frame']
        print('received image')
        cv2.imshow("image")
        return


if __name__ == '__main__':
    main()
