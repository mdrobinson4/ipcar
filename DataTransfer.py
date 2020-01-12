import cv2
import socket
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
import os

class DataTransfer:
    def __init__(self, socket, conn, addr, port, protocol):
        # initialize variables
        self.protocol = protocol
        self.socket = socket
        self.conn = conn
        self.addr = addr
        self.port = port
        self.scale = 1
        if protocol == 'tcp':
            self.transferLimit = 1024
        elif protocol == 'udp':
            self.transferLimit = 65507
        self.clientAddr = None
        #project_folder = os.path.expanduser('~/ipcar')  # adjust as appropriate
        load_dotenv()


    def sendFrames(self, frame):
        if self.clientAddr == None:
            self.clientAddr = (os.getenv('clientHost'), self.port)
        resizedFrame = self.resizeFrame(frame) # resize frame
        compressedFrame = self.compressData(resizedFrame) # convert numpy array to bytes
        if self.protocol == 'tcp':
            self.conn.send(compressedFrame) # send compressed array
        elif self.protocol == 'udp':
            bytesToSend = 0
            bytesSent = 0
            bytesRem = len(compressedFrame)
            while bytesRem > 0:
                bytesToSend = self.transferLimit
                # if we have reach end of stream, simply send the data that is left
                if bytesRem < self.transferLimit:
                    bytesToSend = bytesRem
                # split the array into chunks to send
                data = compressedFrame[bytesSent : bytesSent + bytesToSend]
                self.socket.sendto(data, self.clientAddr)
                # update the number of bytes that have been sent
                bytesSent += bytesToSend
                # update the amount of data left
                bytesRem -= bytesToSend

    def receiveFrames(self):
        dataLen = None
        buffer = b''
        bytesToRec = 0
        image = np.zeros((480,640,3), np.uint8)
        data, address = self.socket.recvfrom(self.transferLimit)
        if dataLen == None:
            dataLen, temp, buffer = data.partition(b':')
            try:
                dataLen = int(dataLen)
            except ValueError:
                return image

        while len(buffer) < dataLen:
            dataRem = dataLen - len(buffer)
            bytesToRec = self.transferLimit
            if dataRem < self.transferLimit:
                bytesToRec = dataRem
            try:
                (bufferRec, address) = self.socket.recvfrom(bytesToRec)
            except:
                return np.zeros((480,640,3), np.uint8)
            buffer += bufferRec
        try:
            image = np.load(BytesIO(buffer))['frame']
        except:
            return np.zeros((480,640,3), np.uint8)
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
