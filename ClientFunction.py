import Client

import pyautogui
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import filedialog


class LowerLevel(Client.ClientApp):
    def __init__(self, top_level_window):
        self.root = tk.Toplevel(top_level_window)
    
    def run(self):
        self.root.mainloop()

class ScreenshotWindow(LowerLevel):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Focus
        self.root.grab_set()
        self.root.title('Sreenshot')

        self.btn_frame = tk.Frame(
            master=self.root
        )

        # Buttons
        self.btn_take_screenshot = tk.Button(
            master=self.btn_frame,
            text='Take screenshot',
            command=self.take_screenshot_command
        )

        self.btn_show_screenshot = tk.Button(
            master=self.btn_frame,
            text='Show screenshot',
            command=self.show_screenshot_command
        )

        self.btn_save_screenshot = tk.Button(
            master=self.btn_frame,
            text='Save screenshot',
            command=self.save_screenshot_command
        )

        self.btn_delete_screenshot = tk.Button(
            master=self.btn_frame,
            text='Delete',
            command=self.delete_screenshot_command
        )

        # Canvas for showing screenshot
        self.canvas = tk.Canvas(master=self.root)
        
        self.btn_frame.pack()
        
        self.btn_take_screenshot.pack(side='left')
        self.btn_show_screenshot.pack(side='left')
        self.btn_save_screenshot.pack(side='left')
        self.btn_delete_screenshot.pack()

        self.btn_show_screenshot.configure(state='disabled')
        self.btn_save_screenshot.configure(state='disabled')
        self.btn_delete_screenshot.configure(state='disabled')
        self.canvas.pack()

    def take_screenshot_command(self):
        self.img = pyautogui.screenshot()
        self.btn_show_screenshot.configure(state='active')
        self.btn_save_screenshot.configure(state='active')
        self.btn_delete_screenshot.configure(state='active')

    def show_screenshot_command(self):
        self.image_tk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def save_screenshot_command(self):
        path = filedialog.asksaveasfilename(
            defaultextension='.jpg',
            filetypes=[('PNG files', '*.png'), ('JPG files', '*.jpg'), ('All files', '*.*')]
        )
        self.img.save(path)

    def delete_screenshot_command(self):
        self.canvas.delete('all')
        self.btn_show_screenshot.configure(state='disabled')
        self.btn_save_screenshot.configure(state='disabled')
        self.btn_delete_screenshot.configure(state='disabled')

class ProcessRunning(LowerLevel):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Button frame
        self.frame_get = tk.Frame(
            master=self.root
        )

        # Button for getting processes
        self.btn_get_process = tk.Button(
            master=self.frame_get,
            text='Get'
            # command=
        )
        self.btn_get_process.pack()

        # Table of running processes
        self.table_process = tk.ttk.Treeview(
            master=self.frame_get,
        )
        
        # Frame for start and kill functions
        self.frame_start_kill = tk.Frame(
            master=self.root,
        )

        # self.label_process_id = tk.Label(
        #     master=self.frame_start_kill,
        #     text='Process ID'
        # )

        # self.entry_process_id = tk.Entry(
        #     master=self.frame_start_kill,
        #     text='Enter process ID'
        # )

        self.btn_start_process = tk.Button(
            master=self.frame_start_kill,
            text='Start'
        )
        self.btn_start_process.pack()

        self.btn_kill_process = tk.Button(
            master=self.frame_start_kill,
            text='Kill'
        )
        self.btn_kill_process.pack()

        self.frame_get.pack()
        self.frame_start_kill.pack()

    def get_process_command(self):
        self.request('process', 'list', '')
        (error_code, error_message, server_data) = self.receive_reply()

        if error_code == 0:
            # TODO: List the processes in the Treeview table object
            pass
        else:
            pass
            # TODO: Raise an exception for error message box

    def start_process_command(self):
        self.entry_start_process = tk.Entry(
            #master=
        )

        process_name = self.entry_start_process.get()

        self.request('process', 'start', process_name)
        (error_code, error_message, server_data) = self.receive_reply()
        if error_code == 0:
            # TODO: Pop up a 'Process start successfully'
            pass
        else:
            # TODO: Raise an exception
            pass

    def kill_process_command(self):
        # TODO: Create a new window, request user for process ID input
        self.entry_kill_process = tk.Entry(
            # master=
        )
        process_id = self.entry_kill_process.get()

        self.request('process', 'kill', process_id)
        (error_code, error_message, server_data) = self.receive_reply()

        if error_code == 0:
            # TODO: Pop up a 'Kill process {process_id} successfully'
            pass
        else:
            # TODO: Raise an exception
            pass
