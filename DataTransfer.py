import cv2
import socket
from io import BytesIO
import numpy as np

class DataTransfer:
    def __init__(self, socket, conn, addr):
        # initialize variables
        self.socket = socket
        self.conn = conn
        self.addr = addr
        self.scale = 1
        self.transferLimit = 1024

    def setupServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print('listening')
        self.conn, self.addr = self.socket.accept()
        print('connected')
        return

    def setupClient(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return

    def sendFrames(self, frame):
        resizedFrame = self.resizeFrame(frame) # resize frame
        compressedFrame = self.compressData(resizedFrame) # convert numpy array to bytes
        self.conn.send(compressedFrame) # send compressed array

    def receiveFrames(self):
        dataLen = None
        buffer = b''
        data = self.socket.recv(1024)
        if dataLen == None:
            dataLen, temp, buffer = data.partition(b':')
            dataLen = int(dataLen)
        while len(buffer) < dataLen:
            dataRem = dataLen - len(buffer)
            bytes = self.transferLimit
            if dataRem < self.transferLimit:
                bytes = dataRem
            buffer += self.socket.recv(dataRem)
        image = np.load(BytesIO(buffer))['frame']
        return image


    def resizeFrame(self, frame):
        bwFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = bwFrame.shape[:2]
        scaled = (int(self.scale*width), int(self.scale*height))
        resized = cv2.resize(bwFrame, scaled)
        return resized

    def compressData(self, resized):
        f = BytesIO()
        np.savez_compressed(f, frame=resized)
        f.seek(0)
        compressedFrame = f.read()
        dataSize = "{0}:".format(len(f.getvalue()))
        compressedFrame = dataSize.encode() + compressedFrame
        return compressedFrame
