from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QStyle

# https://www.pythonguis.com/faq/built-in-qicons-pyqt/2
def loadIcon(view, name_icon):
    pixmapi = getattr(QStyle, name_icon)
    icon = view.style().standardIcon(pixmapi)
    view.setWindowIcon(icon)

class Windows(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setGeometry(300, 300, 300, 100)
        loadIcon(self, 'SP_MessageBoxQuestion')
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
            self.clean2exit()
        else:
            event.ignore()
    
    def clean2exit(self):
        pass