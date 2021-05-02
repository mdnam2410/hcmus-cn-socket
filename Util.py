
def extract_message(message: bytes, message_type='client') -> tuple:
    message = message.decode('utf-8')
    
    # Extract necessary fields
    header_field, data_field = tuple(message.split('\n', 1))
    field1, field2 = tuple(header_field.split(' '))

    # field1 is Error code if this is a server message
    if type == 'server':
        field1 = int(field1)
    
    return (field1, field2, data_field)

def package_message(field1: str, field2: str, data: str) -> tuple:
    s = str(field1) + ' ' + field2 + '\n' + data
    return s.encode('utf-8')

error_message_dictionary = {
    0: 'OK',
    3: 'Unrecognized command',
    200: 'Process not running',
    201: 'Kill request is denied',
    202: 'Cannot kill process',
    203: 'Process not found',
    300: 'Application not running',
    301: 'Kill request is denied',
    302: 'Cannot kill application',
    303: 'Application not found'
}
