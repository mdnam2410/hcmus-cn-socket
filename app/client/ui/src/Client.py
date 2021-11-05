from tool import debug
from PyQt5 import QtGui, QtWidgets

name_func = [
	{'New':['Configuration','Connect','Disconnect']},
	{'Screen':[
		{'Screenshot': ['Screenshot','Save']},
		{'Sharescreen':['Recording']},
		'Configuration'
		]},
	{'Process-App':['Show','Start','Kill']},
	'Registry',
	{'Keyboard':[
		{'Hook':['Start','Stop','Show']},
		'Lock','Unlock'
		]},
	{'File Control':['View','Send','Remove']},
	{'Power':['Shutdown','Logout','Restart','Sleep','Lock']},
	{'Help':'About'}
]

# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'MainClient.ui'
class MainScreen(QtWidgets.QMainWindow):
    def run(self):
        self.setObjectName("MainWindow")
        self.resize(900, 750)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ui/image/16/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.menubar = QtWidgets.QMenuBar(self)

        #self.menubar.setGeometry(QtCore.QRect(0, 0, 887, 21))
        self.menubar.setObjectName("menubar")
        self.add_menu(name_func, self.menubar)
        self.setMenuBar(self.menubar)

    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QtWidgets.QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            self.add_command(data, menu_obj)

    def add_command(self, data: str, menu_obj: QtWidgets.QMenu):
        icon = QtGui.QIcon()
        icon_file_name = "../ui/image/16/"+data.lower()+".png"
        icon.addPixmap(QtGui.QPixmap(icon_file_name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        action = menu_obj.addAction(data)
        action.setIcon(icon)
        action.setIconText(data)

        self.show()
        

    def whoGotSelected(self, selection):
        # Getting the selected button obj, taking the given text name.
        name = selection.text()

        # Print the name selected.
        print(f"{name} is selected")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainScreen()
    ui.run()
    sys.exit(app.exec_())
