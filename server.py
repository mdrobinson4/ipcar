import cv2
import sys 
import socket
import pickle
import time

def main():
    header = 10
    host = '192.168.1.228'
    port = 1050

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print('binded')
    sock.listen()
    conn, addr = sock.accept()

    cap = getSource()
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow("frame", frame)

        msg = pickle.dumps(frame)
        msg = ('len{}:<{}'.format(msg,HEADERSIZE)).encode() + msg

        print(msg)
        conn.send(msg)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break



def getSource():
    return cv2.VideoCapture(0)



if __name__ == '__main__':
    main()

