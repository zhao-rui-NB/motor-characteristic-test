from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class DataItemWidget(QGroupBox):
    def __init__(self, key, value, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0,0,0,0)
        
        self.setTitle(key)
        self.main_layout = QVBoxLayout(self)
        self.data_value = QLabel(value)
        
        self.data_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.data_value)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
    def resizeEvent(self, event):
        base_size = self.height()   
        value_font = self.data_value.font()
        value_font.setPointSize(max(12, int(base_size * 0.3)))
        self.data_value.setFont(value_font)
        super().resizeEvent(event)
        
    def set_key(self, key):
        self.setTitle(key)
        
    def set_value(self, value):
        self.data_value.setText(value)  
    
    def get_key(self):
        return self.title()

    def get_value(self):
        return self.data_value.text()


class ui_MotorMornitor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.item_names = [
            '電壓_RS','電壓_ST','電壓_TR','平均線電壓',
            '電壓_R','電壓_S','電壓_T','平均相電壓',
            '電流_R','電流_S','電流_T','平均電流',
            '功率_R','功率_S','功率_T','輸入功率',
            '乏功率_R','乏功率_S','乏功率_T','輸入乏功率',
            '視在功率_R','視在功率_S','視在功率_T','輸入視在功率',
            '轉速','轉矩','輸出功率','效率',
            '功率因數','頻率',
        ]
        
        self.item_dict: DataItemWidget = {}
        
        self.default_colunm = 4
        
        self.setMinimumSize(300, 450)
        
        self.initUI()
        
    def initUI(self):
        
        # self.center_widget = QWidget(self)
        
        for name in self.item_names:
            self.item_dict[name] = DataItemWidget(name, "N/A...")
            
        self.main_layout = QGridLayout(self)
        
        for i, (name, widget) in enumerate(self.item_dict.items()):
            row, col = divmod(i, self.default_colunm)
            self.main_layout.addWidget(widget, row, col)
            
        self.main_layout.setContentsMargins(0,0,0,0)

    

        
        
if __name__ == "__main__":
    app = QApplication([])
    window = ui_MotorMornitor()
    window.show()
    app.exec()
    
    
