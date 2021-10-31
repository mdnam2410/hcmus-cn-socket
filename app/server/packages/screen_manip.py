import app.core.protocol as protocol

import base64
import base64
import io
import pyautogui

def take_screenshot() -> str:
    """Takes a screenshot

    Returns:
        str: A base64-encoded string
    """
    img = pyautogui.screenshot()
    b = io.BytesIO()
    img.save(b, format='PNG')
    return base64.b64encode(b.getvalue()).decode('utf-8')
