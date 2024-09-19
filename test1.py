import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal

# calc_ui.py
class CalculatorUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.display = QLabel('0')
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        positions = [(i + 1, j) for i in range(4) for j in range(4)]

        for position, button in zip(positions, buttons):
            btn = QPushButton(button)
            layout.addWidget(btn, *position)
            btn.clicked.connect(self.on_button_clicked)

        self.setLayout(layout)

    def on_button_clicked(self):
        # 這個方法在邏輯層中被重寫
        pass

# calc_logic.py
class CalculatorLogic(CalculatorUI):
    result_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_input = ''

    def on_button_clicked(self):
        button = self.sender()
        key = button.text()

        if key == '=':
            try:
                result = str(eval(self.current_input))
                self.display.setText(result)
                self.result_changed.emit(result)
            except:
                self.display.setText('Error')
        else:
            self.current_input += key
            self.display.setText(self.current_input)

# 主應用程式
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("多功能應用程式")
        self.setGeometry(100, 100, 800, 600)

        # 中央窗口
        self.central_widget = QTextEdit()
        self.setCentralWidget(self.central_widget)

        # 創建並添加計算機作為可停靠窗口
        self.create_dockable_calculator("計算機", Qt.DockWidgetArea.RightDockWidgetArea)

        # 添加其他可停靠窗口（示例）
        self.create_dockable_widget("筆記", Qt.DockWidgetArea.LeftDockWidgetArea, QTextEdit("這裡可以寫筆記"))

    def create_dockable_calculator(self, title, area):
        dock = QDockWidget(title, self)
        calculator = CalculatorLogic()
        dock.setWidget(calculator)
        self.addDockWidget(area, dock)
        calculator.result_changed.connect(self.on_calculator_result)

    def create_dockable_widget(self, title, area, widget):
        dock = QDockWidget(title, self)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)

    def on_calculator_result(self, result):
        self.central_widget.append(f"計算結果: {result}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())