import Util

import socket
import tkinter as tk
import tkinter.messagebox
import traceback
import base64
import io
import tkinter.ttk as ttk

from PIL import Image, ImageTk
from tkinter import filedialog

server_address = ""
server_port = 9098
connected = False
s = None

class NoConnectionError(Exception):
    pass

class ClientApp:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def connect(self):
        """ Establish a connection to the server"""

        global server_address
        global server_port
        global connected
        global s

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = self.entry_server_address.get()
            s.connect((server_address, server_port))
            connected = True
            self.entry_server_address['state']=tk.DISABLED
            self.btn_connect.pack_forget()
            self.btn_disconnect.pack()
            tk.messagebox.showinfo('Success', 'Connected to server successfully')
        except ConnectionError:
            tk.messagebox.showerror('Error', 'Cannot connect to server')

    def disconnect(self):
        """ Close a connection to the server """

        global connected
        global s
        
        s.close()
        connected = False
        self.entry_server_address['state']=tk.NORMAL
        self.btn_disconnect.pack_forget()
        self.btn_connect.pack()

    def request(self, command, option, data):
        global connected
        global s
        if not connected:
            raise NoConnectionError('No connection')
        else:
            m = Util.package_message(command, option, data)
            s.send(m)

    def receive_reply(self):
        global connected
        global s

        if not connected:
            raise NoConnectionError('No connection')
        else:
            return Util.extract_message(s.recv(2 ** 20), message_type='server')

    def entry_server_address_on_enter(self, event):
        self.entry_server_address.delete('0','end')
        self.entry_server_address.insert('0','127.0.0.1')
        self.entry_server_address.unbind("<Enter>")

    def run(self):
        # Create main window
        self.root = tk.Tk()
        # self.root.report_callback_exception = self.report_callback_exception
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
        self.entry_server_address.bind("<Enter>",self.entry_server_address_on_enter)
        self.entry_server_address.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_connect = tk.Button(
            master=self.frame1,
            text='Connect',
            command=self.connect
        )
        self.btn_connect.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_disconnect = tk.Button(
            master=self.frame1,
            text='Disconnect',
            command=self.disconnect
        )
        self.btn_disconnect.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_disconnect.pack_forget()

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
        sw = ScreenshotWindow(self.root)
        sw.run()

    def process_running_command(self):
        pr = ProcessWindow(self.root)
        pr.run()

    def app_running_command(self):
        ap = AppWindow(self.root)
        ap.run()

    def keylogging_command(self):
        kl = KeyloggingWindow(self.root)
        kl.run()

    def registry_command(self):
        r = RegistryWindow(self.root)
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

class FunctionWindow(ClientApp):
    def __init__(self, top_level_window):
        super().__init__()
        self.window = tk.Toplevel(top_level_window)
    
    def run(self):
        self.window.mainloop()

class ScreenshotWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Focus
        self.window.grab_set()
        self.window.title('Sreenshot')

        # Container frame for buttons
        self.frame_buttons = tk.Frame(
            master=self.window
        )

        # Buttons
        self.btn_take_screenshot = tk.Button(
            master=self.frame_buttons,
            text='Take screenshot',
            command=self.take_screenshot_command
        )

        self.btn_show_screenshot = tk.Button(
            master=self.frame_buttons,
            text='Show screenshot',
            command=self.show_screenshot_command
        )

        self.btn_save_screenshot = tk.Button(
            master=self.frame_buttons,
            text='Save screenshot',
            command=self.save_screenshot_command
        )

        self.btn_delete_screenshot = tk.Button(
            master=self.frame_buttons,
            text='Delete',
            command=self.delete_screenshot_command
        )
        

        # Canvas for showing screenshot
        self.canvas = tk.Canvas(master=self.window)
        
        # Pack buttons
        self.btn_take_screenshot.pack(side='left')
        self.btn_show_screenshot.pack(side='left')
        self.btn_save_screenshot.pack(side='left')
        self.btn_delete_screenshot.pack()

        # These buttons are disabled initially
        self.btn_show_screenshot.configure(state='disabled')
        self.btn_save_screenshot.configure(state='disabled')
        self.btn_delete_screenshot.configure(state='disabled')

        # Packing frame and canvas
        self.frame_buttons.pack()
        self.canvas.config(width=480, height=360)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def take_screenshot_command(self):
        self.request('screenshot', '', '')
        error_code, error_message, data = self.receive_reply()

        if error_code == 0:

            # # Add padding
            # data += '=' * (len(data) % 4)

            # Retrieve raw image from base64-encoded data
            raw = io.BytesIO(base64.b64decode(data.encode()))

            # Create the image
            self.original_image = Image.open(raw)

            # Resize for displaying on canvas
            self.resized_image = self.original_image.resize((480, 360), Image.ANTIALIAS)

            # Enable these button since the image is available now
            self.btn_show_screenshot.configure(state='active')
            self.btn_save_screenshot.configure(state='active')
            self.btn_delete_screenshot.configure(state='active')
        else:
            tk.messagebox.showerror('Error', error_message)

    def show_screenshot_command(self):
        self.image_tk = ImageTk.PhotoImage(self.resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def save_screenshot_command(self):
        try:
            path = filedialog.asksaveasfilename(
                defaultextension='.jpg',
                filetypes=[('PNG files', '*.png'), ('JPG files', '*.jpg'), ('All files', '*.*')]
            )
            self.original_image.save(path)
        except:
            # Ignore exceptions raised by filedialog
            pass

    def delete_screenshot_command(self):
        self.canvas.delete('all')
        self.btn_show_screenshot.configure(state='disabled')
        self.btn_save_screenshot.configure(state='disabled')
        self.btn_delete_screenshot.configure(state='disabled')

class ProcessWindow(FunctionWindow):
    """ This class is designed to reuse for the AppWindow too"""

    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        self.window.title('Process')
        self.window.rowconfigure(0, weight=1, minsize=10)
        self.window.rowconfigure(1, weight=1, minsize=50)

        # Frame for buttons
        self.frame_buttons = tk.Frame(
            master=self.window
        )

        # Buttons
        self.btn_get = tk.Button(
            master=self.frame_buttons,
            text='Get',
            command=self.get_command
        )

        self.btn_delete = tk.Button(
            master=self.frame_buttons,
            text='Delete',
            command=self.delete_command
        )

        self.btn_start = tk.Button(
            master=self.frame_buttons,
            text='Start',
            command=self.start_command
        )

        self.btn_kill = tk.Button(
            master=self.frame_buttons,
            text='Kill',
            command=self.kill_command
        )

        # Container frame for table
        self.frame_table = tk.Frame(
            master=self.window,
        )

        # Table of running processes
        self.table = ttk.Treeview(
            master=self.frame_table,
            columns=('ID', 'Name', 'Count Thread'),
        )
        self.table['show'] = 'headings'
        self.table.heading('#1', text='Name')
        self.table.heading('#2', text='ID')
        self.table.heading('#3', text='Count Thread')
        self.table.column('#1', stretch=tk.YES)
        self.table.column('#2', stretch=tk.YES)
        self.table.column('#3', stretch=tk.YES)
        # Pointer points to the bottom element of the table
        self.table_process_iid = -1
        
        # Table scrollbar
        self.table_scrollbar = ttk.Scrollbar(
            master=self.frame_table,
            orient='vertical',
            command=self.table.yview
        )
        
        # Packing buttons
        self.btn_get.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.btn_delete.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.btn_start.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.btn_kill.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)

        # Packing table
        self.table.pack(side='left', fill='y', expand=True)
        self.table_scrollbar.pack(side='right', fill='y')

        # Placing frames
        self.frame_buttons.grid(row=0, column=0, padx=5, pady=5)
        self.frame_table.grid(row=1, column=0, padx=5, pady=5)

    def delete_command(self):
        """ Clear all content of the table"""

        while self.table_process_iid >= 0:
            self.table.delete(self.table_process_iid)
            self.table_process_iid -= 1

    def get_command(self):
        self.request('process', 'list', '')
        (error_code, error_message, server_data) = self.receive_reply()
        
        # Clear the table
        self.delete_command()
        if error_code == 0:
            # Display each process in each row of the table
            for line in server_data.splitlines():
                self.table_process_iid += 1
                t = tuple(line.split(','))
                self.table.insert(
                    parent='',
                    index='end',
                    iid=self.table_process_iid,
                    values=t
                )
        else:
            tk.messagebox.showwarning('Error', error_message)

    def start(self, window, entry):
        """ Auxiliary function, make it a method for reuse"""

        process_name = entry.get()
        self.request('process', 'start', process_name)
        (error_code, error_message, _) = self.receive_reply()
        window.destroy()
        if error_code == 0:
            tk.messagebox.showinfo('Start process', f'Start {process_name} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)
    
    def start_command(self):
        # Create a new window to get input
        w = tk.Toplevel(self.window)
        w.title('Start')
        
        # The window has one entry and one button
        entry_start = tk.Entry(
            master=w,
            width=50
        )

        btn_send = tk.Button(
            master=w,
            text='Start',
            command=lambda: self.start(w, entry_start)
        )

        # Packing
        entry_start.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        btn_send.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Run
        w.mainloop()
        
    def kill(self, window, entry):
        """ Auxiliary function, make it a method for reuse"""
        
        process_id = entry.get()
        self.request('process', 'kill', process_id)
        (error_code, error_message, _) = self.receive_reply()
        window.destroy()
        if error_code == 0:
            tk.messagebox.showinfo('Kill process', f'Kill process ID {process_id} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def kill_command(self):
        # Create a new window to get input
        w = tk.Toplevel(self.window)
        w.title('Kill')

        # The window has one entry and one button
        entry_kill = tk.Entry(
            master=w,
            width=50
        )

        btn_kill = tk.Button(
            master=w,
            text='Kill',
            command=lambda: self.kill(w, entry_kill)
        )

        # Packing
        entry_kill.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        btn_kill.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Run
        w.mainloop()

class AppWindow(ProcessWindow):
    """ Reused from ProcessWindow"""

    def __init__(self, top_level_window):
        super().__init__(top_level_window)
        self.window.title('App')

    def get_command(self):
        self.request('app', 'list', '')
        (error_code, error_message, server_data) = self.receive_reply()
        
        # Clear the table
        self.delete_command()
        if error_code == 0:
            # Display each process in each row of the table
            for line in server_data.splitlines():
                self.table_process_iid += 1
                t = tuple(line.split(','))
                self.table.insert(
                    parent='',
                    index='end',
                    iid=self.table_process_iid,
                    values=t
                )
        else:
            tk.messagebox.showwarning('Error', error_message)
    
    def kill_command(self):
        # Create a new window to get input
        w = tk.Toplevel(self.window)
        w.title('Kill')

        # The window has one entry and one button
        entry_kill = tk.Entry(
            master=w,
            width=50
        )

        btn_kill = tk.Button(
            master=w,
            text='Kill',
            command=lambda: self.kill(w, entry_kill)
        )

        # Packing
        entry_kill.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        btn_kill.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Run
        w.mainloop()

    def kill(self, window, entry):
        process_id = entry.get()
        self.request('app', 'kill', process_id)
        (error_code, error_message, _) = self.receive_reply()
        window.destroy()
        if error_code == 0:
            tk.messagebox.showinfo('Kill app', f'Kill app ID {process_id} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def start(self, window, entry):
        process_name = entry.get()
        self.request('app', 'start', process_name)
        (error_code, error_message, _) = self.receive_reply()
        window.destroy()
        if error_code == 0:
            tk.messagebox.showinfo('Start app', f'Start {process_name} successfully')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def start_command(self):
        # Create a new window to get input
        w = tk.Toplevel(self.window)
        w.title('Start')
        
        # The window has one entry and one button
        entry_start = tk.Entry(
            master=w,
            width=50
        )

        btn_send = tk.Button(
            master=w,
            text='Start',
            command=lambda: self.start(w, entry_start)
        )

        # Packing
        entry_start.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        btn_send.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Run
        w.mainloop()

class KeyloggingWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        self.window.title('Keylogging')

        # A stream holding keystrokes hooked
        self.keystroke_stream = ''

        # Frame for buttons
        self.frame_button = tk.Frame(
            master=self.window,
        )

        # Buttons
        self.btn_hook = tk.Button(
            master=self.frame_button,
            text='Hook',
            command=self.hook_command
        )

        self.btn_unhook = tk.Button(
            master=self.frame_button,
            text='Unhook',
            state='disabled',
            command=self.unhook_command
        )

        self.btn_print = tk.Button(
            master=self.frame_button,
            text='Print',
            state='disabled',
            command=self.print_command
        )

        self.btn_delete = tk.Button(
            master=self.frame_button,
            text='Delete',
            command=self.delete_command
        )

        # Text for displaying results
        self.text = tk.Text(
            master=self.window,
            padx=5,
            pady=5,
            state='disabled'
        )

        # Packing buttons
        self.btn_hook.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_unhook.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_print.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

        # Packing frame and text
        self.frame_button.pack()
        self.text.pack()

    def hook_command(self):
        self.request('keylogging', 'hook', '')
        (error_code, error_message, _) = self.receive_reply()
        
        if error_code == 0:
            # Prevent duplicate hook
            self.btn_hook.configure(state='disabled')
            self.btn_unhook.configure(state='active')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def unhook_command(self):
        self.request('keylogging', 'unhook', '')
        (error_code, error_message, server_data) = self.receive_reply()

        if error_code == 0:
            # Add the incoming hooked keys to the stream
            self.keystroke_stream += server_data

            # Client can continue hooking or print the result
            self.btn_hook.configure(state='active')
            self.btn_print.configure(state='active')

            # Prevent duplicate unhook
            self.btn_unhook.configure(state='disabled')
        else:
            tk.messagebox.showwarning('Error', error_message)

    def print_command(self):
        # Insert the hooked keys
        self.text.configure(state='normal')
        self.text.insert(1.0, self.keystroke_stream)
        self.text.configure(state='disabled')

        # Flush the stream
        self.keystroke_stream = ''

        # No more data to print
        self.btn_print.configure(state='disabled')

    def delete_command(self):
        # Clean the text entry
        self.text.configure(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.configure(state='disabled')


class RegistryWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        self.path =''

        self.window.grab_set()
        self.window.title('Registry')

        self.window.rowconfigure(0, weight=1, minsize=75)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.rowconfigure(2, weight=1, minsize=10)
        self.window.columnconfigure(0, weight=1, minsize=50)

        # Divide the window into three frames
        self.create_frame1()
        self.create_frame2()
        self.create_frame3()

        self.frame1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.frame2.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.frame3.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def create_frame1(self):
        # Frame containing buttons and entries for sending registry files
        self.frame1 = tk.Frame(
            master=self.window,
            relief=tk.GROOVE,
            borderwidth=1    
        )

        for i in range(2):
            for j in range(2):
                self.frame1.rowconfigure(i, weight=1, minsize=20)
                self.frame1.columnconfigure(j, weight=1)

        # Entry for displaying browsed registry file
        self.entry_browse_registry_file = tk.Entry(
            master=self.frame1
        )

        # Browse button
        self.btn_browse = tk.Button(
            master=self.frame1,
            text='Browse',
            command=self.browse_command,
        )

        # Text widget for showing the registry file content
        self.text_registry_file_content = tk.Text(
            master=self.frame1,
            height=5,
            width=50
        )

        # Send registry file button
        self.btn_send_registry_file = tk.Button(
            master = self.frame1,
            text='Send',
            height=10,
            command=self.send_registry_file_command
        )

        # Placing the widgets
        self.entry_browse_registry_file.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.btn_browse.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.text_registry_file_content.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.btn_send_registry_file.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    def create_frame2(self):
        # Frame containing buttons, entries, and dropboxes for modifying registry keys directly
        self.frame2 = tk.Frame(
            master=self.window,
            relief=tk.GROOVE,
            borderwidth=1
        )

        # Menu for choosing types of modification
        self.MODIFICATION_TYPE = [
            'Get value',
            'Set value',
            'Delete value',
            'Create key',
            'Delete key'
        ]
        self.modification_type_var = tk.StringVar(self.window)
        self.modification_type_var.set('Select an option')

        self.menu_function = ttk.Combobox(
            master=self.frame2,
            textvariable=self.modification_type_var
        )
        self.menu_function['values'] = self.MODIFICATION_TYPE
        self.menu_function.bind('<<ComboboxSelected>>', self.frame2_alternate_widgets)

        # Entry for key name input
        self.entry_key_name = tk.Entry(
            master=self.frame2
        )
        self.entry_key_name.insert('0','Path key')
        
        # Container frame for value name entry, new data entry, and data type combobox
        self.frame_wrap = tk.Frame(
            master=self.frame2
        )

        # Entry for value name input
        self.entry_value_name = tk.Entry(
            master=self.frame_wrap
        )
        self.entry_value_name.insert('0','Value')
        
        # Entry for new data input
        self.entry_data = tk.Entry(
            master=self.frame_wrap
        )
        self.entry_data.insert('0','Data')

        # Combobox for data types
        self.DATA_TYPES = [
            'String',
            'Binary',
            'DWORD',
            'QWORD',
            'Multi-String',
            'Expandable String'
        ]
        self.data_type_var = tk.StringVar(self.window)
        self.data_type_var.set('Data type')

        self.menu_data_type = ttk.Combobox(
            master=self.frame_wrap,
            textvariable=self.data_type_var,
        )
        self.menu_data_type['values'] = self.DATA_TYPES

        # Text entry for displaying result
        self.text_result = tk.Text(
            master=self.frame2,
            height=8
        )
        self.text_result.configure(state='disabled')

        # Packing all widgets
        self.menu_function.pack(fill=tk.X, padx=5, pady=5)
        self.entry_key_name.pack(fill=tk.X, padx=5, pady=5, expand=True)
        self.entry_value_name.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.entry_data.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.menu_data_type.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.frame_wrap.pack(fill=tk.X, expand=True)
        self.text_result.pack(fill=tk.X, expand=True)

    def create_frame3(self):
        # Container frame for the send and delete buttons
        self.frame3 = tk.Frame(
            master=self.window,
            relief=tk.GROOVE,
            borderwidth=1
        )

        # Buttons
        self.btn_send = tk.Button(
            master=self.frame3,
            text='Send',
            width=10,
            command=self.send_command
        )

        self.btn_delete = tk.Button(
            master=self.frame3,
            text='Delete',
            width=10,
            command=self.delete_command
        )

        # Packing
        self.btn_send.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

    def frame2_alternate_widgets(self, event):
        """ Displaying widgets according to the modification types chosen by user """

        if self.modification_type_var.get() in {'Get value', 'Delete value'}:
            self.entry_data.pack_forget()
            self.menu_data_type.pack_forget()
        elif self.modification_type_var.get() in {'Create key', 'Delete key'}:
            self.frame_wrap.pack_forget()    
        else:
            self.entry_data.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
            self.menu_data_type.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
            self.frame_wrap.pack()

    def browse_command(self):
        try:
            self.path = filedialog.askopenfilename(
                title='Select registry file',
                filetypes=(('reg files', '*.reg'), ('All files', '*.*'))
            )
            self.entry_browse_registry_file.insert(0, self.path)
            content = open(self.path).read()
            self.text_registry_file_content.delete('1.0',tk.END)
            self.text_registry_file_content.insert('1.0', content)
        except:
            pass

    def send_registry_file_command(self):
        content = self.text_registry_file_content.get('1.0', tk.END)
        self.request('reg', 'send', content)
        (error_code, error_message, _) = self.receive_reply()
        if error_code == 0:
            tk.messagebox.showinfo('Success', 'Success')
        else:
            tk.messagebox.showerror('Error', error_message)
    
    def send_command(self):
        option = self.modification_type_var.get()
        c, v = option.split(' ')
        option = c.lower()
        if v == 'key':
            option += '-' + v
        
        key_name = self.entry_key_name.get()
        value_name = self.entry_value_name.get()
        new_data = self.entry_data.get()
        data_type = self.data_type_var.get()

        client_data = ','.join([key_name, value_name, data_type, new_data])

        self.request('reg', option, client_data)
        error_code, error_message, server_data = self.receive_reply()
        if error_code == 0:
            if option == 'get':
                self.text_result.configure(state='normal')
                self.text_result.insert('1.0', server_data)
                self.text_result.configure(state='disabled')
            else:
                tk.messagebox.showinfo('Success', 'Nice!')
        else:
            tk.messagebox.showerror('Error', error_message)

    def delete_command(self):
        self.text_result.configure(state='active')
        self.text_result.delete('1.0', tk.END)
        self.text_result.configure(state='disabled')


if __name__ == '__main__':
    client_app = ClientApp()
    client_app.run()
