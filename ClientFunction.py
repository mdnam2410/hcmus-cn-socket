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