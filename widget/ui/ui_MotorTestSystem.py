from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from .ui_MainMenu import Ui_MainMenu
from .ui_SinglePhaseMenu import Ui_SinglePhaseMenu
from .ui_ThreePhaseMenu import Ui_ThreePhaseMenu

class Ui_MotorTestSystem(QWidget):
    def __init__(self):
        super().__init__()
        
        # set font size 24
        font = QFont()
        font.setPointSize(24)
        self.setFont(font)
        
        self.setupUi()
    
    
    def setupUi(self):
        self.outlayout = QVBoxLayout(self)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.outlayout.addWidget(self.scroll_area)
        
        # 創建容器 widget
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        
        # 創建並添加主菜單
        self.main_menu = Ui_MainMenu()  # 假設這是一個 QWidget
        self.scroll_area.setWidget(self.main_menu)
        
        # # 設置佈局的對齊方式和間距
        # self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.container_layout.setSpacing(10)
        
        # 設置大小策略
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    
    def setupUi_(self):
    
        
        self.outlayout = QVBoxLayout(self)
        
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # 允許滾動區域調整大小
        self.outlayout.addWidget(self.scroll_area)
        
        
        
        # 創建一個容器 widget 來放置您的主菜單
        container = QWidget()
        self.scroll_area.setWidget(container)
        
        # 創建一個佈局來放置您的主菜單內容
        container_layout = QVBoxLayout(container)
        
        # 假設 Ui_MainMenu 是一個自定義的 widget 類
        self.main_menu = Ui_MainMenu()

        # 將主菜單添加到容器佈局中
        container_layout.addWidget(self.main_menu)
                
        
        # self.main_menu = Ui_MainMenu()
        # self.single_phase_menu = Ui_SinglePhaseMenu()
        # self.three_phase_menu = Ui_ThreePhaseMenu()

        
        # test_layoyt = QVBoxLayout()
        # self.scroll_area.setLayout(test_layoyt)
        
        # test_layoyt.addWidget(self.main_menu)
        
        
        # self.main_layoyt.addWidget(self.main_menu)

        # self.main_widget.addWidget(self.main_menu)
        # self.main_widget.addWidget(self.single_phase_menu)
        # self.main_widget.addWidget(self.three_phase_menu)        
        # self.main_layout.addWidget(self.main_menu)
        # self.main_layout.addWidget(self.single_phase_menu)
        # self.main_layout.addWidget(self.three_phase_menu)
        
        # self.main_menu.btn_single_phase.clicked.connect(self.on_btn_single_phase_clicked)
        # self.main_menu.btn_three_phase.clicked.connect(self.on_btn_three_phase_clicked)
        
        # self.single_phase_menu.btn_Back.clicked.connect(self.on_btn_back_clicked)
        # self.three_phase_menu.btn_Back.clicked.connect(self.on_btn_back_clicked)
        
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
                        
        
        
        
        
        
        
    
    