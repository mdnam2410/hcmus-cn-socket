import io
import pyautogui
import wmi
from PIL import Image


def action_screenshot(option, data):
    error_code = 0

    img = pyautogui.screenshot()
    b = io.BytesIO()
    img.save(b, format='PNG')
    server_data = str(b.getvalue())

    return (error_code, server_data)

def action_process(option, data):
    error_code = 0
    server_data = ''

    if option == 'list':
        f = wmi.WMI()
        for process in f.Win32_Process():
            t = (process.ProcessID, process.Name, process.ThreadCount)
            server_data += f'{t[0]},{t[1]},{t[2]}\n'
        return (error_code, data)

    return (error_code, server_data)

def action_app(option, data):
    error_code = 0
    server_data = ''

    """Code here"""

    return (error_code, server_data)

def action_keylogging(option, data):
    error_code = 0
    server_data = ''

    """Code here"""

    return (error_code, server_data)


def action_reg(option, data):
    """
    Parameters
    ---------
    option : str
        One of the five command: 'send', 'get', 'set', 'delete', 'create', 'delete-key'

    data : str
        Depends on option:
            option = 'send':       the .reg file
            option = 'get':        the path the key to get value
            option = 'set':        a formatted string: <path to key>,<new value>
            option = 'delete':     the path to the key to delete value
            option = 'create':     the path to the new key to create
            option = 'delete-key': the path to the key to delete
    
    Returns
    -------
    error_code : int
    
    server_data : str
        If error_code == 0: server_data is empty
        Else depends on option:
            option = 'send':       empty
            option = 'get':        a formatted string: <key type>,<key value>
            option = 'set':        empty
            option = 'delete':     empty
            option = 'create':     empty
            option = 'delete-key': empty
    """
    error_code = 0
    server_data = ''

    """Code here"""

    return (error_code, server_data)

def action_shutdown(option, data):
    error_code = 0
    server_data = ''

    """ Code here"""

    return (error_code, server_data)
