from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from ui_main import ui_main

from widget.logic.MotorMonitor import MotorMonitor
from widget.logic.PowerSupplyControlPanel import PowerSupplyControlPanel
from widget.logic.MotorParameter import MotorParameter

from engine.DeviceManager import DeviceManager
from engine.DataCollector import DataCollector
from engine.DataSender import DataSender

class MotorTestSysetm:
    def __init__(self):
        self.ui = ui_main()
        self.ui.setGeometry(0, 0, 1400, 900)
        self.ui.show()
        
        self.device_manager:DeviceManager = DeviceManager()
        
        self.data_collector:DataCollector = DataCollector(self.device_manager)
        self.data_sender:DataSender = DataSender(self.device_manager, self.data_collector)
        
        self.motor_monitor = MotorMonitor(self.ui.motor_monitor_ui)
        self.power_supply_control_panel = PowerSupplyControlPanel(self.ui.power_ui, self.device_manager)
        self.motor_parameter = MotorParameter(self.ui.motor_parameter_ui)
        
        
        self.data_collector.register_power_meter_data_callback(self.motor_monitor.update_power_meter_data)
        self.data_collector.register_power_supply_data_callback(self.power_supply_control_panel.update_power_supply_info)
        self.data_collector.register_torque_sensor_data_callback(self.motor_monitor.update_torque_sensor_data)
        # test calculate efficiency
        self.data_collector.register_calculated_data_callback(self.motor_monitor.update_calculated_data)

        self.ui.connection_menu.triggered.connect(self.setting_device)
    
    def setting_device(self):
        self.ui.ConnectionDialog.load_settings()
        resault = self.ui.ConnectionDialog.exec()
        ### setting device and start data collection and data sending ###
        if resault == QDialog.DialogCode.Accepted:
            self.data_collector.stop()
            self.device_config = self.ui.ConnectionDialog.get_settings()
            settings = self.device_config
            self.device_manager.init_power_meter(settings["PowerMeter"]["COMPort"], settings["PowerMeter"]["SlaveAddress"])
            self.device_manager.init_power_supply(settings["PowerSupply"]["IPAddress"], settings["PowerSupply"]["Port"])
            
            seg_disp_addr_list = []
            seg_disp_addr_list.extend([addr for addr in settings["SegmentDisplay"]["Addresses"]["power_meter"].values()])
            seg_disp_addr_list.extend([addr for addr in settings["SegmentDisplay"]["Addresses"]["power_supply"].values()])
            self.device_manager.init_segment_displays(settings["SegmentDisplay"]["COMPort"], seg_disp_addr_list)
            
            print(settings)
            
            self.data_collector.start()
            self.data_sender.start_display_sender(settings["SegmentDisplay"]["Addresses"])
            
            
        
    def __del__(self):
        self.device_manager.release_resources()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    window = MotorTestSysetm()
    app.exec()
