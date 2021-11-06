import base64
from app.client.packages.portal import Portal
import app.core.protocol as protocol

import cv2
import io
import logging
import numpy as np
from PIL import Image
import threading
import time

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    p = Portal()
    p.connect('127.0.0.1', protocol.SERVER_PORT)

    while True:
        c = input('> ')
        if c == 'exit':
            p.disconnect()
            break
        elif c == 'app list':
            q = p.list_apps()
            print(q.content())
        elif c == 'app kill':
            pid = int(input('PID to kill: '))
            r = p.kill_app(pid)
            print(r.status_message())
        elif c == 'mac':
            r = p.get_mac_address()
            print(r.content())
        elif c == 'process':
            r = p.list_processes()
            print(r.content())
        elif c == 'screenshot':
            r = p.get_screenshot()
            img = base64.urlsafe_b64decode(r.content())
            img = np.array(Image.open(io.BytesIO(img)))
            img = img[:, :, ::-1].copy()
            cv2.imshow('s', img)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        elif c == 'shutdown':
            r = p.shut_down()
            print(r.status_message())
        elif c == "sleep":
            r = p.sleep()
            print(r.status_message())
        elif c == "restart":
            r = p.restart()
            print(r.status_message())
        elif c == 'keyboard':
            while True:
                o = input('[hook|unhook|lock|unlock|exit]: ')
                if o == 'exit':
                    break
                elif o == 'hook':
                    r = p.keyboard_hook()
                elif o == 'unhook':
                    r = p.keyboard_unhook()
                elif o == 'lock':
                    r = p.keyboard_lock()
                    time.sleep(5)
                    p.keyboard_unlock()
                elif o == 'unlock':
                    r = p.keyboard_unlock()
                print(r.content())
        elif c == 'stream':
            r, vs = p.initialize_screen_stream()
            print(r.status_message())
            if vs is None:
                print('vs is none')
                continue

            def target(vs):
                for frame in vs:
                    f = Image.open(io.BytesIO(frame))
                    f = np.array(f)
                    f = f[:, :, ::-1].copy()
                    cv2.imshow('stream', f)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                print('Stream stop')
            t = threading.Thread(target=target, args=(vs,))
            t.start()

            while True:
                c = input('[start|restart|pause|stop]: ')
                if c == 'start':
                    p.start_stream()
                elif c == 'restart':
                    p.restart_stream()
                elif c == 'pause':
                    p.pause_stream()
                elif c == 'stop':
                    p.stop_stream()
                    break
        else:
            print('Unrecognized command')