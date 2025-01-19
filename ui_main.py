from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


from widget.ui.ui_PowerSupplyControlPanel import Ui_PowerSupplyControlPanel
# from widget.ui.ui_MotorTestSystem import Ui_MotorTestSystem

from widget.ui.ui_MotorTestMenu import Ui_MotorTestMenu

from widget.ui.ui_MotorMonitor import ui_MotorMornitor

from widget.ui.ui_MotorParameter import Ui_MotorParameter
from widget.logic.MotorParameter import MotorParameter

from widget.ConnectionDialog import ConnectionDialog


class ui_main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # font size 24
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        

        
        self.setWindowTitle("Motor Test System")
        
        self.ConnectionDialog = ConnectionDialog(self)
        
        
        # power supply control panel dock
        # self.power_dock = QDockWidget("PowerSupplyControlPanel", self)
        # self.power_ui = Ui_PowerSupplyControlPanel()
        # self.power_dock.setWidget(self.power_ui)
        # self.power_dock.visibilityChanged.connect(self.update_menu_display_status)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.power_dock, Qt.Orientation.Vertical)
        
        # motor test menu dock
        self.motor_menu_dock = QDockWidget("MotorTestMenu", self)
        self.motor_menu_ui = Ui_MotorTestMenu()
        self.motor_menu_dock.setWidget(self.motor_menu_ui)
        self.motor_menu_dock.visibilityChanged.connect(self.update_menu_display_status)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.motor_menu_dock)
        
        # motor monitor dock
        # self.motor_monitor_dock = QDockWidget("MotorMonitor", self)
        # self.motor_monitor_ui = ui_MotorMornitor()
        # self.motor_monitor_dock.setWidget(self.motor_monitor_ui)
        # self.motor_monitor_dock.visibilityChanged.connect(self.update_menu_display_status)
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.motor_monitor_dock)
        
        
        
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.mainlayout = QVBoxLayout(self.main_widget)
        
        
        # label
        label = QLabel("高雄科技大學電機系\n馬達特性測試系統")
        # label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainlayout.addWidget(label)
        
        # motor parameter edit
        self.motor_parameter_ui = Ui_MotorParameter()
        self.motor_parameter = MotorParameter(self.motor_parameter_ui)
        self.mainlayout.addWidget(self.motor_parameter_ui)

        self.setup_menu_bar()
    
    def setup_menu_bar(self):
        
        # menu bar 
        self.menu_bar = self.menuBar()
        
        # set font size 20
        font = QFont()
        font.setPointSize(18)
        self.menu_bar.setFont(font)
        
        ## connection menu
        self.connection_menu = self.menu_bar.addAction("Connection")
        self.connection_menu.setFont(font)
        
        
        ## file menu
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.setFont(font)
        self.file_new = self.file_menu.addAction("New")
        self.file_open = self.file_menu.addAction("Load")
        self.file_save = self.file_menu.addAction("Save")
        self.file_save_as = self.file_menu.addAction("Save As")
        
        self.file_new.triggered.connect(self.motor_parameter.new_file)
        self.file_open.triggered.connect(self.motor_parameter.load_from_file)
        self.file_save.triggered.connect(self.motor_parameter.save_file)
        self.file_save_as.triggered.connect(self.motor_parameter.save_as_file)
        
        

        ## display menu
        self.display_menu = self.menu_bar.addMenu("Display")

        # self.power_supply_action = QAction("power_supply")
        # self.power_supply_action.setFont(font)
        # self.power_supply_action.setCheckable(True)
        # self.power_supply_action.triggered.connect(self.power_dock.setVisible)
        # self.display_menu.addAction(self.power_supply_action)
        
        self.motor_test_system_action = QAction("MotorTestSystem")
        self.motor_test_system_action.setFont(font)
        self.motor_test_system_action.setCheckable(True)
        self.motor_test_system_action.triggered.connect(self.motor_menu_dock.setVisible)
        self.display_menu.addAction(self.motor_test_system_action)
        
        # self.motor_monitor_action = QAction("MotorMonitor")
        # self.motor_monitor_action.setFont(font)
        # self.motor_monitor_action.setCheckable(True)
        # self.motor_monitor_action.triggered.connect(self.motor_monitor_dock.setVisible)
        # self.display_menu.addAction(self.motor_monitor_action)

    
        
        ## about menu
        self.about_menu = self.menu_bar.addAction("About")
        
    def update_menu_display_status(self):
        # self.power_supply_action.setChecked(self.power_dock.isVisible())
        self.motor_test_system_action.setChecked(self.motor_menu_dock.isVisible())
        # self.motor_monitor_action.setChecked(self.motor_monitor_dock.isVisible())



if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = ui_main()
    window.show()
    
    # window.ui.show()
    
    app.exec()    
    
    
    