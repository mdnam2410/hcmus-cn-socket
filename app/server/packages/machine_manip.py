import getmac
import os
import socket

def shutdown(after=5):
    args = ['shutdown', '/s', '/t', str(after)]
    return os.system(' '.join(args)) == 0

def logout():
    args = ['shutdown', '/l']
    return os.system(' '.join(args)) == 0

def sleep():
    args = ['rundll32.exe powrprof.dll, SetSuspendState Sleep']
    return os.system(' '.join(args)) == 0

def restart():
    args = ['shutdown', '/r']
    return os.system(' '.join(args)) == 0

def get_mac() -> str:
    """Gets MAC address, based on the IP address returned by socket

    Returns:
        str: Lowercase, colon-separated MAC address if success
        None: If fail
    """
    s = socket.gethostbyname(socket.gethostname())
    return getmac.get_mac_address(ip=s)
