from app.server.ui.ServerWindow import ServerWindow

from PyQt5.QtWidgets import QApplication
import sys

if __name__=="__main__":
    app = QApplication(sys.argv)
    login = ServerWindow()
    login.show()
    app.exec_()
