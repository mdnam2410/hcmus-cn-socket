import ServerAction as svac
import Util

import socket
import threading
import tkinter as tk

class Server:
    def __init__(self):
        self.SERVER_PORT = 9098
        self.SERVER_ADDRESS = socket.gethostbyname(socket.gethostname())

        # Listening socket
        self.s = None
        # Socket used to communicate with the client
        self.client_connection = None

        # Main window
        self.root = tk.Tk()
        self.root.geometry('100x100')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Button
        self.btn_open_server = tk.Button(self.root, text='Open server', command=self.start)
        self.btn_open_server.pack(padx=5, pady=5, ipadx=5, ipady=5, fill='both')

    def mainloop(self):
        """Start the server application window
        """
        self.root.mainloop()

    def on_closing(self):
        self.close()
        self.root.destroy()

    def start(self):
        """Create a socket and start listening
        """

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.SERVER_ADDRESS, self.SERVER_PORT))
        self.s.listen()

        self.t = threading.Thread(target=self.communicate, args=(self.client_connection,))
        self.t.start()

        self.btn_open_server.configure(text='Close server', command=self.close)

    def close(self):
        """Close the listening socket and the socket communicating with the client (if any)
        """

        if self.client_connection is not None:
            self.client_connection.close()
        if self.s is not None:
            self.s.close()
        self.btn_open_server.configure(text='Open server', command=self.start)

    def communicate(self, client_connection):
        """Accept and communicate with the client
        """

        try:
            client_connection, _ = self.s.accept()
            while True:
                client_message = client_connection.recv(2 ** 16)
                if len(client_message) == 0:
                    client_connection.close()
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
                    client_connection.send(server_message)
        except Exception:
            pass


server = Server()
server.mainloop()
