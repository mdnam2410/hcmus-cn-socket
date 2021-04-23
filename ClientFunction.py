import Client

import pyautogui
import tkinter as tk
import tkinter.ttk as ttk

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
            text='Get',
            command=self.get_process_command
        )
        self.btn_get_process.pack()

        # Container frame for table
        self.frame_table = tk.Frame(
            master=self.root,
        )

        # Table of running processes
        self.table_process = ttk.Treeview(
            master=self.frame_table,
            columns=('ID', 'Name', 'Count Thread')
        )

        self.table_process.heading('#0', text='Index')
        self.table_process.heading('#1', text='ID')
        self.table_process.heading('#2', text='Name')
        self.table_process.heading('#3', text='Count Thread')

        self.table_process.column('#0', stretch=tk.YES)
        self.table_process.column('#1', stretch=tk.YES)
        self.table_process.column('#2', stretch=tk.YES)
        self.table_process.column('#3', stretch=tk.YES)
        self.table_process.pack(side='left')
        self.table_process_iid = -1 # Pointer for the table
        
        # Table scrollbar
        self.table_process_scrollbar = ttk.Scrollbar(
            master=self.frame_table,
            orient='vertical',
            command=self.table_process.yview
        )
        self.table_process_scrollbar.pack(side='right', fill='y')

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
            text='Start',
            command=self.start_process_command
        )
        self.btn_start_process.pack()

        self.btn_kill_process = tk.Button(
            master=self.frame_start_kill,
            text='Kill'
        )
        self.btn_kill_process.pack()

        self.frame_get.pack()
        self.frame_table.pack()
        self.frame_start_kill.pack()

    def table_clear_all(self):
        while self.table_process_iid >= 0:
            self.table_process.delete(self.table_process_iid)
            self.table_process_iid -= 1

    def get_process_command(self):
        self.request('process', 'list', '')
        (error_code, error_message, server_data) = self.receive_reply()
        
        self.table_clear_all()
        if error_code == 0:
            for line in server_data.splitlines():
                self.table_process_iid += 1
                t = tuple(line.split(','))
                self.table_process.insert(
                    parent='',
                    index='end',
                    iid=self.table_process_iid,
                    text=str(self.table_process_iid + 1),
                    values=t
                )
        else:
            tk.messagebox.showwarning('Error', error_message)

    def start_process_command(self):
        self.entry_start_process = tk.Entry(
            #master=
        )

        # process_name = self.entry_start_process.get()
        process_name = 'abc'

        self.request('process', 'start', process_name)
        (error_code, error_message, server_data) = self.receive_reply()
        if error_code == 0:
            tk.messagebox.showinfo('Start process', f'Start {process_name} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def kill_process_command(self):
        # TODO: Create a new window, request user for process ID input
        self.entry_kill_process = tk.Entry(
            # master=
        )
        process_id = self.entry_kill_process.get()

        self.request('process', 'kill', process_id)
        (error_code, error_message, server_data) = self.receive_reply()

        if error_code == 0:
            tk.messagebox.showinfo('Kill process', f'Kill process ID {process_id} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)

class KeyloggerWindow(LowerLevel):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Frame for buttons
        self.frame_button = tk.Frame(
            master=self.root,
        )

        self.btn_hook = tk.Button(
            master=self.frame_button,
            text='Hook',
            command=self.hook_command
        )
        self.btn_hook.pack()

        self.btn_unhook = tk.Button(
            master=self.frame_button,
            text='Unhook',
            state='disabled',
            command=self.unhook_command
        )
        self.btn_unhook.pack()

        self.btn_print = tk.Button(
            master=self.frame_button,
            text='Print',
            state='disabled',
            command=self.print_command
        )
        self.btn_print.pack()

        self.btn_delete = tk.Button(
            master=self.frame_button,
            text='Delete',
            state='disabled',
            command=self.delete_command
        )
        self.btn_delete.pack()

        self.text = tk.Text(
            master=self.root,
            padx=5,
            pady=5,
            state='disabled' # No text entry
        )

        self.frame_button.pack()
        self.text.pack()

        # A stream holding keystrokes hooked
        self.keystroke_stream = ''

    def hook_command(self):
        self.request('keylogging', 'hook', '')
        (error_code, error_message, server_data) = self.receive_reply()
        
        if error_code == 0:
            self.keystroke_stream += server_data
            self.btn_hook.configure(state='disabled')
            self.btn_unhook.configure(state='active')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def unhook_command(self):
        self.request('keylogging', 'unhook', '')
        (error_code, error_message, server_data) = self.receive_reply()

        if error_code == 0:
            self.btn_hook.configure(state='active')
            self.btn_print.configure(state='active')
            self.btn_delete.configure(state='active')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def print_command(self):
        self.text.configure(state='normal')
        self.text.insert(1.0, self.keystroke_stream)
        self.text.configure(state='disabled')

    def delete_command(self):
        self.text.configure(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.configure(state='disabled')

        self.btn_unhook.configure(state='disabled')
        self.btn_print.configure(state='disabled')
        self.btn_delete.configure(state='disabled')
        self.keystroke_stream = ''
