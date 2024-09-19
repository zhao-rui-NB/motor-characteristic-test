import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                             QDockWidget, QPushButton, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("可拖拽多视窗示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建中央小部件
        self.central_widget = QTextEdit()
        self.setCentralWidget(self.central_widget)

        # 创建并添加可停靠窗口
        self.create_dockable_window("窗口1", Qt.DockWidgetArea.LeftDockWidgetArea)
        self.create_dockable_window("窗口2", Qt.DockWidgetArea.RightDockWidgetArea)
        self.create_dockable_window("窗口3", Qt.DockWidgetArea.BottomDockWidgetArea)

    def create_dockable_window(self, title, area):
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        # 创建dock窗口的内容
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.addWidget(QPushButton(f"{title}的按钮"))
        layout.addWidget(QTextEdit(f"{title}的文本编辑区"))

        dock.setWidget(content)
        self.addDockWidget(area, dock)

        return dock

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())