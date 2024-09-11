from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


from logic.MotorTestSystem import MotorTestSystem


if __name__ == '__main__':
    app = QApplication([])
    window = MotorTestSystem()
    window.ui.show()
    
    app.exec()    
    
    
    