import base64
import ctypes
import io
from mss import mss
from PIL import Image

FRAME_SIZE = (360, 240)

def take_screenshot() -> bytes:
    """Takes a screenshot

    Returns:
        bytes: A base64-encoded, JPEG-format image
    """
    try:
        bbox = {
            'top': 0,
            'left': 0,
            'width': ctypes.windll.user32.GetSystemMetrics(0),
            'height': ctypes.windll.user32.GetSystemMetrics(1),
        }
        screenshot = mss().grab(bbox)
        img = Image.frombytes(
            mode='RGB',
            size=(screenshot.width, screenshot.height),
            data=screenshot.rgb
        )
        img = img.resize(size=FRAME_SIZE, resample=Image.ANTIALIAS)

        jpeg = io.BytesIO()
        img.save(jpeg, format='JPEG', quality=95)
        return base64.urlsafe_b64encode(jpeg.getvalue())
    except Exception:
        return b''
