import ClientFunction
import Util

import pyautogui
import socket
import tkinter as tk
import tkinter.messagebox
import traceback

from PIL import ImageTk, Image
from tkinter import filedialog

class NoConnectionError(Exception):
    pass

class ClientApp:
    def __init__(self):
        """Initialize neccessary variables"""
        
        self.server_address = ""
        self.server_port = 12345
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        pass

    def connect(self):
        """ Establish a connection to the server"""

        self.server_address = self.entry_server_address.get()
        self.socket.connect((self.server_address, self.server_port))
        self.connected = True
        tk.messagebox.showinfo('Success', 'Connected to server successfully')

    def request(self, command, option, data):
        if not self.connected:
            raise NoConnectionError('No connection')
        else:
            self.socket.send(Util.package_message(command, option, data))

    def receive_reply(self):
        if not self.connected:
            raise NoConnectionError('No connection')
        else:
            return self.socket.recv(2 ** 16)

    def run(self):
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
            text='Connect',
            command=self.connect
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
            command=self.app_running_command
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
            text='Shut down',
            command=self.shutdown_command
        )

        self.btn_screenshot.grid(row=0, column=0)
        self.btn_app.grid(row=0, column=1)
        self.btn_process.grid(row=0, column=2)
        self.btn_registry.grid(row=1, column=0)
        self.btn_keylog.grid(row=1, column=1)
        self.btn_shutdown.grid(row=1, column=2)
        self.root.mainloop()
    
    def screenshot_command(self):
        sw = ClientFunction.ScreenshotWindow(self.root)
        sw.run()

    def process_running_command(self):
        pr = ClientFunction.ProcessWindow(self.root)
        pr.run()
        # pass

    def app_running_command(self):
        ap = ClientFunction.AppWindow(self.root)
        ap.run()

    def keylogging_command(self):
        kl = ClientFunction.KeyloggingWindow(self.root)
        kl.run()

    def registry_command(self):
        r = ClientFunction.RegistryWindow(self.root)
        r.run()

    def shutdown_command(self):
        self.request('shutdown', '', '')
        (error_code, error_message, _) = self.receive_reply()
        if error_code == 0:
            tk.messagebox.showinfo('Shutdown', 'Shut server down successfully')
        else:
            tk.messagebox.showerror('Error', error_message)

    def report_callback_exception(self, *args):
        error = traceback.format_exception(*args)
        error = error[len(error) - 1].split(':')[1].strip()
        tk.messagebox.showerror('Error', error)


if __name__ == '__main__':
    client_app = ClientApp()
    client_app.run()
