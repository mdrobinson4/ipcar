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
        print('done')

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
        if key not in self.pressed and (key == 'Left' or key == 'Right' or key == 'Up' or key == 'Down'):
            self.pressed.append(key)
        elif key.lower() == 'escape':
            self.root.destroy()
            self.pressed = None

    def sendInput(self):
        while self.pressed != None:
            pressed = self.pressed
            try:
                if len(pressed) > 0:
                    data = pressed[0]
                    if len(pressed) > 1:
                        data += ':' + pressed[1]
                    data = data.zfill(10).encode()
                    print(data)
                    #self.socket.send(data)
            except IndexError:
                print('changed')
                pass
            except TypeError:
                break


if __name__ == '__main__':
    gui = SendCommands(None)
