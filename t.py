from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import QSize

class DynamicGridWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        # 添加一些數據控件作為範例（可以是自定義的 data widgets）
        self.widgets = [QPushButton(f"Button {i+1}") for i in range(10)]
        for widget in self.widgets:
            self.layout.addWidget(widget)

        # 設置每個控件的大小
        self.widget_size = QSize(150, 50)

    def resizeEvent(self, event):
        # 取得當前視窗的寬度
        window_width = self.width()
        
        # 計算每行應該顯示多少個 widget (例如每個 widget 寬度約為 150)
        column_count = max(1, window_width // self.widget_size.width())

        # 清除當前的布局
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget)
        
        # 根據新的列數重新排列控件
        row, col = 0, 0
        for i, widget in enumerate(self.widgets):
            self.layout.addWidget(widget, row, col)
            col += 1
            if col >= column_count:
                col = 0
                row += 1

        super().resizeEvent(event)

# 主程式執行
app = QApplication([])

# 創建並顯示動態網格視窗
window = DynamicGridWidget()
window.setWindowTitle('Dynamic Column Grid Example')
window.resize(600, 400)  # 設置初始大小
window.show()

app.exec()
