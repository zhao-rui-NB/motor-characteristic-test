from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


from widget.ui.ui_PowerSupplyControlPanel import Ui_PowerSupplyControlPanel
from widget.ui.ui_MotorTestSystem import Ui_MotorTestSystem

from widget.ui.ui_MotorTestMenu import Ui_MotorTestMenu

from widget.ui.ui_MotorMonitor import ui_MotorMornitor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motor Test System")
        
        
        # power supply control panel dock
        self.power_dock = QDockWidget("PowerSupplyControlPanel", self)
        self.power_ui = Ui_PowerSupplyControlPanel()
        self.power_dock.setWidget(self.power_ui)
        self.power_dock.visibilityChanged.connect(self.update_menu_display_status)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.power_dock, Qt.Orientation.Vertical)
        
        
        # motor test system dock 
        # self.motor_menu_dock = QDockWidget("MotorTest", self)
        # self.motor_ui = Ui_MotorTestSystem()
        # self.motor_menu_dock.setWidget(self.motor_ui)
        # self.motor_menu_dock.visibilityChanged.connect(self.update_menu_display_status)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.motor_menu_dock)
        
        # motor test menu dock
        self.motor_menu_dock = QDockWidget("MotorTestMenu", self)
        self.motor_menu_ui = Ui_MotorTestMenu()
        self.motor_menu_dock.setWidget(self.motor_menu_ui)
        self.motor_menu_dock.visibilityChanged.connect(self.update_menu_display_status)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.motor_menu_dock)
        
        # motor monitor dock
        self.motor_monitor_dock = QDockWidget("MotorMonitor", self)
        self.motor_monitor_ui = ui_MotorMornitor()
        self.motor_monitor_dock.setWidget(self.motor_monitor_ui)
        self.motor_monitor_dock.visibilityChanged.connect(self.update_menu_display_status)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.motor_monitor_dock)
        
        
        
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.mainlayout = QVBoxLayout(self.main_widget)
        
        
        label = QLabel("Motor Test System")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainlayout.addWidget(label)
        
        self.setup_menu_bar()
    
    def setup_menu_bar(self):
        # menu bar 
        self.menu_bar = self.menuBar()
        
        ## file menu
        self.file_menu = self.menu_bar.addMenu("File")

        ## display menu
        self.display_menu = self.menu_bar.addMenu("Display")

        self.power_supply_action = QAction("power_supply")
        self.power_supply_action.setCheckable(True)
        self.power_supply_action.triggered.connect(self.on_power_supply_action)
        self.display_menu.addAction(self.power_supply_action)
        
        self.motor_test_system_action = QAction("MotorTestSystem")
        self.motor_test_system_action.setCheckable(True)
        self.motor_test_system_action.triggered.connect(self.on_motor_test_system_action)
        self.display_menu.addAction(self.motor_test_system_action)
        
        self.motor_monitor_action = QAction("MotorMonitor")
        self.motor_monitor_action.setCheckable(True)
        self.motor_monitor_action.triggered.connect(self.motor_monitor_dock.setVisible)
        self.display_menu.addAction(self.motor_monitor_action)

    
        
        ## about menu
        self.about_menu = self.menu_bar.addMenu("About")
        
    
    
    def update_menu_display_status(self):
        self.power_supply_action.setChecked(self.power_dock.isVisible())
        self.motor_test_system_action.setChecked(self.motor_menu_dock.isVisible())
        self.motor_monitor_action.setChecked(self.motor_monitor_dock.isVisible())


    
    def on_power_supply_action(self, checked):
        self.power_dock.setVisible(checked)

    def on_motor_test_system_action(self, checked):
        self.motor_menu_dock.setVisible(checked)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    
    # window.ui.show()
    
    app.exec()    
    
    
    