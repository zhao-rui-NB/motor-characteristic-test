from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from .ui_MainMenu import Ui_MainMenu
from .ui_SinglePhaseMenu import Ui_SinglePhaseMenu
from .ui_ThreePhaseMenu import Ui_ThreePhaseMenu

class Ui_MotorTestSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # set font size 24
        font = QFont()
        font.setPointSize(24)
        self.setFont(font)
        
        self.setupUi()
        
    def setupUi(self):
        
        self.main_layout = QStackedWidget(self)
        self.setCentralWidget(self.main_layout)
        
        
        self.main_menu = Ui_MainMenu()
        self.single_phase_menu = Ui_SinglePhaseMenu()
        self.three_phase_menu = Ui_ThreePhaseMenu()
        
        self.main_layout.addWidget(self.main_menu)
        self.main_layout.addWidget(self.single_phase_menu)
        self.main_layout.addWidget(self.three_phase_menu)
        
        self.main_menu.btn_single_phase.clicked.connect(self.on_btn_single_phase_clicked)
        self.main_menu.btn_three_phase.clicked.connect(self.on_btn_three_phase_clicked)
        
        self.single_phase_menu.btn_Back.clicked.connect(self.on_btn_back_clicked)
        self.three_phase_menu.btn_Back.clicked.connect(self.on_btn_back_clicked)
        
        self.main_menu.btn_exit.clicked.connect(self.close)
        
        
    def on_btn_single_phase_clicked(self):
        self.main_layout.setCurrentWidget(self.single_phase_menu)
    
    def on_btn_three_phase_clicked(self):
        self.main_layout.setCurrentWidget(self.three_phase_menu)
        
    def on_btn_back_clicked(self):
        self.main_layout.setCurrentWidget(self.main_menu)
        
if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MotorTestSystem()
    window.show()
    app.exec()        
                        
        
        
        
        
        
        
    
    