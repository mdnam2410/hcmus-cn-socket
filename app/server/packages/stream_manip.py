import app.core.protocol as protocol

import base64
import ctypes
import logging
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

    def __init__(self, peer):
        """Initializes stream service for peer

        Args:
            peer (tuple): Address of the peer (addr, port)
        """

        self.peer = peer
        self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_streaming = False
        self.stop_signal = False
        self.sleep_between_frames = 0.3
        self.FRAME_SIZE = (480, 360)

    def connect_to_peer(self):
        self.stream_socket.connect(self.peer)

    def capture_frame(self) -> Tuple[int, int, bytes]:
        """Captures one screenshot frame

        Returns:
            Tuple[int, int, bytes]: A 3-tuple of image's width, height, and raw
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
            return img.width, img.height, img.tobytes()

    def send_frame(self):
        """Sends one screenshot frame to peer
        """

        status_code = 0
        data = ''

        w, h, frame = self.capture_frame()
        im_to_str = base64.urlsafe_b64encode(frame).decode('utf-8')
        logging.debug(f'Encoded frame using base64, frame size {len(im_to_str)}')
        data = '\n'.join([str(w), str(h), im_to_str])

        response = protocol.Response(status_code, data)
        protocol.send(self.stream_socket, response)

    def start(self):
        """Continuously sends frames to peer until paused
        """
        if self.is_streaming:
            logging.debug('Stream is already started')
            return
        self.is_streaming = True
        def stream():
            i = 0
            while not self.stop_signal:
                while self.is_streaming:
                    self.send_frame()
                    logging.debug(f'Sent frame {i}...')
                    i += 1
                    time.sleep(self.sleep_between_frames)
                    logging.debug(f'Slept for {self.sleep_between_frames} second(s)')

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
        self.pause()
        self.stop_signal = True
