import tkinter as tk
import threading

class SendCommands:
    def __init__(self, socket):
        self.pressed = []
        self.socket = socket
        self.root = tk.Tk()
        self.setup()

    def setup(self):
        sendThread = threading.Thread(target=self.sendInput)
        sendThread.start()
        self.getInput()
        sendThread.join()

    def getInput(self):
        self.root.bind("<KeyPress>", self.keydown)
        self.root.bind("<KeyRelease>", self.keyup)
        self.root.focus_set()
        self.root.withdraw()
        self.root.mainloop()

    def keyup(self, e):
        if  e.keysym in self.pressed :
            self.pressed.pop(self.pressed.index(e.keysym))

    def keydown(self, e):
        key = e.keysym
        if key.lower() == 'escape':
            self.root.destroy()
            self.pressed = None
        elif not key in self.pressed and not 'Shift' in key:
            self.pressed.append(key.lower())

    def sendInput(self):
        while self.pressed != None:
            if len(self.pressed) > 0:
                #print(self.pressed)
                str = self.pressed[0]
                if len(self.pressed) > 1:
                    str += ':' + self.pressed[1]
                str.zfill(10)
                print(str)
                #self.socket.send(self.pressed)
        print('quit')

if __name__ == '__main__':
    gui = SendCommands(None)
