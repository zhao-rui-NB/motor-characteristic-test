from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import json
import sys

class Ui_MotorParameter(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ctrl_pressed = False
        
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)
        
        self.technical_parameters = [
            '額定電壓', '額定電流', '馬力', '空載電流', '相數', '頻率', '極數', '迴轉數'
        ]
        
        self.basic_info = [
            '廠牌', '型號', '序號', '備註'
        ]
        
        
        self.unit = {
            '額定電壓': 'V', '額定電流': 'A', '馬力': 'HP', '空載電流': 'A',
            '相數': 'PH', '頻率': 'Hz', '極數': 'P', '迴轉數': 'RPM'
        }
        
        self.tree_items = {}
        self.tree_lineedit = {}
        
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)
        
        self.tree_widget = QTreeWidget()
        self.main_layout.addWidget(self.tree_widget)
        
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(['項目', '值'])

        tech_param_item = QTreeWidgetItem(self.tree_widget, ['技術參數'])
        for param in self.technical_parameters:
            self.add_parameter(tech_param_item, param)

        basic_info_item = QTreeWidgetItem(self.tree_widget, ['基本資料'])
        for info in self.basic_info:
            self.add_parameter(basic_info_item, info)
        
        self.tree_widget.expandAll()
        self.tree_widget.resizeColumnToContents(0)

    def add_parameter(self, parent_item, param):
        param_and_util = f'{param}\t({self.unit[param]})' if param in self.unit else param
        item = QTreeWidgetItem(parent_item, [param_and_util])
        edit = QLineEdit()
        if param not in self.basic_info:
            edit.setValidator(QDoubleValidator())
        self.tree_widget.setItemWidget(item, 1, edit)
        self.tree_items[param] = item
        self.tree_lineedit[param] = edit

    # change the font size by press ctrl and mouse wheel 
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = True
    
    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False

    def wheelEvent(self, event: QWheelEvent):
        if self.ctrl_pressed:
            font = self.font()
            new_size = font.pointSize()
            if event.angleDelta().y() > 0:
                new_size = new_size + 2
            else:
                new_size = max(8, new_size - 2)
            font.setPointSize(new_size)
            self.setFont(font)
            
            # resize the tree widget
            self.tree_widget.resizeColumnToContents(0)
    
    
if __name__ == '__main__':
    app = QApplication([])
    windows = Ui_MotorParameter()
    windows.show()
    app.exec()