import sys
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout
import app.server.packages.services as services
import app.server.packages.service as service
import app.core.ui as ui
import logging
import threading

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)

class ServerWindow(ui.Windows):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        logging.debug(f'Creating server UI')
        self.service = service.Service()
        layout = QVBoxLayout()

        self.start_btn = QPushButton("Start server")
        self.start_btn.clicked.connect(self.start)

        self.stop_btn = QPushButton("Stop client")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.hide()

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        
        self.setLayout(layout)
        self.setWindowTitle("Server")
        ui.loadIcon(self, 'SP_VistaShield')

    def start(self):
        print("Start")
        self.start_btn.hide()
        self.stop_btn.show()
        self.mainThread = threading.Thread(target=self.service.start)
        self.mainThread.start()
        pass

    # bug here
    # when stop it thread still open and however socket still open :)
    def stop(self):
        print("Stop")
        self.start_btn.show()
        self.stop_btn.hide()
        self.service.stop()
        pass

    def clean2exit(self):
        self.service.stop()
        return super().clean2exit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    login = ServerWindow()
    login.show()
    app.exec_()