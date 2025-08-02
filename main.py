from gui.main import MainWindow
from PyQt6.QtWidgets import QApplication
import sys




if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyle('WindowsVista')
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"[ERROR] 發生嚴重異常錯誤，請重啟馬達測試系統: {e}")
        # input("Press Enter to exit...")
        # sys.exit(1)