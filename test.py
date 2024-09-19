import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class SizePolicyDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("This is a test label with Preferred size policy")
        self.label.setStyleSheet("background-color: lightblue;")
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        self.button = QPushButton("Toggle minimum size")
        self.button.clicked.connect(self.toggleMinSize)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Size Policy Demo')

    def toggleMinSize(self):
        if self.label.minimumWidth() == 0:
            self.label.setMinimumSize(200, 50)
            self.button.setText("Remove minimum size")
        else:
            self.label.setMinimumSize(0, 0)
            self.button.setText("Set minimum size")

        # 強制重新計算佈局
        self.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SizePolicyDemo()
    ex.show()
    sys.exit(app.exec())