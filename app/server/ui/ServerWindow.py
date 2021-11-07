import app.core.ui as ui
import app.server.packages.service as service

import logging
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
import threading

class ServerWindow(ui.Windows):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        logging.debug(f'Creating server UI')
        self.service = service.Service()
        layout = QVBoxLayout()

        self.control_btn = QPushButton("Start server")
        self.control_btn.clicked.connect(self.start)
        layout.addWidget(self.control_btn)
        
        self.setLayout(layout)
        self.setWindowTitle("Server")
        ui.loadIcon(self, 'SP_VistaShield')

    def start(self):
        logging.debug("Start")
        self.control_btn.setText("Disconnect client")
        self.control_btn.clicked.disconnect(self.start)
        self.control_btn.clicked.connect(self.stop)
        def target():
            self.service.start()
        self.service_thread = threading.Thread(target=target)
        self.service_thread.start()

    def stop(self):
        logging.debug("Stop")
        self.service.stop()
        self.control_btn.setText("Start server")
        self.control_btn.clicked.disconnect(self.stop)
        self.control_btn.clicked.connect(self.start)
        pass

    def clean2exit(self):
        if self.service.is_alive():
            self.service.stop()
        return super().clean2exit()
