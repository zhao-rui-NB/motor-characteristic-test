import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea

class ScrollExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 創建主佈局
        main_layout = QVBoxLayout(self)

        # 創建滾動區域
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        # 創建容器 widget 並設置佈局
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        vbox = QVBoxLayout(content_widget)

        # 添加多個按鈕
        for i in range(20):
            button = QPushButton(f'Button {i+1}')
            vbox.addWidget(button)

        # 設置窗口屬性
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Scroll Area Example')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScrollExample()
    ex.show()
    sys.exit(app.exec())