from os import abort
from PyQt5 import uic
import sys
from PyQt5.QtGui import QColor, QPalette

from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QWidget
import app.core.ui as ui
from app.client.packages.portal import *
class ClientFlow(QMainWindow):
    def __init__(self):
        super(ClientFlow, self).__init__()
        uic.loadUi('./ui/MainClient.ui', self)
        self.portal = Portal()
        self.connectFunc()
        self.aboutWindow = self.About(self)


    def run(self):
        self.show()

    def connectFunc(self):
        self.actionConnect.triggered.connect(lambda: self.portal.connect(*self.parseServerAddress()))
        self.connect_btn.clicked.connect(lambda: self.portal.connect(*self.parseServerAddress()))
        # when it disconnect the port will be in time wait state by TCP
        self.disconnect_btn.clicked.connect(self.disconnectServer)
        self.actionDisconnect.triggered.connect(self.disconnectServer)
        self.actionAbout.triggered.connect(self.about)


    class About(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setParent(parent)
            uic.loadUi('./ui/About.ui', self)
            self.setWindowModality(1)
            self.hide()

        def t(self):
            print("hmm")

    def about(self):
        self.statusbar.showMessage('Info about this application.')
        self.aboutWindow.show()

    def disconnectServer(self):
        self.ip_server.setEnabled(1)
        self.port_server.setEnabled(1)
        # maybe not have socket --> use try
        try:
            self.portal.disconnect()
            print("h")
        except:
            pass

    def parseServerAddress(self):
        ip = self.ip_server.text()
        self.ip_server.setDisabled(1)
        port = self.port_server.text()
        self.port_server.setDisabled(1)
        return ip, int(port)

if __name__=="__main__":
    app = QApplication(sys.argv)
    client = ClientFlow()
    client.run()
    app.exec_()