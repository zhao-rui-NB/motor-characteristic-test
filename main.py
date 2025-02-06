from gui.main import MainWindow
from PyQt6.QtWidgets import QApplication
import sys




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())