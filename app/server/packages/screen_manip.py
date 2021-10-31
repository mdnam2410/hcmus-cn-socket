import app.core.protocol as protocol

import base64
import base64
import io
import pyautogui

def take_screenshot() -> bytes:
    """Takes a screenshot

    Returns:
        bytes: A base64-encoded byte string
    """
    img = pyautogui.screenshot()
    b = io.BytesIO()
    img.save(b, format='PNG')
    return base64.urlsafe_b64encode(b.getvalue())
