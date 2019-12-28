import cv2
import DataTransfer

def main():
    command = input()
    print(command)
    return
    host = 'localhost'
    port = 1050
    state = 'client'
    client = DataTransfer.DataTransfer(host, port, state)
    getFrames(client)

def getFrames(client):
    while True:
        frame = client.receiveFrames()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
