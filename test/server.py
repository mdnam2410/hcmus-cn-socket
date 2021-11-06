from app.server.packages.service import Service

import threading

if __name__ == '__main__':

    s = Service()
    def t(s):
        s.start()
    th = threading.Thread(target=t, args=(s,))
    th.start()

    i = input('> ')
    s.stop()

