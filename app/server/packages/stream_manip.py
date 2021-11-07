import app.core.protocol as protocol
from app.core.exceptions import SendingError

import base64
import ctypes
import io
import logging
import lzma
from mss import mss
from PIL import Image
import socket
import threading
import time

class StreamService:
    SCREEN_BOUNDING_BOX = {
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
        self.SLEEP_BETWEEN_FRAMES = 1/20
        #self.FRAME_SIZE = (720, 480)
        self.FRAME_SIZE = (360, 240)

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

    def capture_frame(self) -> bytes:
        """Captures one screenshot frame

        Returns:
            bytes: The frame in JPEG format
        """
        with mss() as s:
            logging.debug('Capturing frame')
            screenshot = s.grab(self.SCREEN_BOUNDING_BOX)
            img = Image.frombytes(
                mode='RGB',
                size=(screenshot.width, screenshot.height),
                data=screenshot.rgb,
            )

            logging.debug('Resizing frame')
            img = img.resize(size=self.FRAME_SIZE, resample=Image.ANTIALIAS)

            logging.debug('Saving frame to JPEG format')
            jpg = io.BytesIO()
            img.save(jpg, format='jpeg', quality=95)
            return jpg.getvalue()

    def send_frame(self):
        """Sends one screenshot frame to peer
        """

        status_code = protocol.SC_OK
        data = self.capture_frame()
        
        logging.debug('Compressing frame using LZMA')
        data = lzma.compress(data)
        logging.debug(f'Encoding frame using base64')
        data = base64.urlsafe_b64encode(data)

        logging.debug(f'Sending frame with size {len(data)} bytes')
        response = protocol.Response(status_code, data)
        protocol.send(self.stream_socket, response)

    def send_terminate_frame(self):
        data = b''
        protocol.send(self.stream_socket, protocol.Response(protocol.SC_OK, data))

    def start(self):
        """Continuously sends frames to peer until paused
        """
        self.is_streaming = True
        def stream():
            i = 0
            try:
                logging.debug('Starting streaming')
                while not self.stop_signal:
                    while self.is_streaming:
                        logging.debug(f'Sending frame {i}...')
                        self.send_frame()
                        i += 1
                        logging.debug(f'Sleeping for {self.SLEEP_BETWEEN_FRAMES} second(s)')
                        time.sleep(self.SLEEP_BETWEEN_FRAMES)
                
                logging.debug('Received stop signal, sending terminate frame...')
                self.send_terminate_frame()
            except SendingError:
                logging.debug('Error occured when sending frame, closing stream...')
                self.stop_signal = False
                self.is_streaming = False
            finally:
                self.stream_socket.close()
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
        self.stop_signal = False
