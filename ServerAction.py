import ProcessRunning

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
        server_data = ProcessRunning.get_running_process()

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
    type of value in key: https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-rprn/25cce700-7fcf-4bb6-a2f3-0f6d08430a55
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
