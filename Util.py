
def extract_message(message, message_type='client'):
    message = message.decode('utf-8')
    
    # Extract necessary fields
    header_field, data_field = tuple(message.split('\n', 1))
    field1, field2 = tuple(header_field.split(' '))

    # field1 is Error code if this is a server message
    if type == 'server':
        field1 = int(field1)
    
    return (field1, field2, data_field)

def package_message(field1, field2, data):
    s = str(field1) + ' ' + field2 + '\n' + data
    return s.encode('utf-8')

error_message_dictionary = {
    0: 'OK',
    3: 'Unrecognized command',
    200: 'Process not running',
    201: 'Cannot kill process'
}