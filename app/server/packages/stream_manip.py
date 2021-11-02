import app.core.protocol as protocol
from app.core.exceptions import SendingError

import base64
import ctypes
import logging
import lzma
from mss import mss
from PIL import Image
import socket
import threading
import time
from typing import Tuple

class StreamService:
    BBOX = {
        'top': 0,
        'left': 0,
        'width': ctypes.windll.user32.GetSystemMetrics(0),
        'height': ctypes.windll.user32.GetSystemMetrics(1),
    }

    def __init__(self):
        """Initializes stream service for peer

        Args:
            peer (tuple): Address of the peer (addr, port)
        """
        self.stream_socket = None

        self.is_streaming = False
        self.stop_signal = False
        self.SLEEP_BETWEEN_FRAMES = 0.2
        self.FRAME_SIZE = (480, 360)

    def is_running(self):
        return self.stream_socket is not None

    def connect_to_peer(self, peer_address) -> bool:
        try:
            self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_socket.connect((peer_address, protocol.VIDEO_STREAM_PORT))
            return True
        except Exception:
            self.stream_socket.close()
            self.stream_socket = None
            return False

    def capture_frame(self) -> Tuple[int, int, bytes]:
        """Captures one screenshot frame

        Returns:
            tuple: A 3-tuple of image's width, height, and raw
            bytes (in RBGA mode)
        """
        with mss() as s:
            screenshot = s.grab(self.BBOX)
            logging.debug('Captured frame')
            img = Image.frombytes(
                mode='RGBA',
                size=(screenshot.width, screenshot.height),
                data=screenshot.bgra,
            )
            img = img.resize(size=self.FRAME_SIZE, resample=Image.ANTIALIAS)
            logging.debug('Resized frame')
            return img.width, img.height, lzma.compress(img.tobytes())

    def send_frame(self):
        """Sends one screenshot frame to peer
        """

        status_code = 0
        data = b''

        w, h, frame = self.capture_frame()
        b64encoded = base64.urlsafe_b64encode(frame)
        logging.debug(f'Encoded frame using base64, frame size {len(b64encoded)}')
        data = b'\n'.join(
            [str(w).encode(protocol.MESSAGE_ENCODING), str(h).encode(protocol.MESSAGE_ENCODING), b64encoded]
        )

        response = protocol.Response(status_code, data)
        protocol.send(self.stream_socket, response)

    def send_terminate_frame(self):
        data = b'0\n0\n'
        protocol.send(self.stream_socket, protocol.Response(protocol.SC_OK, data))

    def start(self):
        """Continuously sends frames to peer until paused
        """
        self.is_streaming = True
        def stream():
            i = 0
            try:
                while not self.stop_signal:
                    while self.is_streaming:
                        self.send_frame()
                        logging.debug(f'Sent frame {i}...')
                        i += 1
                        time.sleep(self.SLEEP_BETWEEN_FRAMES)
                        logging.debug(f'Slept for {self.SLEEP_BETWEEN_FRAMES} second(s)')
                self.send_terminate_frame()
                self.stream_socket.close()
            except SendingError:
                self.stream_socket.close()
            finally:
                self.stream_socket = None

        stream_thread = threading.Thread(target=stream)
        stream_thread.start()

    def restart(self):
        """Restarts the stream
        """
        self.is_streaming = True

    def pause(self):
        """Pauses the stream
        """
        self.is_streaming = False

    def stop(self):
        """Stops the stream service
        """
        if self.is_running():
            self.pause()
            self.stop_signal = True
            time.sleep(2.0)
            if self.is_running():
                self.stream_socket.close()
                self.stream_socket = None
