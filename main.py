from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui_main import ui_main

from widget.logic.MotorMonitor import MotorMonitor
from widget.logic.PowerSupplyControlPanel import PowerSupplyControlPanel
from widget.logic.MotorParameter import MotorParameter

from engine.DeviceManager import DeviceManager
from engine.DataCollector import DataCollector

class MotorTestSysetm:
    def __init__(self):
        self.ui = ui_main()
        self.ui.setGeometry(0, 0, 1400, 900)
        self.ui.show()
        
        self.device_manager = DeviceManager()
        # self.device_manager.init_power_meter("COM3", 0x0F)
        # self.device_manager.init_power_supply("127.0.0.1", 2268)
        
        self.data_collector = DataCollector(self.device_manager)
        
        self.motor_monitor = MotorMonitor(self.ui.motor_monitor_ui)
        self.power_supply_control_panel = PowerSupplyControlPanel(self.ui.power_ui, self.device_manager)
        self.motor_parameter = MotorParameter(self.ui.motor_parameter_ui)
        
        
        self.data_collector.register_power_meter_data_callback(self.motor_monitor.update_power_meter_data)
        self.data_collector.register_power_supply_data_callback(self.power_supply_control_panel.update_power_supply_info)
        # self.data_collector.start()
        
        # self.
        self.ui.connection_menu.triggered.connect(self.setting_device)
    
    def setting_device(self):
        resault = self.ui.ConnectionDialog.exec()
        if resault == QDialog.DialogCode.Accepted:
            self.data_collector.stop()
            
            settings = self.ui.ConnectionDialog.get_settings()
            self.device_manager.init_power_meter(settings["PowerMeter"]["COMPort"], settings["PowerMeter"]["SlaveAddress"])
            self.device_manager.init_power_supply(settings["PowerSupply"]["IPAddress"], settings["PowerSupply"]["Port"])
            
            self.data_collector.start()
        
    def __del__(self):
        self.device_manager.release_resources()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = MotorTestSysetm()
    app.exec()
