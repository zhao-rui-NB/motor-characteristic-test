import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import QDate
import json

class MotorTestPlatform(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('馬達測試平台')
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # 創建輸入字段
        self.fields = {}
        grid = QGridLayout()

        parameters = [
            ('試驗日期', QLineEdit()),
            ('印表日期', QLineEdit()),
            ('額定電壓', QLineEdit()),
            ('額定電流', QLineEdit()),
            ('馬力', QLineEdit()),
            ('空載電流', QLineEdit()),
            ('相數', QLineEdit()),
            ('頻率', QLineEdit()),
            ('極數', QLineEdit()),
            ('迴轉數', QLineEdit())
        ]

        for i, (label, widget) in enumerate(parameters):
            grid.addWidget(QLabel(label), i, 0)
            grid.addWidget(widget, i, 1)
            self.fields[label] = widget

        # 設置日期欄位的默認值為今天
        today = QDate.currentDate().toString("yyyy-MM-dd")
        self.fields['試驗日期'].setText(today)
        self.fields['印表日期'].setText(today)

        layout.addLayout(grid)

        # 創建按鈕
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('儲存')
        save_btn.clicked.connect(self.save_data)
        load_btn = QPushButton('載入')
        load_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(load_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def save_data(self):
        data = {field: widget.text() for field, widget in self.fields.items()}
        filename, _ = QFileDialog.getSaveFileName(self, "儲存檔案", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f)
            QMessageBox.information(self, "成功", "數據已成功儲存！")

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "載入檔案", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            for field, value in data.items():
                if field in self.fields:
                    self.fields[field].setText(value)
            QMessageBox.information(self, "成功", "數據已成功載入！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MotorTestPlatform()
    ex.show()
    sys.exit(app.exec())