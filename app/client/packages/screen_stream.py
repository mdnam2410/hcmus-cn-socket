import app.core.protocol as protocol
from app.core.exceptions import ReceivingError, ServerError

import base64
import binascii
import logging
import lzma
import socket
import threading

class ScreenStream:
    def __init__(self):
        """Initializes the screen stream object

        This object should be created before sending the video stream request
        to the server. The ScreenStream object will wait for connection from
        the server, receive the frames and deliver back to the client.
        """
        self.addr = ('127.0.0.1', protocol.VIDEO_STREAM_PORT)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind(self.addr)
        self.data_socket = None

        self._wait()

    def _wait(self):
        def t(self):
            self.listen_socket.listen()
            self.data_socket, _ = self.listen_socket.accept()
        wait_thread = threading.Thread(target=t, args=(self,))
        wait_thread.start()
        
    def _receive(self):
        """Receives frames from the server

        Returns:
            bytes: The content of the message from server

        Raises:
            app.core.exceptions.ReceivingError
        """
        r = protocol.Response.from_bytes(protocol.receive(self.data_socket))
        return r.content()

    def is_connected(self):
        return self.data_socket is not None

    def __iter__(self) -> bytes:
        """Yields the frames received from server

        Yields:
            bytes: The frame in JPEG format

        Raises:
            app.core.exceptions.ServerError
        """
        try:
            while True:
                data =  self._receive()
                frame = data
                # w, h = int(w.decode(protocol.MESSAGE_ENCODING)), int(h.decode(protocol.MESSAGE_ENCODING))
                if not frame:
                    break
                try:
                    frame = base64.urlsafe_b64decode(frame)
                    frame = lzma.decompress(frame)
                    yield frame
                except (lzma.LZMAError, Exception):
                    logging.debug('Error in decompressing, skipping frame...')
                    pass
                except binascii.Error:
                    logging.debug('Error in decoding frame using base64, skipping frame...')
                    pass
        except ReceivingError:
            raise ServerError('Stream is broken')
        finally:
            self.listen_socket.close()
            self.data_socket.close()
