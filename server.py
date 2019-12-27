import cv2
import socket
from io import BytesIO
import numpy as np


def main():
    host = '192.168.1.228'
    port = 1050
    sock, conn, addr = getConnections(host, port)
    try:
        sendFrames(sock, conn)
    except:
        sock.close()

def getConnections(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()
    return sock, conn, addr

def sendFrames(sock, conn):
    cap = getSource()
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        bwFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = bwFrame.shape[:2]
        resized = cv2.resize(bwFrame, (int(0.2*width), int(0.2*height)))
        
        if ret is True:
            send(conn, resized)
        else:
            break
        #cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    sock.close()

def send(conn, image):
    if not isinstance(image, np.ndarray):
        print('not a valid image')
        return
    
    f = BytesIO()
    np.savez_compressed(f, frame=image)
    f.seek(0)
    output = f.read()
    dataLen = "{0}:".format(len(f.getvalue()))
    output = dataLen.encode() + output
    try:
        conn.send(output)
    except BrokenPipeError:
        return

def getSource():
    try:
        source = cv2.VideoCapture(0)
        return source
    except "VIDEOIO ERROR":
        return False



if __name__ == '__main__':
    main()
