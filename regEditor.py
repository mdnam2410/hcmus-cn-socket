import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import subprocess
root = tk.Tk()

SIZE_ROW = 30
H = 190
W = 360
var=StringVar()

E1 = tk.Entry(root, textvariable=var,relief=tk.RAISED, state=DISABLED) 
E1.place(x=60, y=5, width = W-60, height = SIZE_ROW-10)
def selectFile():
    if(var.get()==""):
        tk.messagebox.showerror("Warning","No file selected")
        return False
    return True

def success(msg=""):
    if(msg==""):
        tk.messagebox.showinfo("Alert","Operate successfully")
    else:
        tk.messagebox.showinfo("Alert",msg)

def fail(msg=""):
    if(msg==""):
        tk.messagebox.showerror("Alert","Operate failed")
    else:
        tk.messagebox.showerror("Alert",msg)
# this is the function called when the button is clicked
def btnEditClickFunction():
    if(not selectFile()):
        return
    print('edit')
    print("Selected file:"+var.get())
    if(var.get()!=""):
        os.system('notepad'+' '+var.get())

def btnProceedClickFunction():
    if(not selectFile()):
        return
    print('proceed')
    if(os.system("reg import "+var.get())==0):
        success()
    else:
        fail()

def btnLoadClickFunction():
    print('select')
    var.set(tk.filedialog.askopenfilename())

root.geometry(str(W+20)+"x"+str(H+20))
#root.geometry('400x300')
root.title('Regeditor')

# File reg
loadBtn = tk.Button(root, text='Browse', command=btnLoadClickFunction)
loadBtn.place(x=5, y=5)
editBtn = tk.Button(root, text='Edit', command=btnEditClickFunction)
editBtn.place(x=200, y=30, width = 100)
proceedBtn= tk.Button(root, text='Import file', command=btnProceedClickFunction)
proceedBtn.place(x=60, y=30, width = 100)

### Path Key
pathLabel = tk.Label(root, text="Pathkey: ")
pathLabel.place(x=5, y=30+SIZE_ROW*2)
pathEntry = tk.Entry(root, bd =2)
pathEntry.place(x=60, y=30+SIZE_ROW*2, width = W-60, height = SIZE_ROW-10)

### Value
valueLabel = tk.Label(root, text="Value: ")
valueLabel.place(x=5, y=30+SIZE_ROW*3)
valueEntry = tk.Entry(root, bd =2)
valueEntry.place(x=60, y=30+SIZE_ROW*3, width = W-60, height = SIZE_ROW-10)
valueLabel.pack_forget()
valueEntry.pack_forget()

### Data
dataLabel = tk.Label(root, text="Data: ")
dataLabel.place(x=5, y=30+SIZE_ROW*4)
dataEntry = tk.Entry(root, bd =2)
dataEntry.place(x=60, y=30+SIZE_ROW*4, width = W-120, height = SIZE_ROW-10)
dataLabel.pack_forget()
dataEntry.pack_forget()

### Datatype menu
dataDictType = {
    'String':'REG_SZ',
    'Multi-String':'REG_MULTI_SZ',
    'DWORD':'REG_DWORD',
    'QWORD':'REG_QWORD',
    'Binary':'REG_BINARY',
    'Expandable String':'REG_EXPAND_SZ'
}
dataListType = []
[dataListType.append(k) for k, v in dataDictType.items()]
dttype = StringVar(root)
dttype.set(dataListType[0])
typeMenu = tk.OptionMenu(root, dttype, *dataListType)
typeMenu.place(x=W-60, y=20+SIZE_ROW*4)
action = ['Set value','Get value','Delete Value','Create key','Delete key']

def showAct(value):
    pass
    #if value=action[0]:

# Action menu
tk.Label(root, text="Action: ").place(x=5, y=30+SIZE_ROW)
actVar = StringVar(root)
actVar.set(action[0])
actMenu = tk.OptionMenu(root, actVar, *action, command=showAct)
actMenu.place(x=60, y=30+SIZE_ROW)


def converttostr(input_seq, seperator):
   final_str = seperator.join(input_seq)
   return final_str

realAction = ['add','query', 'delete','add','delete']
def btnCommandClickFunction():
    print("Test")
    if(pathEntry.get()==""):
        fail("Path key is null")
        return
    actNow = actVar.get()
    if actNow==action[0]:
        if(valueEntry.get()==""):
            fail("Value is null")
        else:
            command=["reg","add",pathEntry.get(),"/v",valueEntry.get(),"/t",dataDictType[dttype.get()],"/d",dataEntry.get(),"/f"]
    elif actNow==action[1]:
        print(actNow)
        if(valueEntry.get()==""):
            fail("Value is null")
        else:
            command=["reg","query",pathEntry.get(),"/v",valueEntry.get()]
            out = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            success(str(out).split()[-1].split('\\')[0])
    elif actNow==action[2]:
        if(valueEntry.get()==""):
            fail("Value is null")
        else:
            command=["reg","delete",pathEntry.get(),"/v",valueEntry.get(), "/f"]
    elif actNow==action[3]:
        command=["reg","add",pathEntry.get(),"/f"]
    else:
        command=["reg","delete",pathEntry.get(),"/f"]
    print(converttostr(command," "))
    if(os.system(converttostr(command," "))==0):
        success()
    else:
        fail()

tk.Button(root, text='Proceed command', command=btnCommandClickFunction).place(x=W-20-40-120, y=H-10)

def btnSendClickFunction():
    print("Send")
tk.Button(root, text='Send', command=btnSendClickFunction).place(x=W-20-40, y=H-10)

def btnQuitClickFunction():
    print('quit')
    root.destroy()
quitBtn = tk.Button(root, text='Quit ', command=btnQuitClickFunction)
quitBtn.place(x=W-20, y=H-10)

root.mainloop()