import sys

"""
from PySide6.QtWidgets import QApplication, QPushButton

def button_clicked():
    print("Clicked")


app = QApplication(sys.argv)


button = QPushButton("Press Me")
button.clicked.connect(button_clicked)

button.show()
app.exec()
"""

"""
#importing the components we need
from PySide6.QtWidgets import QApplication, QPushButton

def button_clicked(data):
    print("Clicked", data)


app = QApplication(sys.argv)


button = QPushButton("Press Me")
button.setCheckable(True)
button.clicked.connect(button_clicked)

button.show()
app.exec()
"""

"""
#importing the components we need
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSlider

def respond_to_slider(data):
    print("Slider Moved To: ", data)


app = QApplication(sys.argv)
slider = QSlider(Qt.Horizontal)
slider.setMaximum(100)
slider.setMinimum(1)
slider.setValue(25)

slider.valueChanged.connect(respond_to_slider)

slider.show()
app.exec()

"""
"""
#importing the components we need
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout

class RockWidget (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RockWidget")
        button1 = QPushButton("Button1")
        button1.clicked.connect(self.button1_clicked)
        button2 = QPushButton("Button2")
        button2.clicked.connect(self.button2_clicked)

        button_layout = QVBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        self.setLayout(button_layout)

    def button1_clicked(self):
        print("Button 1 Clicked")

    def button2_clicked(self):
        print("Button 2 Clicked")



app = QApplication(sys.argv)

window = RockWidget()
window.show()

app.exec()
"""
#importing the components we need
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QToolBar, QStatusBar

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Testing")

        #menubar and menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Cut")
        edit_menu.addAction("Paste")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        menu_bar.addMenu("Window")
        menu_bar.addMenu("Settings")
        menu_bar.addMenu("Help")


        toolbar = QToolBar("Main Tool Bar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        toolbar.addAction(quit_action)

        action1 = QAction("Some Action", self)
        action1.setStatusTip("Status message from some Action")
        action1.triggered.connect(self.toolbar_button_click)
        toolbar.addAction(action1)

        action2 = QAction(QIcon("start.png"),"Some other Action", self)
        action2.setStatusTip("Status message from some other Action")
        action2.triggered.connect(self.toolbar_button_click)
        action2.setCheckable(True)
        toolbar.addAction(action2)

        toolbar.addSeparator()
        toolbar.addWidget(QPushButton("Click Here"))


        self.setStatusBar(QStatusBar(self))

        button1 = QPushButton("Button1")
        button1.clicked.connect(self.button1_clicked)
        self.setCentralWidget(button1)

    def button1_clicked(self):
        print("clicked on the button")

    def toolbar_button_click(self):
        self.statusBar().showMessage("Message from Application", 3000)

    def quit_app(self):
        self.app.quit()

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()
