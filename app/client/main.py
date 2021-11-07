from xml.etree.ElementTree import indent
from PyQt5 import uic
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QHeaderView, QInputDialog, QLineEdit, QMainWindow, QPushButton, QTabWidget, QTableView, QTableWidget, QTableWidgetItem, QWidget
from cv2 import NORM_HAMMING, sepFilter2D
from app.client.Data import Data
from app.client.packages.portal import *

class ClientFlow(QMainWindow):
    def __init__(self):
        super(ClientFlow, self).__init__()
        self.updateUIBeforeConnect()
        self.portal = Portal()
        self.aboutWindow = self.About(self)
        self.registryWindow = self.Registry(self.portal, self)
        self.data = Data()
        self.connectFunc()

    def updateUIAfterConnect(self):
        self.mac_addr.setText(self.data.mac_addr)

    def updateUIBeforeConnect(self):
        uic.loadUi('./ui/MainClient.ui', self)
        self.setFixedSize(901, 775)
        self.proc_list.setColumnWidth(0, 150)
        self.proc_list.setColumnWidth(1, 75)
        self.proc_list.setColumnWidth(3, 50)

    def run(self):
        self.show()

    def updateAfterConnect(self):
        self.get_mac()
        self.portal.keyboard_hook()
        self.updateUIAfterConnect()
        

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
        self.key_hook_btn.clicked.connect(self.portal.keyboard_hook)
        self.key_lock_btn.clicked.connect(self.portal.keyboard_lock)
        self.key_unlock_btn.clicked.connect(self.portal.keyboard_unlock)
        self.key_unhook_btn.clicked.connect(self.keylogger)
        self.key_print_btn.clicked.connect(self.keyloggerPrint)

        self.proc_get_btn.clicked.connect(self.showProcessList)
        self.proc_start_btn.clicked.connect(self.startProcess)
        self.proc_kill_btn.clicked.connect(self.killProcess)
        #self.proc_list.cellClicked.connect(self.cell_was_clicked)

        self.app_get_btn.clicked.connect(self.showAppList)
        self.app_start_btn.clicked.connect(self.startApp)
        self.app_kill_btn.clicked.connect(self.killApp)
        #self.app_list.cellClicked.connect(self.cell_was_clicked)
    def startApp(self):
        app_name = None
        try:
            text, ok = QInputDialog.getText(self, 'Input', 'App name')
            if ok:
                app_name = str(text)
            r = self.portal.start_app(app_name)
            self.statusbar.showMessage('Start app '+app_name+ ' -> '+ r.status_message())
        except:
            pass

    def killApp(self):
        # choose row to kill
        try:
            indexes = self.app_list.selectionModel().selectedRows()
            selected = None
            for index in sorted(indexes):
                selected = index.row()
            app = self.data.app[selected]
            r = self.portal.kill_app(app[1])
            self.statusbar.showMessage('Kill app '+ app[0] +' -> '+ r.status_message())
        except:
            self.statusbar.showMessage('Please choose a row to kill.')
    
    def showAppList(self):
        try:
            self.statusbar.showMessage('Show app list.')
            r = self.portal.list_apps()
            content = r.content().decode(protocol.MESSAGE_ENCODING)
            data = []
            content = content.split("\n")
            self.app_list.setRowCount(len(content))
            self.app_list.setColumnCount(3)
            for i in range(len(content)):
                row = content[i].split(",")
                for j in range(3):
                    self.app_list.setItem(i, j, QTableWidgetItem(row[j]))
                data.append(row)
            self.data.app = data
        except:
            self.statusbar.showMessage('Not connect server.')

    def startProcess(self):
        proc_name = None
        try:
            text, ok = QInputDialog.getText(self, 'Input', 'Process name')
            if ok:
                proc_name = str(text)
            r = self.portal.start_process(proc_name)
            self.statusbar.showMessage('Start process '+proc_name+ ' -> '+ r.status_message())
        except:
            pass

    # bug here cannot kill notepad
    def killProcess(self):
        # choose row to kill
        try:
            indexes = self.proc_list.selectionModel().selectedRows()
            selected = None
            for index in sorted(indexes):
                selected = index.row()
            proc = self.data.process[selected]
            r = self.portal.kill_process(proc[1]).status_message()
            print(r)
            self.statusbar.showMessage('Kill process '+ proc[0] +' -> '+ r)
        except:
            self.statusbar.showMessage('Please choose a row to kill.')
    
    def cell_was_clicked(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))

    def showProcessList(self):
        try:
            r = self.portal.list_processes()
            content = r.content().decode(protocol.MESSAGE_ENCODING)
            data = []
            content = content.split("\n")
            self.proc_list.setRowCount(len(content))
            self.proc_list.setColumnCount(3)
            for i in range(len(content)):
                row = content[i].split(",")
                for j in range(3):
                    self.proc_list.setItem(i, j, QTableWidgetItem(row[j]))
                data.append(row)
            self.data.process = data
            self.statusbar.showMessage('Show process list.')
        except:
            self.statusbar.showMessage('Not connect server.')


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

            self.dataDictType = {
                'String':'REG_SZ',
                'Multi-String':'REG_MULTI_SZ',
                'DWORD':'REG_DWORD',
                'QWORD':'REG_QWORD',
                'Binary':'REG_BINARY',
                'Expandable String':'REG_EXPAND_SZ'
            }

            type = self.dataDictType[type]
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
                self.status.setText(r.content().decode(protocol.MESSAGE_ENCODING)+" "+r.status_message())
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