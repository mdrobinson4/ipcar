import tkinter as tk
import threading

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
        if key not in self.pressed and (key == 'Left' or key == 'Right' or key == 'Up' or key == 'Down'):
            self.pressed.append(key)

    def sendInput(self):
        while self.pressed != None:
            pressed = self.pressed
            try:
                if len(pressed) > 0:
                    data = pressed[0]
                    if len(pressed) > 1:
                        data += ':' + pressed[1]
                    data = data.zfill(10).encode()
                    if self.socket != None:
                        self.socket.send(data)
                    print(data)
                else:
                    if self.socket != None:
                        self.socket.send('0'.zfill(10).encode())
            except IndexError:
                pass
            except TypeError:
                break
        data = 'close'.zfill(10).encode()
        #print(data)
        if self.socket != None:
            self.socket.send(data) # close socket
        print('exit')
