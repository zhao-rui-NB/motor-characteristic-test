import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit
from PyQt6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DockWidget Layout Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件
        central_widget = QTextEdit()
        self.setCentralWidget(central_widget)

        # 创建左侧DockWidget
        left_dock = QDockWidget("Left Dock", self)
        left_dock.setWidget(QTextEdit())
        left_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

        # 设置左侧DockWidget的尺寸策略
        left_dock.widget().setMinimumWidth(200)
        left_dock.widget().setMaximumWidth(400)

        # 创建底部DockWidget
        bottom_dock = QDockWidget("Bottom Dock", self)
        bottom_dock.setWidget(QTextEdit())
        bottom_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, bottom_dock)

        # 设置底部DockWidget的尺寸策略
        bottom_dock.widget().setMinimumHeight(100)
        bottom_dock.widget().setMaximumHeight(200)

        # 设置左下角由左侧DockWidget占据
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())