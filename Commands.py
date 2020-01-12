import tkinter as tk
import threading
import re

class Commands:
    def __init__(self, socket):
        self.pressed = []
        self.socket = socket
        self.root = tk.Tk()
        self.setup()
        print('done')

    def setup(self):
        sendThread = threading.Thread(target=self.sendInput)
        sendThread.start()
        self.getInput()
        sendThread.join()

    def getInput(self):
        self.frame = tk.Frame(self.root, width=200, height=200)
        self.frame.bind("<KeyPress>", self.keydown)
        self.frame.bind("<KeyRelease>", self.keyup)
        self.frame.pack()
        self.frame.focus_set()
        self.root.mainloop()

    def keyup(self, e):
        if e.keysym.lower() == 'escape':
            self.pressed = None
            self.root.destroy()
        elif e.keysym in self.pressed :
            self.pressed.pop(self.pressed.index(e.keysym))

    def keydown(self, e):
        key = e.keysym
        if key not in self.pressed: #and (key == 'Left' or key == 'Right' or key == 'Up' or key == 'Down'):
            self.pressed.append(key)

    def sendInput(self):
        prev = []
        while self.pressed != None:
            pressed = self.pressed
            try:
                if len(pressed) > 0:
                    data = ':'
                    for i in range(len(pressed)):
                        data += pressed[i] + ':'
                    data = data.zfill(15).encode()
                    if self.socket != None:
                        self.socket.send(data)
                    print(data)
                    #print(re.findall("(?<=\:)(.*?)(?=\:)", data.decode()))
                elif len(self.pressed) == 0:
                    data = (':-:'.zfill(15)).encode()
                    if self.socket != None:
                        self.socket.send(data)
            except IndexError:
                pass
            except TypeError:
                break
        data = ':close:'.zfill(15).encode()
        #print(data)
        if self.socket != None:
            self.socket.send(data) # close socket
        print('exit')

'''
if __name__ == '__main__':
    c = Commands(None)
'''
