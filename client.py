import socket
import sys
import cv2
import pickle

def main():
    host = '192.168.1.228'
    port = 1050
    header = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(host, port)
    getData(header)
    
    def getData(h_size):
        full_msg = b''
        len_msg = 0
        new_msg = True
        while True:
            msg = sock.recv(16)
            if new_msg == True:
                print('new msg len: {}'.format(msg[:h_size]))
                len_msg = int(msg[:h_size])
                new_msg = False
            print('full message length: {}'.format(len_msg))
            print('collecting message')
            full_msg += msg
            print(len(full_msg))

            if len(full_msg) - HEADERSIZE == len_msg:
                print('full message received')
                frame = pickle.loads(full_msg[h_size:])
                cv2.imshow(frame)
                new_msg = True
                full_msg = b''


