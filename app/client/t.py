# import sched, time
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc): 
#     print("Doing stuff...")
#     # do your stuff
#     s.enter(2, 1, do_something, (sc,))

# s.enter(2, 1, do_something, (s,))
# s.run()

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import Qt


# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data

#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]

#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)

#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.table = QtWidgets.QTableView()

#         data = [
#           [4, 9, 2],
#           [1, 0, 0],
#           [3, 5, 0],
#           [3, 3, 2],
#           [7, 8, 9],
#         ]

#         self.model = TableModel(data)
#         self.table.setModel(self.model)

#         self.setCentralWidget(self.table)


# app=QtWidgets.QApplication(sys.argv)
# window=MainWindow()
# window.show()
# app.exec_()

# Import necessary libraries
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDesktopWidget
# from PyQt5.QtCore import QSize

# # Define class to create the table with static data
# class SimpleTable(QMainWindow):
#     def __init__(self):
#         # Call the parent constructor
#         super().__init__()

#         # Set the size and title of the window
#         self.setMinimumSize(QSize(420, 150))
#         self.setWindowTitle("Simple Table with Static Data")

#         # Create the table with necessary properties
#         table = QTableWidget(self)
#         table.setColumnCount(4)
#         table.setRowCount(5)
#         table.setMinimumWidth(500)
#         table.setMinimumHeight(500)

#         # Set the table headers
#         table.setHorizontalHeaderLabels(["Header-1", "Header-2", "Header-3", "Header-4"])

#         # Set the table values
#         for i in range(5):
#             for j in range(4) :
#                 table.setItem(i, j, QTableWidgetItem("Row-" + str(i+1) + " , Col-" + str(j+1)))

#         # Resize of the rows and columns based on the content
#         table.resizeColumnsToContents()
#         table.resizeRowsToContents()

#         # Display the table
#         table.show()

#         # Display the window in the center of the screen
#         win = self.frameGeometry()
#         pos = QDesktopWidget().availableGeometry().center()
#         win.moveCenter(pos)
#         self.move(win.topLeft())
#         self.show()

# # Create app object and execute the app
# app = QApplication(sys.argv)
# mw = SimpleTable()
# mw.show()
# app.exec()

# import sys
# from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
# QLineEdit, QInputDialog)

# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.btn = QPushButton('Show Dialog', self)
#         self.btn.move(20, 20)
#         self.btn.clicked.connect(self.showDialog)

#         self.le = QLineEdit(self)
#         self.le.move(130, 22)

#         self.setGeometry(300, 300, 300, 150)
#         self.setWindowTitle('Input Dialog')        
#         self.show()

#     def showDialog(self):
#         text, ok = QInputDialog.getText(self, 'input dialog', 'Is this ok?')
#         if ok:
#             self.le.setText(str(text))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


# from PyQt5 import QtGui, QtCore, QtWidgets
# import cv2
# import sys

# class DisplayImageWidget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(DisplayImageWidget, self).__init__(parent)

#         self.button = QtWidgets.QPushButton('Show picture')
#         self.button.clicked.connect(self.show_image)
#         self.image_frame = QtWidgets.QLabel()

#         self.layout = QtWidgets.QVBoxLayout()
#         self.layout.addWidget(self.button)
#         self.layout.addWidget(self.image_frame)
#         self.setLayout(self.layout)

#     @QtCore.pyqtSlot()
#     def show_image(self):
#         self.image = cv2.imread('placeholder4.PNG')
#         print(self.image)
#         self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
#         self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     display_image_widget = DisplayImageWidget()
#     display_image_widget.show()
#     sys.exit(app.exec_())

import sys
from PyQt5 import QtCore, QtWidgets 



class Example(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainLayout = QtWidgets.QGridLayout()
        self.setLayout(self.mainLayout)
        self.columnas = ["Columna 1", "Columna 2"]
        self.listaDatos = [["A", "B"],["C", "D"]]  
        self.tabla()        


    def tabla(self):
        #Boton de exportar a excel
        self.toolButton = QtWidgets.QToolButton()
        self.toolButton.clicked.connect(self.exportar)   # <<<<<<<<<<<<<<<<<<<<<<<
        #Tabla
        self.table = QtWidgets.QTableView()
        self.table.setObjectName("table")

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(self.columnas))
        self.tableWidget.setRowCount(len(self.listaDatos))

        #Colocamos la cabecera
        self.tableWidget.setHorizontalHeaderLabels(self.columnas)
        header_view = self.tableWidget.horizontalHeader()
        idx = header_view.count() - 1
        header_view.setSectionResizeMode(idx, QtWidgets.QHeaderView.ResizeToContents)

        #Colocamos los datos
        for fila, lista in enumerate(self.listaDatos):
            for columna, elemento in enumerate(lista):
                self.tableWidget.setItem(fila, columna,
                                         QtWidgets.QTableWidgetItem(elemento)
                                         )
        # Evento
        self.tableWidget.doubleClicked.connect(self.on_click)  # <<<<<<<<<<<<<<

        #Layout
        self.mainLayout.addWidget(self.tableWidget, 7, 0, 5, 7)
        self.mainLayout.addWidget(self.toolButton, 6, 5, 1, 1, QtCore.Qt.AlignRight)


    #Metodo asociado al evento de hacer doble click sobre una fila de la tabla 
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_click(self, index):
        row = index.row()
        column = index.column()
        print(row, column)


    @QtCore.pyqtSlot()
    def exportar(self):
        '''
        A modo de ejemplo solo imprime el contenido de la tabla
        en forma de csv
        '''
        print("Exportando tabla:")
        for row in range(self.tableWidget.rowCount()):
            print(",".join(self.tableWidget.item(row, column).text()
                for column in range(self.tableWidget.columnCount())))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = Example()
    dialog.exec_()