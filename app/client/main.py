import base64
import io
from os import path
import threading
from xml.etree.ElementTree import ProcessingInstruction, indent
from PIL import Image
from PyQt5 import uic
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
import numpy as np

from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QHeaderView, QInputDialog, QLineEdit, QMainWindow, QPushButton, QTabWidget, QTableView, QTableWidget, QTableWidgetItem, QWidget
from cv2 import NORM_HAMMING, sepFilter2D
import cv2
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
        self.app_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.proc_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        header = self.file_list.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def run(self):
        self.show()

    def updateAfterConnect(self):
        self.get_mac()
        self.file_view()
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
        self.actionShowProc.triggered.connect(self.showProcessList)
        self.actionStartProc.triggered.connect(self.startProcess)
        self.actionKillProc.triggered.connect(self.killProcess)
        

        self.app_get_btn.clicked.connect(self.showAppList)
        self.app_start_btn.clicked.connect(self.startApp)
        self.app_kill_btn.clicked.connect(self.killApp)
        #self.app_list.cellClicked.connect(self.cell_was_clicked)
        self.actionShowApp.triggered.connect(self.showAppList)
        self.actionStartApp.triggered.connect(self.startApp)
        self.actionKillApp.triggered.connect(self.killApp)

        self.screenshot_btn.clicked.connect(self.screenshot)
        self.actionTake.triggered.connect(self.screenshot)
        self.actionSave.triggered.connect(self.save_img)

        self.stream_btn.clicked.connect(self.stream)
        self.actionStart_stream.triggered.connect(self.stream)
        self.stop_stream_btn.clicked.connect(self.stop_stream)
        self.actionStop_stream.triggered.connect(self.stop_stream)

        self.actionViewFile.triggered.connect(self.file_view)
        self.file_get_btn.clicked.connect(self.file_view)
        self.file_back_btn.clicked.connect(self.file_view_previous)

        self.file_rename_btn.clicked.connect(self.file_rename)
        self.file_down_btn.clicked.connect(lambda: self.portal.get_file())
        self.file_upload_btn.clicked.connect(self.file_send)
        self.file_del_btn.clicked.connect(self.file_delete)

        self.file_list.cellClicked.connect(self.file_cell_was_clicked)
        self.file_list.doubleClicked.connect(self.file_view_advanced)

    def file_delete(self):
        path = self.data.path[-1] + self.data.currentF
        self.portal.delete_file(path)

    def file_cell_was_clicked(self, row, column):
        #print("Row %d and Column %d was clicked" % (row, column))
        self.data.currentF = self.data.listF[-1][row].strip()
        print("Selected: "+self.data.currentF)

    def file_send(self):
        self.statusbar.showMessage("Open file")
        try:
            file_name = QFileDialog.getOpenFileName()[0]
            print(file_name)
            new_name = None
            cnt = open(file_name).read()
            text, ok = QInputDialog.getText(self, 'Input', 'New name')
            if ok:
                new_name = str(text)
            r = self.portal.send_file(self.data.path[-1], new_name, cnt)
            self.statusbar.showMessage(r.status_message())
        except:
            pass

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def file_view_advanced(self, index):
        row = index.row()
        self.pathFile.setText(self.data.path[-1]+self.data.listF[-1][row].strip())
        self.file_view()

    def file_rename(self):
        new_name = None
        try:
            text, ok = QInputDialog.getText(self, 'Input', 'New name')
            if ok:
                new_name = str(text)
            print(self.data.path[-1], self.data.currentF ,new_name)
            r = self.portal.rename_F(self.data.path[-1], self.data.currentF ,new_name)
            self.statusbar.showMessage(r.status_message())
        except:
            self.statusbar.showMessage('Not connect server.')
    
    def file_choose(self) -> str:
        pass

    def file_view_previous(self):
        if len(self.data.path) > 1:
            self.data.path.pop()
            path = self.data.path[-1]
            self.pathFile.setText(path)
            self.data.listF.pop()
            data = self.data.listF[-1]
            self.file_list.setRowCount(len(data))
            self.file_list.setColumnCount(1)
            for i in range(len(data)):
                item = QTableWidgetItem(data[i])
                item.setFlags(Qt.ItemIsEnabled)
                self.file_list.setItem(0, i, item)

    def file_view(self):
        try:
            self.statusbar.showMessage('Show file list.')
            path = self.pathFile.text()
            r = None
            if path == "":
                r = self.portal.get_list_F("disk")
            else:
                r = self.portal.get_list_F(path)
            data = r.content().decode(protocol.MESSAGE_ENCODING).split(',')
            self.file_list.setRowCount(len(data))
            self.file_list.setColumnCount(1)
            for i in range(len(data)):
                item = QTableWidgetItem(data[i])
                item.setFlags(Qt.ItemIsEnabled)
                self.file_list.setItem(0, i, item)
            self.data.path.append(path)
            self.data.listF.append(data)
        except:
            pass

    def save_img(self):
        try:
            path = QFileDialog.getSaveFileName(caption="Save file", filter="*.jpeg")[0]
            self.data.image.save(path)
            #self.original_image.save(path)
        except:
            # Ignore exceptions raised by filedialog
            pass
        pass
    
    def stop_stream(self):
        self.stream_btn.setEnabled(1)
        self.actionStart_stream.setEnabled(1)
        # bug here
        self.portal.stop_stream()

    def stream(self):
        r, vs = self.portal.initialize_screen_stream()
        self.statusbar.showMessage(r.status_message())
        if vs is None:
            print('vs is none')
            pass

        def target(vs):
            for frame in vs:
                img = np.array(Image.open(io.BytesIO(frame)))
                img = img[:, :, ::-1].copy()
                img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                self.image.setPixmap(QtGui.QPixmap.fromImage(img))
                self.data.image = img
            print('Stream stop')

        t = threading.Thread(target=target, args=(vs,))
        t.start()
        self.portal.start_stream()
        self.stream_btn.setDisabled(1)
        self.actionStart_stream.setDisabled(1)
        
        

    def screenshot(self):
        try:
            r =self.portal.get_screenshot()
            img = base64.urlsafe_b64decode(r.content())
            self.data.image = Image.open(io.BytesIO(img))
            # Resize here to make save file more quality and future feature: open stream, screenshot external
            #img = img.resize(size=(360, 240), resample=Image.ANTIALIAS)
            img = np.array(self.data.image)
            img = img[:, :, ::-1].copy()
            img = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.image.setPixmap(QtGui.QPixmap.fromImage(img))
        except:
            self.statusbar.showMessage('Not connect server.')

    def startApp(self):
        app_name = None
        try:
            text, ok = QInputDialog.getText(self, 'Input', 'App name')
            if ok:
                app_name = str(text)
            r = self.portal.start_app(app_name)
            self.statusbar.showMessage('Start app '+app_name+ ' -> '+ r.status_message())
        except:
            self.statusbar.showMessage('Not connect server.')

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
                    item = QTableWidgetItem(row[j])
                    item.setFlags(Qt.ItemIsEnabled)
                    self.app_list.setItem(i, j, item)
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
            self.statusbar.showMessage('Not connect server.')

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
                    item = QTableWidgetItem(row[j])
                    item.setFlags(Qt.ItemIsEnabled)
                    self.proc_list.setItem(i, j, item)
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