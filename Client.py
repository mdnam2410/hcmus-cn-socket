import ClientFunction
import Util

import pyautogui
import socket
import tkinter as tk
import tkinter.messagebox
import traceback

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
        self.root.report_callback_exception = self.report_callback_exception
        self.root.title('Client app')

        self.frame1 = tk.LabelFrame(
            master=self.root,
            relief=tk.GROOVE,
            borderwidth=1,
            text='Connect to server'
        )
        self.frame1.pack(padx=5, pady=5, fill=tk.X, expand=True)

        self.entry_server_address = tk.Entry(
            master=self.frame1
        )
        self.entry_server_address.insert(tk.END, 'Enter server address')
        self.entry_server_address.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_connect = tk.Button(
            master=self.frame1,
            text='Connect'
        )
        self.btn_connect.pack(side=tk.LEFT, padx=5, pady=5)

        self.frame2 = tk.Frame(
            master=self.root,
            relief=tk.GROOVE,
            borderwidth=1
        )
        self.frame2.pack(padx=5, pady=5)

        # Create buttons
        self.btn_app = tk.Button(
            master=self.frame2,
            text='App',
            # command=btn_app
        )

        self.btn_process = tk.Button(
            master=self.frame2,
            text='Process',
            command=self.process_running_command
        )

        self.btn_registry = tk.Button(
            master=self.frame2,
            text='Registry',
            command=self.registry_command
        )

        self.btn_keylog = tk.Button(
            master=self.frame2,
            text='Keylogging',
            command=self.keylogging_command
        )

        self.btn_screenshot = tk.Button(
            master=self.frame2,
            text='Screenshot',
            command=self.screenshot_command
        )

        self.btn_shutdown = tk.Button(
            master=self.frame2,
            text='Shut down'
        )

        self.btn_screenshot.grid(row=0, column=0)
        self.btn_app.grid(row=0, column=1)
        self.btn_process.grid(row=0, column=2)
        self.btn_registry.grid(row=1, column=0)
        self.btn_keylog.grid(row=1, column=1)
        self.btn_shutdown.grid(row=1, column=2)

    def __del__(self):
        pass

    def request(self, command, option, data):
        # self.socket.send(Util.package_message(command, option, data))
        #pass
        print(Util.package_message(command, option, data))

    def receive_reply(self):
        # return Util.extract_message(self.socket.recv(2**32))
        return (0, 'OK', 'Let\'s go\n')

    def run(self):
        self.root.mainloop()

    def screenshot_command(self):
        sw = ClientFunction.ScreenshotWindow(self.root)
        sw.run()

    def process_running_command(self):
        pr = ClientFunction.ProcessWindow(self.root)
        pr.run()
        # pass

    def keylogging_command(self):
        kl = ClientFunction.KeyloggerWindow(self.root)
        kl.run()

    def registry_command(self):
        r = ClientFunction.RegistryWindow(self.root)
        r.run()

    def show_error_message(self, e):
        self.error_message_box = tk.Tk()
        error_message = tk.Label(master=self.error_message_box, text=e)
        error_message.pack()
        self.error_message_box.mainloop()

    def report_callback_exception(self, *args):
        error = traceback.format_exception(*args)
        tk.messagebox.showerror('Error', error)


if __name__ == '__main__':
    client_app = ClientApp()
    client_app.run()
