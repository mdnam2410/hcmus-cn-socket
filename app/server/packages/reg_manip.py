import subprocess
import os

# Depricated, used for reference only
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

def import_file(content):
    temp_file = 'recv.reg'
    with open(temp_file, 'w') as f:
        f.write(content)
    args = ['reg', 'import', temp_file]
    return os.system(' '.join(args)) == 0

def get(key, value):
    args = ['reg', 'query', key, '/v', value]
    try:
        r = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
        r = r.decode().split()[-1].split('\\')[0]
        return r
    except subprocess.CalledProcessError:
        return None

def set(key, value, type, data):
    data_type_dict = {
        'String':'REG_SZ',
        'Multi-String':'REG_MULTI_SZ',
        'DWORD':'REG_DWORD',
        'QWORD':'REG_QWORD',
        'Binary':'REG_BINARY',
        'Expandable String':'REG_EXPAND_SZ'
    }
    args = ['reg', 'add', key, '/v', value, '/t', data_type_dict[type], '/d', data, '/f']
    return os.system(' '.join(args)) == 0

def delete(key, value):
    args = ['reg', 'delete', key, '/v', value, '/f']
    return os.system(' '.join(args)) == 0

def create_key(key):
    args = ['reg', 'add', key, '/f']
    return os.system(' '.join(args)) == 0

def delete_key(key):
    args = ['reg', 'delete', key, '/f']
    return os.system(' '.join(args)) == 0
