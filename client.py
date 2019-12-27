import cv2
import socket
from io import BytesIO
import numpy as np

def main():
    host = '192.168.1.228'
    port = 1050
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    try:    
        getFrames(sock)
    except ValueError:
        return

def getFrames(sock):
    while True:
        dataLen = None
        buffer = b''
        data = sock.recv(1024)
        if dataLen == None:
            dataLen, ignored, buffer = data.partition(b':')
            dataLen = int(dataLen)
        while len(buffer) < dataLen:
            dataRem = dataLen - len(buffer)
            if dataRem < 1024:
                bytes = dataRem
            else:
                bytes = 1024
            buffer += sock.recv(bytes)
        image = np.load(BytesIO(buffer))['frame']
        #print(image)
        #print('{} >= {}'.format(dataLen, len(buffer)))
        height, width = image.shape[:2]
        resized = cv2.resize(image, (int(width*5), int(height*5)))
        cv2.imshow("image", resized)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        

if __name__ == '__main__':
    main()
