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
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)