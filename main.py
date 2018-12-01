from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# S430 is a 480px x 800px screen 


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        w = 800; h = 480
        
        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Top'))
        layout.addWidget(QPushButton('Bottom'))
        layout.addWidget(QLabel('This Window is 480x800'))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget (container)
        self.setFixedSize(w, h)
        self.setWindowTitle("Driver Feedback Interface")
        
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
