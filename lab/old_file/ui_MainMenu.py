from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Ui_MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        # set font size 24
        font = QFont()
        font.setPointSize(24)
        self.setFont(font)
        
        self.setupUi()
        
    def setupUi(self):
        
        self.setObjectName("MainMenu")
        self.setWindowTitle("高雄科技大學電機系 - 馬達特性測試系統")
        
        main_layout = QVBoxLayout(self)
        
        self.label_1 = QLabel("高雄科技大學電機系 - 馬達特性測試系統")
        main_layout.addWidget(self.label_1)
        
        self.label_2 = QLabel("馬達特性測試系統")
        main_layout.addWidget(self.label_2)
        
        self.btn_single_phase = QPushButton("單相馬達")
        main_layout.addWidget(self.btn_single_phase)

        self.btn_three_phase = QPushButton("三相馬達")
        main_layout.addWidget(self.btn_three_phase)

        self.btn_exit = QPushButton("Exit結束")
        self.btn_exit.clicked.connect(self.close)
        main_layout.addWidget(self.btn_exit)

        

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MainMenu()
    window.show()
    app.exec()