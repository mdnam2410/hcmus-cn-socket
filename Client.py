import ClientFunction

import pyautogui
import socket
import tkinter as tk
import tkinter.messagebox

from PIL import ImageTk, Image
from tkinter import filedialog

class ClientApp:
    def __init__(self):
        """Initialize client app with main window and buttons"""
        
        # Test later
        # ----------
        # self.server_address = ""
        # self.server_port = 0
        # self.socket = socket.socket()
        # self.socket.connect((server_address, server_port))

        # Create main window
        self.root = tk.Tk()
        self.root.configure(background='#F0F8FF')
        self.root.title('Client app')

        # Create buttons
        self.btn_app = tk.Button(
            master=self.root,
            text='App',
            bg='#F0F8FF',
            font=('arial', 12, 'normal'),
            # command=btn_app
        )

        self.btn_process = tk.Button(
            master=self.root,
            text='Process',
            bg='#F0F8FF',
            font=('arial', 12, 'normal'),
            # command=btn_process
        )

        self.btn_registry = tk.Button(
            master=self.root,
            text='Registry',
            bg='#F0F8FF',
            font=('arial', 12, 'normal')
        )

        self.btn_screenshot = tk.Button(
            master=self.root,
            text='Screenshot',
            bg='#F0F8FF',
            font=('arial', 12, 'normal'),
            command=self.screenshot_command
        )

    def __del__(self):
        pass

    def contact_server(self, command, option, data):
        # self.socket.send(package_message(command, option, data))
        pass

    def get_from_server(self):
        # return extract_message(self.socket.recv(2**32))
        pass

    def run(self):
        self.btn_app.pack()
        self.btn_process.pack()
        self.btn_registry.pack()
        self.btn_screenshot.pack()
        self.root.mainloop()

    def screenshot_command(self):
        sw = ClientFunction.ScreenshotWindow(self.root)
        sw.run()

    def show_error_message(self, e):
        self.error_message_box = tk.Tk()
        error_message = tk.Label(master=self.error_message_box, text=e)
        error_message.pack()
        self.error_message_box.mainloop()


if __name__ == '__main__':
    client_app = ClientApp()
    try:
        client_app.run()
    except Exception as e:
        # client_app.show_error_message(e)
        print(e)
        print(type(e))