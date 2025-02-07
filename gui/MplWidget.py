from  PyQt6.QtWidgets  import * 
from  PyQt6.QtCore  import *
from  PyQt6.QtGui  import *
from  matplotlib.backends.backend_qtagg import  FigureCanvasQTAgg  as  FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from  matplotlib.figure  import  Figure 
import numpy as np
    
class  MplWidget(QFrame):
    def  __init__(self, parent=None):
        super().__init__(parent)
        
        self.canvas = FigureCanvas(Figure())
        self.toolbar = NavigationToolbar(self.canvas)
        # add the canvas to the frame
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(self.toolbar, 1)
        vertical_layout.addWidget(self.canvas, 1)
        
        # add the toolbar
        
        
        self.canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.ax = self.canvas.figure.add_subplot(111)

    def get_axes(self):
        return self.ax
    
    def plot(self, x,y):
        self.ax.clear()
        self.ax.plot(x, y, 'r')
    
    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()
        

        
    

        
        
        
        
        
