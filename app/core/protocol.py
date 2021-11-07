from app.core.exceptions import SendingError, ReceivingError

import socket
from typing import Tuple

# Status codes
SC_OK = 0
SC_ERROR_SERVER_NOT_RUNNING = 1
SC_ERROR_SERVER_SHUTDOWN = 2
SC_ERROR_UNRECOGNIZED_COMMAND = 3
SC_ERROR_UNKNOWN = 4
SC_SCREENSHOT_CANNOT_TAKE = 100
SC_PROCESS_NOT_RUNNING = 200
SC_PROCESS_KILL_REQUEST_IS_DENIED = 201
SC_PROCESS_CANNOT_KILL = 202
SC_PROCESS_NOT_FOUND = 203
SC_APP_NOT_RUNNING = 300
SC_APP_KILL_REQUEST_IS_DENIED = 301
SC_APP_CANNOT_KILL = 302
SC_APP_NOT_FOUND = 303
SC_STREAM_CANNOT_INITIALIZE = 400
SC_STREAM_SERVICE_ALREADY_INITIALIZED = 401
SC_STREAM_IS_NOT_RUNNING = 402
SC_MACHINE_CANNOT_SHUTDOWN = 500
SC_MACHINE_CANNOT_LOGOUT = 501
SC_MACHINE_CANNOT_SLEEP = 502
SC_MACHINE_CANNOT_RESTART = 503
SC_MACHINE_CANNOT_GET_MAC = 504
SC_REGISTRY_CANNOT_IMPORT_FILE = 600
SC_REGISTRY_CANNOT_GET_VALUE = 601
SC_REGISTRY_CANNOT_SET_VALUE = 602
SC_REGISTRY_CANNOT_DELETE_VALUE = 603
SC_REGISTRY_CANNOT_CREATE_KEY = 604
SC_REGISTRY_CANNOT_DELETE_KEY = 605

STATUS_MESSAGES = {
    SC_OK: 'OK',
    SC_ERROR_UNRECOGNIZED_COMMAND: 'Unrecognized command',
    SC_ERROR_UNKNOWN: 'Unknown error',
    SC_PROCESS_NOT_RUNNING: 'Process not running',
    SC_PROCESS_KILL_REQUEST_IS_DENIED: 'Kill request is denied',
    SC_PROCESS_CANNOT_KILL: 'Cannot kill process',
    SC_PROCESS_NOT_FOUND: 'Process not found',
    SC_APP_NOT_RUNNING: 'Application not running',
    SC_APP_KILL_REQUEST_IS_DENIED: 'Kill request is denied',
    SC_APP_CANNOT_KILL: 'Cannot kill application',
    SC_APP_NOT_FOUND: 'Application not found',
    SC_STREAM_CANNOT_INITIALIZE: "Cannot initialize stream",
    SC_STREAM_SERVICE_ALREADY_INITIALIZED: "Stream service is already initialized",
    SC_STREAM_IS_NOT_RUNNING: "Stream service is not running",
    SC_MACHINE_CANNOT_SHUTDOWN: 'Cannot shutdown',
    SC_MACHINE_CANNOT_LOGOUT: 'Cannot log out',
    SC_MACHINE_CANNOT_GET_MAC: 'Cannot get MAC address',
    SC_REGISTRY_CANNOT_IMPORT_FILE: "Cannot import registry file",
    SC_REGISTRY_CANNOT_GET_VALUE: "Cannot get value",
    SC_REGISTRY_CANNOT_SET_VALUE: "Cannot set value",
    SC_REGISTRY_CANNOT_DELETE_VALUE: "Cannot delete value",
    SC_REGISTRY_CANNOT_CREATE_KEY: "Cannot create key",
    SC_REGISTRY_CANNOT_DELETE_KEY: "Cannot delete key",
    SC_SCREENSHOT_CANNOT_TAKE: "Cannot take screenshot",
}

MESSAGE_ENCODING = 'utf-8'
SERVER_PORT = 9098
SOCKET_BUFFER = 1024
VIDEO_STREAM_PORT = 9890
VIDEO_STREAM_BUFFER = 32768

def split_fields(raw: bytes) -> Tuple[bytes, bytes, bytes]:
    """Splits the raw array of bytes into different fields

    Args:
        raw (bytes): The raw message

    Returns:
        tuple: A tuple of (field1, field2, body)
    """
    r = raw.rstrip(b'\x00')
    header, body = tuple(r.split(b'\n', 1))
    field1, field2 = tuple(header.split(b' ', 1))
    return field1, field2, body

def join_fields(field1: bytes, field2: bytes, body: bytes) -> bytes:
    """Joins different fields into raw bytes

    Args:
        message (Message): A message

    Returns:
        bytes: An encoded message in bytes, ready to be sent to socket
    """
    header = b' '.join([field1, field2])
    m = b'\n'.join([header, body])
    return m + b'\x00'
    
class Message:
    """Represents a message sent from client to server (a request), and from
    server to client (a response)
    """

    def __init__(self, field1: bytes, field2: bytes, body: bytes):
        self.field1, self.field2, self.body = field1, field2, body
        
    def to_bytes(self) -> bytes:
        """Converts the message into bytes, ready to be sent to the socket

        Returns:
            bytes: An encoded message
        """
        # header = ' '.join([self.field1, self.field2])
        # m = '\n'.join([header, self.body])
        # return m.encode(MESSAGE_ENCODING) + b'\x00'
        return join_fields(self.field1, self.field2, self.body)

    @classmethod
    def from_bytes(cls, raw: bytes):
        field1, field2, body = split_fields(raw)
        return cls(field1, field2, body)


class Response(Message):
    """Represents a response from server
    """

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            field1=str(status_code).encode(MESSAGE_ENCODING),
            field2=STATUS_MESSAGES[status_code].encode(MESSAGE_ENCODING),
            body=content,
        )

    def ok(self) -> bool:
        return self.status_code() == SC_OK

    def status_code(self) -> int:
        return int(self.field1.decode(MESSAGE_ENCODING))

    def status_message(self) -> str:
        return self.field2.decode(MESSAGE_ENCODING)
    
    def content(self) -> bytes:
        return self.body

    def __str__(self):
        return f'<Response [{self.status_code()}]>'

    @classmethod
    def from_bytes(cls, raw: bytes):
        """Parses a raw byte string

        Args:
            raw (bytes): Raw data

        Returns:
            Response: A response
        """
        status_code, _, body = split_fields(raw)
        return cls(int(status_code.decode(MESSAGE_ENCODING)), body)


class Request(Message):
    """Represents a request from client
    """

    def __init__(self, command: str, option: str, content: bytes):
        super().__init__(
            command.encode(MESSAGE_ENCODING),
            option.encode(MESSAGE_ENCODING),
            content
        )

    def command(self) -> str:
        return self.field1.decode(MESSAGE_ENCODING)

    def option(self) -> str:
        return self.field2.decode(MESSAGE_ENCODING)

    def content(self) -> bytes:
        return self.body

    def __str__(self) -> str:
        return f'<Request [{self.command()} {self.option()}]>'

    @classmethod
    def from_bytes(cls, raw: bytes):
        field1, field2, body = split_fields(raw)
        return cls(field1.decode(MESSAGE_ENCODING), field2.decode(MESSAGE_ENCODING), body)


def send(s: socket.socket, message: Message):
    """Sends `message` to peer using socket `s`

    Args:
        s (socket.socket): A socket object
        message (Message): A message

    Raises:
        app.core.exceptions.SendingError
    """
    try:
        s.sendall(message.to_bytes())
    except OSError as e:
        raise SendingError from e

def receive(s: socket.socket, buffer=SOCKET_BUFFER) -> bytes:
    """Receives message from peer using socket `s`

    Args:
        s (socket.socket): A socket
        buffer (int): Default to SOCKET_BUFFER

    Returns:
        bytes: The message

    Raises:
        app.core.exceptions.ReceivingError
    """
    message = bytearray()
    while True:
        try:
            temp = s.recv(buffer)
        except OSError as e:
            raise ReceivingError from e

        if not temp:
            raise ReceivingError
        
        message += temp
        # This signals the end of the message
        if temp[-1] == 0:
            break
    return bytes(message)
