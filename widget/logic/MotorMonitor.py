from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import time
import json

from widget.ui.ui_MotorMonitor import ui_MotorMornitor
from utils.PowerMeterSPM3 import PowerMeterSPM3


class MotorMonitor():
    def __init__(self, ui: ui_MotorMornitor):
        super().__init__()
        
        self.ui = ui
        
        self.power_meter = PowerMeterSPM3('COM3', 0x0f)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)

    def update_info(self):
        # print("update_info")
        data_dict = {}

        
        vcf = self.power_meter.read_vcf()
        if vcf:
            data_dict.update(vcf)
        
        power_resault = self.power_meter.read_power_resault()
        if power_resault:
            data_dict.update(power_resault)
        
        # ui item name to meter parameter map
        # RST is ABC
        map_dict = {
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
        
        for name in self.ui.item_names:
            if name in map_dict and map_dict[name] in data_dict:
                self.ui.item_dict[name].set_value(f'{data_dict[map_dict[name]]:.3f}')
            else:
                self.ui.item_dict[name].set_value("N/A")                
                
                
if __name__ == "__main__":  
    app = QApplication([])
    
    ui = ui_MotorMornitor()
    ctrl = MotorMonitor(ui)
    ui.show()
    
    app.exec()
    
    
            
            
            