import socket
import datetime

# Status codes
SC_OK = 0
SC_UNRECOGNIZED_COMMAND = 3
SC_ERROR = 400
SC_PROCESS_NOT_RUNNING = 200
SC_PROCESS_KILL_REQUEST_IS_DENIED = 201
SC_PROCESS_CANNOT_KILL = 202
SC_PROCESS_NOT_FOUND = 203
SC_APP_NOT_RUNNING = 300
SC_APP_KILL_REQUEST_IS_DENIED = 301
SC_APP_CANNOT_KILL = 302
SC_APP_NOT_FOUND = 303
SC_MACHINE_CANNOT_SHUTDOWN = 500

STATUS_MESSAGES = {
    SC_OK: 'OK',
    SC_UNRECOGNIZED_COMMAND: 'Unrecognized command',
    SC_PROCESS_NOT_RUNNING: 'Process not running',
    SC_PROCESS_KILL_REQUEST_IS_DENIED: 'Kill request is denied',
    SC_PROCESS_CANNOT_KILL: 'Cannot kill process',
    SC_PROCESS_NOT_FOUND: 'Process not found',
    SC_APP_NOT_RUNNING: 'Application not running',
    SC_APP_KILL_REQUEST_IS_DENIED: 'Kill request is denied',
    SC_APP_CANNOT_KILL: 'Cannot kill application',
    SC_APP_NOT_FOUND: 'Application not found',
    SC_ERROR: 'Error',
    SC_MACHINE_CANNOT_SHUTDOWN: 'Cannot shutdown'
}

MESSAGE_ENCODING = 'utf-8'
SERVER_PORT = 9098
SOCKET_BUFFER = 1024

def decode(raw: bytes):
    """Decodes the raw message into different fields

    Args:
        raw (bytes): The raw message

    Returns:
        tuple: A tuple of (field1, field2, body)
    """
    r = raw.decode(MESSAGE_ENCODING).rstrip('\x00')
    header, body = tuple(r.split('\n', 1))
    field1, field2 = tuple(header.split(' ', 1))
    return field1, field2, body

def encode(message) -> bytes:
    """Converts a message into raw bytes

    Args:
        message (Message): A message

    Returns:
        bytes: An encoded message in bytes, ready to be sent to socket
    """
    header = ' '.join([message.field1, message.field2])
    m = '\n'.join([header, message.body])
    return m.encode(MESSAGE_ENCODING) + b'\x00'
    
class Message:
    """Represents a message sent from client to server (a request), and from
    server to client (a response)
    """

    def __init__(self, field1, field2, body):
        self.field1, self.field2, self.body = field1, field2, body
        
    def to_bytes(self) -> bytes:
        """Converts the message into bytes, ready to be sent to the socket

        Returns:
            bytes: An encoded message
        """
        # header = ' '.join([self.field1, self.field2])
        # m = '\n'.join([header, self.body])
        # return m.encode(MESSAGE_ENCODING) + b'\x00'
        return encode(self)

    @classmethod
    def from_bytes(cls, raw: bytes):
        field1, field2, body = decode(raw)
        return cls(field1, field2, body)


class Response(Message):
    """Represents a response from server
    """

    def __init__(self, status_code: int, content: str):
        super().__init__(str(status_code), STATUS_MESSAGES[status_code], content)

    def ok(self) -> bool:
        return self.status_code() != 0

    def status_code(self) -> int:
        return int(self.field1)

    def status_message(self) -> str:
        return STATUS_MESSAGES[self.status_code()]
    
    def content(self) -> str:
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
        status_code, _, body = decode(raw)
        return cls(int(status_code), body)


class Request(Message):
    """Represents a request from client
    """

    def __init__(self, command: str, option: str, content: str):
        super().__init__(command, option, content)

    def command(self) -> str:
        return self.field1

    def option(self) -> str:
        return self.field2

    def content(self) -> str:
        return self.body

    def __str__(self) -> str:
        return f'<Request [{self.command()} {self.option()}]>'


def send(s: socket.socket, message: Message):
    """Sends `message` to peer using socket `s`

    Args:
        s (socket.socket): A socket object
        message (Message): A message
    """
    s.sendall(message.to_bytes())

def receive(s: socket.socket) -> bytes:
    """Receives message from peer using socket `s`

    Args:
        s (socket.socket): A socket

    Returns:
        bytes: The message
    """
    message = b''
    while True:
        temp = s.recv(SOCKET_BUFFER)
        # TODO: handle the case of closed connection
        if not temp:
            break
        
        message += temp
        # This signals the end of the message
        if temp[-1] == 0:
            break
    return message
