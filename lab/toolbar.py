import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("左側工具欄範例")
        self.setGeometry(100, 100, 800, 600)

        # 創建一個工具欄
        toolbar = QToolBar("工具欄")
        # self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolbar)  # 將工具欄放置在左側
        self.addToolBar(toolbar)
        

        # 添加動作到工具欄
        action_1 = QAction("動作 1", self)
        toolbar.addAction(action_1)

        action_2 = QAction("動作 2", self)
        toolbar.addAction(action_2)

        # # 創建一個中央的文字編輯器
        # editor = QTextEdit("這是主區域")
        # self.setCentralWidget(editor)
        
        
        # set center label 
        main_widget = QWidget()
        layout =  QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)
        
        
        label = QLabel("Test System")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        tb = QToolButton()
        tb.setText("Test")
        
        layout.addWidget(tb)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())