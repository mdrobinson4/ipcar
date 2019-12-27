import cv2
import DataTransfer

def main():
    host = 'localhost'
    port = 1050
    state = 'server'
    server = DataTransfer.DataTransfer(host, port, state)
    cap = cv2.VideoCapture(0)
    sendFrames(server, cap)

def sendFrames(server, cap):
    while cap != False and cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            server.sendFrames(frame)
        else:
            break

if __name__ == '__main__':
    main()
