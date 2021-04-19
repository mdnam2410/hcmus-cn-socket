import os
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
class fileReg:
    def __init__ (self, path):
        self.path = path
    def set(self, path):
        self.path = path
    def p(self):
        return str(self.path)
reg = fileReg("")
# this is the function called when the button is clicked
def btnShowClickFunction():
    print(reg.p())
    if(reg.p()!=""):
        os.system('notepad'+' '+reg.p())
'''
def textEditor(s):
    root1 = tk.Tk()
    root1.geometry("350x250")
    root1.title("editor")
    root1.minsize(height=250, width=350)
    root1.maxsize(height=250, width=350)
    
    
    # adding scrollbar
    scrollbar = tk.Scrollbar(root)
    
    # packing scrollbar
    scrollbar.pack(side=tk.RIGHT,
                fill=tk.Y)
    
    
    text_info = tk.Text(root,yscrollcommand=scrollbar.set)
    text_info.insert(tk.INSERT, s)
    text_info.pack(fill=tk.BOTH)
    
    # configuring the scrollbar
    scrollbar.config(command=text_info.yview)
    
    root1.mainloop()
'''
def btnLoadClickFunction():
    print('clicked')
    reg.set(tk.filedialog.askopenfilename())

# this is the function called when the button is clicked
def btnQuitClickFunction():
    print('quit')
    root.destroy()

root.geometry('400x300')
root.title('Regeditor')

tk.Button(root, text='load', command=btnLoadClickFunction).place(x=5, y=5)

tk.Button(root, text='quit', command=btnQuitClickFunction).place(x=360, y=265)

tk.Button(root, text='showFile', command=btnShowClickFunction).place(x=300, y=265)

root.mainloop()