import cv2
import socket
from io import StringIO
import numpy as np


def main():
    host = '192.168.1.228'
    port = 1050

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    
    try:
        sendFrames(sock, conn, addr)
    except:
        raise
        sock.close()

def sendFrames(sock, conn, addr):
    cap = getSource()
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        send(conn, frame)
        #cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    sock.close()

def send(conn, image):
    f = StringIO()
    np.savez_compressed(f, frame=image)
    f.seek(0)
    out = f.read()
    val = "{0}:".format(len(f.getvalue()))
    out = val + out
    conn.send(out)



def getSource():
    try:
        source = cv2.VideoCapture(0)
        return source
    except "VIDEOIO ERROR":
        return False



if __name__ == '__main__':
    main()
