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
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(5)
        
        self.query_meter_func = None
        
    def set_query_meter_func(self, query_meter_func):
        self.query_meter_func = query_meter_func
    
    def update_info(self):
        # ui to meter
        UI2METER = {
            '電壓_RS': 'Vll_ab',
            '電壓_ST': 'Vll_bc',
            '電壓_TR': 'Vll_ca',
            '平均線電壓': 'Vll_avg',
            
            '電壓_R': 'Vln_a',
            '電壓_S': 'Vln_b',
            '電壓_T': 'Vln_c',
            '平均相電壓': 'Vln_avg',
            
            
            '電流_R': 'I_a',
            '電流_S': 'I_b',
            '電流_T': 'I_c',
            '平均電流': 'I_avg',
            '功率_R': 'kW_a',
            '功率_S': 'kW_b',
            '功率_T': 'kW_c',
            '輸入功率': 'kW_tot',
            '乏功率_R': 'kvar_a',
            '乏功率_S': 'kvar_b',
            '乏功率_T': 'kvar_c',
            '輸入乏功率': 'kvar_tot',
            '視在功率_R': 'kVA_a',
            '視在功率_S': 'kVA_b',
            '視在功率_T': 'kVA_c',
            '輸入視在功率': 'kVA_tot',
            # '轉速': 'Frequency',
            # '轉矩': 'Frequency',
            # '輸出功率': 'Frequency',
            # '效率': 'Frequency',
            '功率因數': 'PF',
            '頻率': 'Frequency',
        }
        
        if self.query_meter_func is None:
            return
        
        meter_data = self.query_meter_func()
        
        for name in self.ui.item_names: # update all item in ui
            if name in UI2METER and UI2METER[name] in meter_data and meter_data[UI2METER[name]] is not None:
                self.ui.item_dict[name].set_value(f'{meter_data[UI2METER[name]]:.3f}')
            else:
                self.ui.item_dict[name].set_value("N/A")
                
if __name__ == "__main__":  
    
    class test_engine(QObject):
        def __init__(self):
            super().__init__()
            
            self.modbus_worker = ModbusWorker(port='COM3', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5)
            self.modbus_worker.start()
            
            self.powermeter = PowerMeterSPM3(self.modbus_worker, slave_address=0x0F)
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_meter_info)
            self.timer.start(500)
            
            self.meter_data = {}
            
            
        def get_meter_data(self):
            return self.meter_data
        
        def _meter_callback(self, data):
            self.meter_data.update(data)
                        
        def update_meter_info(self):
            # print(self.modbus_worker.get_task_count())
            self.powermeter.read_vcfp(self._meter_callback)
                
    
    
    app = QApplication([])
    
    test = test_engine()
    
    
    ui = ui_MotorMornitor()
    ctrl = MotorMonitor(ui)
    ctrl.set_query_meter_func(test.get_meter_data)


    
    ui.show()
    app.exec()
    
    
            
            
            