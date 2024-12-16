from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Ui_MotorTestMenu(QScrollArea):
    def __init__(self):
        super().__init__()
        
        # set font size 24
        # font = QFont()
        # font.setPointSize(24)
        # self.setFont(font)
        
        self.setupUi()
    
    '''
    self(out widget)
    |-- outlayout
        |-- scroll_area
            |-- main_widget
                |-- main_layout
                    |-- label
                    |-- btn_NoLoad
                    |-- btn_LockedRotor
                    |-- btn_IronLoss
                    |-- btn_FrequencyChange
                    |-- btn_ParameterInput
                    |-- btn_ResultQuery
                    |-- btn_LoadMotorParameter
                    |-- btn_ComprehensiveTest
                    |-- btn_PrintResult
                    |-- btn_Back
    
    '''
    
    
    def setupUi(self):
        
        self.setWidget(QWidget())
        self.widget().setLayout(QVBoxLayout())
        self.setWidgetResizable(True)
        
        
        self.main_layout = self.widget().layout()
        
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
        
        self.main_layout.addStretch(1)

    
    
    def create_motor_type_menu(self):
        self.setWindowTitle("高雄科技大學電機系 - 馬達特性測試系統")
        
        main_layout = QVBoxLayout(self)
        
        label_1 = QLabel("高雄科技大學電機系")
        main_layout.addWidget(self.label_1)
        
        label_2 = QLabel("馬達特性測試系統")
        main_layout.addWidget(self.label_2)
        
        self.btn_single_phase = QPushButton("單相馬達")
        main_layout.addWidget(self.btn_single_phase)

        self.btn_three_phase = QPushButton("三相馬達")
        main_layout.addWidget(self.btn_three_phase)


if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MotorTestMenu()
    window.show()
    app.exec()
        