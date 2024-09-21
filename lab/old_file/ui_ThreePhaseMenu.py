from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Ui_ThreePhaseMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        # set font size 24
        font = QFont()
        font.setPointSize(24)
        self.setFont(font)
        
        self.setupUi()
        
    def setupUi(self):
        self.main_layout = QVBoxLayout(self)
        

        self.label = QLabel("三相馬達測試")
        self.main_layout.addWidget(self.label)
        
        self.btn_NoLoad = QPushButton("無載測試") 
        self.main_layout.addWidget(self.btn_NoLoad)

        self.btn_LockedRotor = QPushButton("堵轉測試")
        self.main_layout.addWidget(self.btn_LockedRotor)
        
        self.btn_IronLoss = QPushButton("鐵損分離測試")
        self.main_layout.addWidget(self.btn_IronLoss)
        
        self.btn_FrequencyChange = QPushButton("頻率變動測試")
        self.main_layout.addWidget(self.btn_FrequencyChange)
        
        self.btn_ParameterInput = QPushButton("馬達參數輸入")
        self.main_layout.addWidget(self.btn_ParameterInput)
        
        self.btn_ResultQuery = QPushButton("測試結果查詢")
        self.main_layout.addWidget(self.btn_ResultQuery)
        
        self.btn_LoadMotorParameter = QPushButton("載入馬達參數")
        self.main_layout.addWidget(self.btn_LoadMotorParameter)
        
        self.btn_ComprehensiveTest = QPushButton("綜合測試")
        self.main_layout.addWidget(self.btn_ComprehensiveTest)
        
        self.btn_PrintResult = QPushButton("測試結果列印")
        self.main_layout.addWidget(self.btn_PrintResult)
        
        self.btn_Back = QPushButton("回上頁")
        self.main_layout.addWidget(self.btn_Back)        
        

        

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_ThreePhaseMenu()
    window.show()
    app.exec()