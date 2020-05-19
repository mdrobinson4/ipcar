import cv2
import socket
from io import BytesIO
import numpy as np
import os

class DataTransfer:
    def __init__(self, socket, clientAddr, port, protocol):
        # initialize variables
        self.protocol = protocol
        self.socket = socket
        self.scale = 1/2
        self.transferLimit = 65507 # udp limit
        self.client = (clientAddr, port)

    ''' stream video to the controller '''
    def sendFrames(self, frame):
        resizedFrame = self.resizeFrame(frame) # resize frame
        compressedFrame = self.compressData(resizedFrame) # convert numpy array to bytes
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
            self.socket.sendto(data, self.client)
            # update the number of bytes that have been sent
            bytesSent += bytesToSend
            # update the amount of data left
            bytesRem -= bytesToSend
    
    ''' get video stream from the rover '''
    def receiveFrames(self):
        dataLen = None
        buffer = b''
        bytesToRec = 0
        # empty image
        image = np.zeros((480,640,3), np.uint8)
        # receive limit
        try:
            data, address = self.socket.recvfrom(self.transferLimit)
        except socket.timeout:
            return
        try:
            # get the header from the first packet
            dataLen, temp, buffer = data.partition(b':')
            # get value telling us the total size of data to be received
            dataLen = int(dataLen)
        except:
            return image
        try:
            # continue listening for data until the entire frame has been sent
            while len(buffer) < dataLen:
                # amount of data we have left to attain
                dataRem = dataLen - len(buffer)
                # receive the maximum number of data possible
                bytesToRec = self.transferLimit
                # dynamically adjust the amount of data we are waiting for
                if dataRem < self.transferLimit:
                    bytesToRec = dataRem
                (bufferRec, address) = self.socket.recvfrom(bytesToRec)
                # build up frame buffer
                buffer += bufferRec
            image = np.load(BytesIO(buffer))['frame']
        except:
            return np.zeros((480,640,3), np.uint8)
        return image

    def resizeFrame(self, frame):
        # grayscale image
        bwFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = bwFrame.shape[:2]
        scaled = (int(self.scale*width), int(self.scale*height))
        resized = cv2.resize(bwFrame, scaled)
        return resized
    
    ''' encode frame '''
    def compressData(self, resized):
        f = BytesIO()
        np.savez_compressed(f, frame=resized)
        f.seek(0)
        compressedFrame = f.read()
        dataSize = "{0}:".format(len(f.getvalue()))
        compressedFrame = dataSize.encode() + compressedFrame
        return compressedFrame

