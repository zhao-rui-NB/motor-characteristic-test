import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QSize

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        for i in range(10):
            button = QPushButton(f"Button {i+1}")
            layout.addWidget(button)
        
        # 設置大小策略為垂直方向可擴展
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    
    def sizeHint(self):
        # 返回一個合適的初始大小
        return QSize(200, 400)

    def minimumSizeHint(self):
        # 返回一個合理的最小大小
        return QSize(150, 300)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adaptive Scrollable Layout")
        self.initUI()

    def initUI(self):
        # 創建一個中央widget來容納滾動區域
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 創建主佈局
        main_layout = QVBoxLayout(central_widget)

        # 創建滾動區域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 創建 MyWidget 實例
        my_widget = MyWidget()

        # 將 MyWidget 設置為滾動區域的widget
        scroll_area.setWidget(my_widget)

        # 將滾動區域添加到主佈局
        main_layout.addWidget(scroll_area)

        # 設置初始窗口大小
        self.resize(300, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
exit()
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QScrollArea
from PyQt6.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # put 10 button in a vertical layout
        layout = QVBoxLayout(self)
        for i in range(10):
            button = QPushButton(f"Button {i+1}")
            layout.addWidget(button)
            
    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable and Scrollable Layout")

    def initUI(self):
        # create a main layout
        my_widget = MyWidget()
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
    
    # # test My Widget
    # app = QApplication(sys.argv)
    # window = MyWidget()
    # window.show()
    # app.exec()