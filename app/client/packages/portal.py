import app.core.protocol as protocol
from app.core.exceptions import SendingError, ServerError, ReceivingError
from app.client.packages.screen_stream import ScreenStream

import socket
from typing import Tuple, Union


class Portal:
    """A wrapper for client socket, can send request and receive response from the server
    """
    
    def __init__(self):
        self.s = None
        self.connected = False

    def connect(self, addr, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((addr, port))
            self.connected = True
        except OSError as e:
            raise ServerError('Cannot connect to server') from e

    def disconnect(self):
        self.s.close()
        self.connected = False

    def is_connected(self):
        return self.connected
    
    def request(self, command, option, data) -> protocol.Response:
        if type(data) == str:
            data = data.encode(protocol.MESSAGE_ENCODING)
        try:
            req = protocol.Request(command, option, data)
            protocol.send(self.s, req)
            response = protocol.receive(self.s)
            return protocol.Response.from_bytes(response)
        except (SendingError, ReceivingError) as e:
            raise ServerError('Server is down') from e

    # ---- Screenshot and video stream ----

    def get_screenshot(self) -> protocol.Response:
        """Gets a screenshot from the server

        Returns:
            app.core.protocol.Response:
                On success, return the base64-encoded, JPEG-format image

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('screenshot', '', '')

    def initialize_screen_stream(self) -> Tuple[protocol.Response, Union[ScreenStream, None]]:
        """Initializes the screen stream service

        Returns:
            tuple: A 2-tuple of (response, screenstream). `screenstream` is None if
            the initialization is fail.
        
        Raises:
            app.core.exceptions.ServerError
        """
        vs = ScreenStream(self.s.getsockname()[0])
        response = self.request('stream', '', '')
        if not response.ok():
            vs = None
        return (response, vs)

    def start_stream(self) -> protocol.Response:
        """Starts streaming

        Once called, the associated ScreenStream object will start receiving
        frames from the server. Please call this function only once.

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('stream', 'start', '')

    def restart_stream(self) -> protocol.Response:
        """Restarts the stream

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('stream', 'restart', '')

    def pause_stream(self) -> protocol.Response:
        """Pauses the stream
        
        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('stream', 'pause', '')

    def stop_stream(self) -> protocol.Response:
        """Stops the stream

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('stream', 'stop', '')


    # ---- Processes and apps ----

    def list_processes(self) -> protocol.Response:
        """Gets a list of running processes on the server machine

        Returns:
            `app.core.protocol.Response`: On success, return a  `bytes` object with
            comma-separated value of <process id>,<thread count>,<description>.

            For example:
            1,1,system.exe\n
            2,1,login.exe\n
            ...

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('process', 'list', '')

    def start_process(self, process_name: str) -> protocol.Response:
        """Starts a process given its name

        Args:
            process_name (str): Process name

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('process', 'start', process_name)

    def kill_process(self, pid: int) -> protocol.Response:
        """Kills a process

        Args:
            pid (int): Process ID

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('process', 'kill', str(pid))

    def list_apps(self) -> protocol.Response:
        """Lists the running applications on the server

        Returns:
            app.core.protocol.Response: The same as `Portal.list_processes`

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('app', 'list', '')

    def start_app(self, app_name: str) -> protocol.Response:
        """Starts an app

        Args:
            app_name (str): The app's name

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('app', 'start', app_name)

    def kill_app(self, pid: int) -> protocol.Response:
        """Kills an app

        Args:
            pid (int): The app's ID

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('app', 'kill', str(pid))


    # ---- Keylogging ----

    def keyboard_hook(self) -> protocol.Response:
        """Starts hooking

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('keylogging', 'hook', '')
    
    def keyboard_unhook(self) -> protocol.Response:
        """Unhooks

        Returns:
            app.core.protocol.Response: On success return a string of
            keys hooked previously

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('keylogging', 'unhook', '')

    def keyboard_lock(self):
        """Locks the keyboard

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('keylogging', 'lock', '')

    def keyboard_unlock(self):
        """Unlocks the keyboard

        No effect if the keyboard is not locked already.

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('keylogging', 'unlock', '')


    # ---- Registry manipulation ----

    def send_registry_file(self, registry_file: str) -> protocol.Response:
        """Sends a registry file (in text form)

        Args:
            registry_file (str): The content of the file

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('reg', 'send', registry_file)

    def _registry_wrapper(self, command, option, key, value='', data_type='', new_data=''):
        body = ','.join([key, value, data_type, new_data])
        print(body)
        return self.request(command, option, body)

    def get_registry(self, key, value) -> protocol.Response:
        """Gets the value of the registry

        Args:
            key (str): Path to key
            value (str): Value name

        Returns:
            app.core.protocol.Response: On success, returns the data of the
            registry

        Raises:
            app.core.exceptions.ServerError
        """
        return self._registry_wrapper('reg', 'get', key, value)

    def set_registry(self, key: str, value: str, data_type: str, new_data: str) -> protocol.Response:
        """Sets new value for the registry

        Args:
            key (str): Path to registry
            value (str): Value name
            data_type (str): Must be one of 'REG_SZ', 'REG_MULTI_SZ',
            'REG_DWORD', 'REG_QWORD', 'REG_BINARY', 'REG_EXPAND_SZ'
            new_data (str): New data

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self._registry_wrapper('reg', 'set', key, value, data_type, new_data)

    def delete_registry(self, key: str, value: str) -> protocol.Response:
        """Deletes a registry

        Args:
            key (str): Path to key
            value (str): Value name

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self._registry_wrapper('reg', 'delete', key, value)

    def create_registry_key(self, key: str) -> protocol.Response:
        """Creates a new registry key

        Args:
            key (str): Path to new key

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self._registry_wrapper('reg', 'create-key', key)

    def delete_registry_key(self, key: str) -> protocol.Response:
        """Deletes a registry key

        Args:
            key (str): Path to key

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self._registry_wrapper('reg', 'delete-key', key)
    
    
    # ---- Machine ----

    def shut_down(self) -> protocol.Response:
        """Shuts the server down

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('machine', 'shutdown', '')

    def log_out(self) -> protocol.Response:
        """Logs out

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError        
        """
        self.request('machine', 'log-out', '')

    def sleep(self) -> protocol.Response:
        """Sleep the server machine

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('machine', 'sleep', '')

    def restart(self) -> protocol.Response:
        """Restart the server machine

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('machine', 'restart', '')

    def get_mac_address(self) -> protocol.Response:
        """Gets MAC address

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('machine', 'mac', '')

    # ---- File system ----

    def get_list_F(self, path: str = "disk") -> protocol.Response:
        """Gets list file and folder

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('file', 'list', path)

    def get_file(self, path: str, name_file: str = None) -> protocol.Response:
        """Download file

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('file', 'down', ', '.join([path, name_file]))

    def rename_F(self, path: str, old_name: str = None, new_name: str = None) -> protocol.Response:
        """Rename file or folder

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('file', 'rename', ', '.join([path, old_name, new_name]))

    def send_file(self, path: str, dest_name: str, data_file: str) -> protocol.Response:
        """Upload file

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('file', 'send', ', '.join([path, dest_name, data_file]))

    def delete_file(self, path: str) -> protocol.Response:
        """Delete file

        Returns:
            app.core.protocol.Response

        Raises:
            app.core.exceptions.ServerError
        """
        return self.request('file', 'del', path)

if __name__ == '__main__':
    # First, create a protal object
    portal = Portal()

    # Connect to server when ready
    portal.connect('127.0.0.1', protocol.SERVER_PORT)

    # Make a request to the server. Each response will have a status code
    # a status message and a response content
    response = portal.get_screenshot()

    # No error
    response.ok()

    # Retrieve status code and message here
    response.status_code()
    response.status_message()

    # The response content returned is always a string, but its format is
    # different for each request. Refer to the each request function
    # documentation string.
    response.content()
