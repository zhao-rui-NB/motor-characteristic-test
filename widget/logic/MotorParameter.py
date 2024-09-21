from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import time
import json

from widget.ui.ui_MotorParameter import Ui_MotorParameter

class MotorParameter():
    def __init__(self, ui:Ui_MotorParameter):
        super().__init__()
        self.ui = ui
        
        self.now_file = None
        
    def make_default_file_name(self):
        # format time y m d_h m s
        t = time.strftime("%Y%m%d_%H%M%S")
        return f"motor_parameter_{t}.json"    
    
    def dump_data(self):
        data = {}
        for key, item in self.ui.tree_lineedit.items():
            data[key] = item.text()
        return data
    
    
    def save_as_file(self):
        # ask user to select file
        file_name, s2 = QFileDialog.getSaveFileName(self.ui, "Save File", self.make_default_file_name(), "JSON File (*.json)")
        if file_name:
            with open(file_name, 'w', encoding='utf8') as f:
                json.dump(self.dump_data(), f, ensure_ascii=False, indent=4)
            self.now_file = file_name
            
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Save as Success")
            msg.exec()
        
    
    def save_file(self):
        if self.now_file:
            with open(self.now_file, 'w', encoding='utf8') as f:
                json.dump(self.dump_data(), f, ensure_ascii=False, indent=4)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Save Success")
            msg.exec()
        else:
            self.save_as_file()
                            
    def load_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.ui, "Open File", "", "JSON File (*.json)")
        if not file_name:
            return
        
        with open(file_name, 'r', encoding='utf8') as f:
            try:
                data = json.load(f)
                for k,v in data.items():
                    if k in self.ui.tree_lineedit.keys():
                        self.ui.tree_lineedit[k].setText(str(v))
            except Exception as e:
                # show error message with QMessageBox
                msg = QMessageBox()
                msg.setText("Error")
                msg.setWindowTitle("Error")
                msg.setInformativeText(str(e))
                msg.exec()
                print(e)
                return

        self.now_file = file_name
        
        # show success message with QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Load Success")
        msg.exec()
    
    def new_file(self):
        for key, item in self.ui.tree_lineedit.items():
            item.setText("")
        self.now_file = None
            
            
            
                                    
    
    
    
    
    
if __name__ == "__main__":
    
    class test_singal_panel(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("test")
            self.main_layout = QVBoxLayout(self)
            
            
            self.button = QPushButton("test")
            self.main_layout.addWidget(self.button)
            
            
            self.save_btn = QPushButton("save")
            self.main_layout.addWidget(self.save_btn)
            
            self.save_as_btn = QPushButton("save as")
            self.main_layout.addWidget(self.save_as_btn)
            
            self.load_btn = QPushButton("load")
            self.main_layout.addWidget(self.load_btn)
            
            self.new_btn = QPushButton("new")
            self.main_layout.addWidget(self.new_btn)
    
            self.show()
    
    app = QApplication([])
    ui = Ui_MotorParameter()
    ctrl = MotorParameter(ui)
    ui.show()
    ui.setGeometry(0, 100, 800, 600)
    
    test = test_singal_panel()
    test.setGeometry(800, 100, 800, 600)
    test.button.clicked.connect(lambda: print(ctrl.dump_data()))
    
    test.save_btn.clicked.connect(lambda: ctrl.save_file())
    test.save_as_btn.clicked.connect(lambda: ctrl.save_as_file())
    
    test.load_btn.clicked.connect(lambda: ctrl.load_from_file())    
    
    test.new_btn.clicked.connect(lambda: ctrl.new_file())
    
    
    app.exec()