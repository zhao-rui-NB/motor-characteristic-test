from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class DataItemWidget(QWidget):
    def __init__(self, key, value, parent=None):
        super().__init__(parent)
        self.setMinimumSize(50, 50)
        self.setContentsMargins(0,0,0,0)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.data_key = QLabel(key)
        self.data_value = QLabel(value)
        self.data_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.data_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.data_key.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.data_value.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        self.main_layout.addWidget(self.data_key, 1)
        self.main_layout.addWidget(self.data_value, 2)
        
            # font-size: 20px;
        self.data_key.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        """)
        
            # font-size: 24px;
        self.data_value.setStyleSheet("""
            background-color: white;
            color: #2c3e50;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
        
    def resizeEvent(self, event):
        base_size = self.height()
        key_font = self.data_key.font()
        key_font.setPointSize(max(8, int(base_size * 0.15)))
        self.data_key.setFont(key_font)

        value_font = self.data_value.font()
        value_font.setPointSize(max(10, int(base_size * 0.3)))
        self.data_value.setFont(value_font)

        super().resizeEvent(event)
        
        
    def set_key(self, key):
        self.data_key.setText(key)
        
    def set_value(self, value):
        self.data_value.setText(value)  
    
    def get_key(self):
        return self.data_key.text()

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
        
        self.center_widget = QWidget(self)
        
        for name in self.item_names:
            self.item_dict[name] = DataItemWidget(name, "N/A")
            
        self.main_layout = QGridLayout(self.center_widget)
        
        for i, (name, widget) in enumerate(self.item_dict.items()):
            row, col = divmod(i, self.default_colunm)
            self.main_layout.addWidget(widget, row, col)
            
        self.main_layout.setContentsMargins(0,0,0,0)
        # self.main_layout.setSpacing(0)
        
        
        # set layout at the center
        # self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def resizeEvent(self, event:QResizeEvent):
        # put the self center widget to the center of the window
        
        ratio_limit = 1.4
        
        new_width = self.width() # fix the width
        new_height = self.height()
        new_height = min(new_height, int(new_width * ratio_limit))
        
        
        # set the center widget to the center of the window
        
        self.center_widget.setGeometry(
            int(event.size().width() - new_width) // 2,
            int(event.size().height() - new_height) // 2,
            new_width,
            new_height
        )
        
        
if __name__ == "__main__":
    app = QApplication([])
    window = ui_MotorMornitor()
    window.show()
    app.exec()
    
    # test item widget
    # app = QApplication([])
    # window = DataItemWidget("電壓_RS", "N/A")
    # window.show()
    # app.exec()
    
