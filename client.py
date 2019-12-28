import cv2
import DataTransfer

def main():
    command = input()
    print(command)
    return
    host = 'localhost'
    port = 1050
    state = 'client'

    getFrames(host, port)
    getCommands(host, port)

def getFrames(client):
    socket = setupClient(host, port)
    transfer = DataTransfer.DataTransfer(socket, None, None)
    while True:
        frame = transfer.receiveFrames()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def sendCommands(host, port):
    socket = setupClient(host, port)
    command = Commands.Commands(socket)

def setupClient(location):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((host, port + 1))
    return socket



if __name__ == '__main__':
    main()
