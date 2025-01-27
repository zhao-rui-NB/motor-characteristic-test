from  PyQt6.QtWidgets  import * 
from  matplotlib.backends.backend_qtagg import  FigureCanvasQTAgg  as  FigureCanvas
from  matplotlib.figure  import  Figure 
import numpy as np
    
class  MplWidget(QWidget):
    def  __init__(self, parent=None):
        QWidget.__init__(self, parent) 
        self.canvas = FigureCanvas(Figure()) 
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(self.canvas)
        
        
        self.canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.ax = self.canvas.figure.add_subplot(111)
        
        # 設置畫布上的圖形
        self.plot(np.linspace(0, 50, 1000), np.sin(np.linspace(0, 50, 1000)))

    def get_axes(self):
        return self.ax
    
    def plot(self, x,y):
        self.ax.clear()
        # 繪製新的圖形
        self.ax.plot(x, y, 'r')

        
        
        
