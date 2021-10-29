import getmac
import os
import socket

def shutdown(after=5):
    args = ['shutdown', '/s', '/t', str(after)]
    return os.system(' '.join(args)) == 0

# TODO: define logout function

def get_mac() -> str:
    """Gets MAC address, based on the IP address returned by socket

    Returns:
        str: Lowercase, colon-separated MAC address if success
        None: If fail
    """
    s = socket.gethostbyname(socket.gethostname())
    return getmac.get_mac_address(ip=s)
