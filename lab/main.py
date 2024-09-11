import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel

class MotorTestSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高雄科技大學電機系 - 馬達特性測試系統")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.setup_main_menu()
        self.setup_single_phase_menu()
        self.setup_three_phase_menu()

    def setup_main_menu(self):
        main_menu = QWidget()
        main_layout = QVBoxLayout(main_menu)

        label = QLabel("馬達特性測試系統")
        main_layout.addWidget(label)

        btn_single_phase = QPushButton("單相馬達")
        btn_single_phase.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        main_layout.addWidget(btn_single_phase)

        btn_three_phase = QPushButton("三相馬達")
        btn_three_phase.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        main_layout.addWidget(btn_three_phase)

        btn_exit = QPushButton("Exit結束")
        btn_exit.clicked.connect(self.close)
        main_layout.addWidget(btn_exit)

        self.stacked_widget.addWidget(main_menu)

    def setup_single_phase_menu(self):
        single_phase_menu = QWidget()
        layout = QVBoxLayout(single_phase_menu)

        label = QLabel("單向馬達測試")
        layout.addWidget(label)

        options = [
            "無載測試", "堵轉測試", "鐵損分離測試", "頻率變動測試",
            "馬達參數輸入", "測試結果查詢", "載入馬達參數", "綜合測試",
            "測試結果列印", "回上頁"
        ]

        for option in options:
            btn = QPushButton(option)
            if option == "回上頁":
                btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
            layout.addWidget(btn)

        self.stacked_widget.addWidget(single_phase_menu)

    def setup_three_phase_menu(self):
        three_phase_menu = QWidget()
        layout = QVBoxLayout(three_phase_menu)

        label = QLabel("三向馬達測試")
        layout.addWidget(label)

        options = [
            "無載測試", "堵轉測試", "鐵損分離測試", "頻率變動測試",
            "馬達參數輸入", "測試結果查詢", "載入馬達參數", "綜合測試",
            "測試結果列印", "回上頁"
        ]

        for option in options:
            btn = QPushButton(option)
            if option == "回上頁":
                btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
            layout.addWidget(btn)

        self.stacked_widget.addWidget(three_phase_menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotorTestSystem()
    window.show()
    sys.exit(app.exec())