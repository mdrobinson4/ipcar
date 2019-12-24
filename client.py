import cv2
import socket
from io import StringIO
import numpy as np

def main():
    host = '192.168.1.228'
    port = 1050
    header = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('connected')
    getFrames(sock)
    
def getFrames(sock):
    while True:
        receive(sock)

def receive(sock):
    length = None
    ultimate_buffer = ""
    while True:
        data = sock.recv(1024)
        ultimate_buffer += data
        if len(ultimate_buffer) == length:
            break
        while True:
            if length is None:
                if ':' not in ultimate_buffer:
                    break
                length_str, ignored, ultimate_buffer = ultimate_buffer.partition(':')
                length = int(length_str)
            if len(ultimate_buffer) < length:
                break
            ultimate_buffer = ultimate_buffer[length:]
            length = None
            break
        final_image = np.load(StringIO(ultimate_buffer))['frame']
        print('received image')
        return


if __name__ == '__main__':
    main()
