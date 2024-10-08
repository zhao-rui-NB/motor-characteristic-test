from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import time
import json

import threading
from widget.ui.ui_MotorMonitor import ui_MotorMornitor
from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.ModbusWorker import ModbusWorker

class MotorMonitor():
    def __init__(self, ui: ui_MotorMornitor):
        super().__init__()
        self.ui = ui
        
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_power_meter) 
    
        # self.timer.start(500)
    
    def update_power_meter_data(self, data):
        
        name_pairs = [
            ('電壓_RS', 'Vll_ab'),
            ('電壓_ST', 'Vll_bc'),
            ('電壓_TR', 'Vll_ca'),
            ('平均線電壓', 'Vll_avg'),
            
            ('電壓_R', 'Vln_a'),
            ('電壓_S', 'Vln_b'),
            ('電壓_T', 'Vln_c'),
            ('平均相電壓', 'Vln_avg'),
            
            ('電流_R', 'I_a'),
            ('電流_S', 'I_b'),
            ('電流_T', 'I_c'),
            ('平均電流', 'I_avg'),
            
            ('功率_R', 'kW_a'),
            ('功率_S', 'kW_b'),
            ('功率_T', 'kW_c'),
            ('輸入功率', 'kW_tot'),
            
            ('乏功率_R', 'kvar_a'),
            ('乏功率_S', 'kvar_b'),
            ('乏功率_T', 'kvar_c'),
            ('輸入乏功率', 'kvar_tot'),
            
            ('視在功率_R', 'kVA_a'),
            ('視在功率_S', 'kVA_b'),
            ('視在功率_T', 'kVA_c'),
            ('輸入視在功率', 'kVA_tot'),
            
            ('功率因數', 'PF'),
            ('頻率', 'Frequency'),
        ]
        
        for ui, meter in name_pairs:
            if data[meter] is not None:
                self.ui.item_dict[ui].set_value(f'{data[meter]:.3f}')
            else:
                self.ui.item_dict[ui].set_value("N/A")        
    


    

if __name__ == "__main__":
    from engine.DeviceManager import DeviceManager
    from engine.DataCollector import DataCollector
    
    app = QApplication([])
    
    ui = ui_MotorMornitor()
    ctrl = MotorMonitor(ui)
    
    device_manager = DeviceManager()
    device_manager.init_power_meter("COM3", 0x0F)
    data_collector = DataCollector(device_manager)
    data_collector.register_power_meter_data_callback(ctrl.update_power_meter_data)
    data_collector.start()
    
    ui.show()
    app.exec()
    
    
            
            
            