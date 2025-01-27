from  PyQt6.QtWidgets  import * 
from  matplotlib.backends.backend_qtagg import  FigureCanvasQTAgg  as  FigureCanvas
from  matplotlib.figure  import  Figure 

    
class  MplWidget(QWidget):
    def  __init__(self, parent=None):
        QWidget.__init__(self, parent) 
        self.canvas = FigureCanvas(Figure()) 
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        
        self.canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
