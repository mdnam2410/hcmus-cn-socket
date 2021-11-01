import logging
import app.core.protocol as protocol

import base64
import cv2
import numpy as np
import lzma
from PIL import Image
import socket
import threading
from typing import Tuple

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
        
    def is_connected(self):
        return self.data_socket is not None

    def receive(self):
        """Receives frames from the server

        Returns:
            str: The content of the message from server
        """
        r = protocol.Response.from_bytes(protocol.receive(self.data_socket))
        return r.content()

    def __iter__(self) -> Tuple[int, int, bytes]:
        """Yields the frames received from server

        Returns:
            Tuple[int, int, bytes]: 

        Yields:
            Iterator[Tuple[int, int, bytes]]: A 3-tuple of (w, h, b), where
            w is the frame's width, h is the frame's height, and b is the
            frame's raw bytes (in RBGA mode)
        """
        while True:
            data =  self.receive()
            w, h, frame = tuple(data.split(b'\n', 2))
            frame = base64.urlsafe_b64decode(frame)
            frame = lzma.decompress(frame)
            yield int(w.decode(protocol.MESSAGE_ENCODING)), int(h.decode(protocol.MESSAGE_ENCODING)), frame


if __name__ == '__main__':
    vs = ScreenStream()
    for w, h, im in vs:
        print(w, h)
        img = Image.frombytes(
            mode='RGBA',
            size=(w, h),
            data=im,
        )
        cv2.imshow('show', np.array(img))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
