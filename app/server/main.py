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
        # chưa tạo được icon connect
        self.start_btn.setGeometry(0, 0, 100, 50)
        self.start_btn.setIcon(QIcon("ui/image/15/start.png"))
        self.start_btn.clicked.connect(self.start)
        #ui.loadIcon(start_btn, 'SP_MediaPlay')
        layout.addWidget(self.start_btn)
        
        self.setLayout(layout)
        self.setWindowTitle("Server")
        ui.loadIcon(self, 'SP_VistaShield')

    def start(self):
        self.start_btn.setText("Disconnect client")
        self.start_btn.clicked.connect(self.stop)
        self.mainThread = threading.Thread(target=self.service.start)
        self.mainThread.start()
        pass

    # bug here
    # when stop it thread still open and however socket still open :)
    def stop(self, event):
        self.service.stop_client_connection()
        self.start_btn.setText("Start server")
        self.start_btn.clicked.connect(self.start)
        pass

    def clean2exit(self):
        self.service.stop()
        return super().clean2exit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    login = ServerWindow()
    login.show()
    app.exec_()