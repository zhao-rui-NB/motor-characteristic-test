from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ..ui.ui_MotorTestSystem import Ui_MotorTestSystem

class MotorTestSystem:
    def __init__(self,ui: Ui_MotorTestSystem):
        # self.ui = Ui_MotorTestSystem()
        
        self.ui = ui
        
        self.ui.single_phase_menu.btn_NoLoad.clicked.connect(self.on_btn_NoLoad_clicked)
        
        self.ui.single_phase_menu.btn_LockedRotor.clicked.connect(self.on_btn_LockedRotor_clicked)
        
        self.ui.single_phase_menu.btn_FrequencyChange.clicked.connect(self.on_btn_FrequencyChange_clicked)
        

        
    def on_btn_NoLoad_clicked(self):
        print("No Load")
        
    def on_btn_LockedRotor_clicked(self):
        print("Locked Rotor")
        
    def on_btn_FrequencyChange_clicked(self):
        print("Frequency Change")    
    
        
if __name__ == "__main__":
    # app = QApplication([])
    # window = MotorTestSystem()
    # window.ui.show()
    # app.exec()
    
    app = QApplication([])
    ui = Ui_MotorTestSystem()
    window = MotorTestSystem(ui)
    window.ui.show()
    app.exec()
    