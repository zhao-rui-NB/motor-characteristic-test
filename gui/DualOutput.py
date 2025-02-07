from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
# Qobject
from PyQt6.QtCore import QObject

import io


# Qtimer every 0.5 second update the textedit form log.txt
# class LogUpdater_Qthread(QThread):
#     def __init__(self, text_edit:QTextEdit):
#         super().__init__()
#         self.text_edit = text_edit

#     def run(self):


class log_updater(QObject):
    update_log_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
    
    def update_log(self, message):
        self.update_log_signal.emit(message)
        

class DualOutput(io.IOBase):
    def __init__(self, original_stdout: io.TextIOBase):
        self.original_stdout = original_stdout
        # self.text_edit = text_edit
        self.log_updater = log_updater()

    def write(self, message):
        # Print to the original stdout (command line)
        self.original_stdout.write(message)

        self.log_updater.update_log(message)

        # Emit signal to update the text edit
        # self.update_log_signal.emit(message)

        # with open("log.txt", "a", encoding='utf-8') as f:
        #     f.write(message)


        # vertical_scrollbar = self.text_edit.verticalScrollBar()
        # scrollbar_pos = vertical_scrollbar.value()
        # is_at_bottom = scrollbar_pos == vertical_scrollbar.maximum()
        
        # self.text_edit.setText(self.text_edit.toPlainText() + message)
        
        # if is_at_bottom:
        #     vertical_scrollbar.setValue(vertical_scrollbar.maximum())
        # else:
        #     vertical_scrollbar.setValue(scrollbar_pos)
            
    def flush(self):
        # Ensure flush functionality for compatibility with print
        self.original_stdout.flush()
        
        
# test script
if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    
    center_widget = QWidget()
    layout = QVBoxLayout(center_widget)  
    
    text_edit = QTextEdit()
    layout.addWidget(text_edit) 
    
    btn = QPushButton("Click me!")
    btn.clicked.connect(lambda: text_edit.setText(text_edit.toPlainText() + "Click me!"))
    layout.addWidget(btn)
    
    window.setCentralWidget(center_widget)
    window.show()
    
    # Redirect stdout to DualOutput
    import sys
    sys.stdout = DualOutput(sys.stdout, text_edit)
    
    print("Hello, world!")
    print("This is a test.")
    print("Goodbye!")
    
    app.exec()