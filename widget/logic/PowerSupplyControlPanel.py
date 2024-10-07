from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from engine.DeviceManager import DeviceManager
from widget.ui.ui_PowerSupplyControlPanel import Ui_PowerSupplyControlPanel

class PowerSupplyControlPanel():
    def __init__(self, ui:Ui_PowerSupplyControlPanel, device_manager: DeviceManager):
        super().__init__()
        self.ui = ui
        self.device = device_manager
        
        self.ui.control_volt_set_button.clicked.connect(self._ps_set_voltage)
        self.ui.control_freq_set_button.clicked.connect(self._ps_set_frequency)
        self.ui.control_curr_set_button.clicked.connect(self._ps_set_current_limit)
        self.ui.output_on_button.clicked.connect(self._ps_output_on)
        self.ui.output_off_button.clicked.connect(self._ps_output_off)
        
        
    def update_power_supply_info(self, data):
        text = f'{data["voltage"]:.3f} V' if data["voltage"] is not None else "N/A"
        self.ui.control_volt_read_label.setText(text)
        
        text = f'{data["frequency"]:.3f} Hz' if data["frequency"] is not None else "N/A"
        self.ui.control_freq_read_label.setText(text)
        
        text = f'{data["current_limit"]:.3f} A' if data["current_limit"] is not None else "N/A"
        self.ui.control_curr_read_label.setText(text)
        
        if data["output"] is not None:
            if data["output"]:
                self.ui.output_state_label.setText("Output is ON")
                self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style + self.ui.output_state_label_add_style_on)
            else:
                self.ui.output_state_label.setText("Output is OFF")
                self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style + self.ui.output_state_label_add_style_off)
        else:
            self.ui.output_state_label.setText("Output is unknown")
            self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style)

        text = f'{data["measure_voltage"]:.3f} V' if data["measure_voltage"] is not None else "N/A"
        self.ui.meas_volt_label.setText(text)
        
        text = f'{data["measure_current"]:.3f} A' if data["measure_current"] is not None else "N/A"
        self.ui.meas_curr_label.setText(text)
        
        text = f'{data["measure_power"]:.3f} W' if data["measure_power"] is not None else "N/A"
        self.ui.meas_power_label.setText(text)
        
        text = f'{data["measure_VA"]:.3f} VA' if data["measure_VA"] is not None else "N/A"
        self.ui.meas_app_power_label.setText(text)
        
                    
        
    def _ps_set_voltage(self):
        try:
            voltage = float(self.ui.control_volt_input.text())
        except ValueError:
            return            
        self.device.power_supply.set_voltage(voltage, None)
        self.ui.control_volt_input.clear()
        
    def _ps_set_frequency(self):
        try:
            freq = float(self.ui.control_freq_input.text())
        except ValueError:
            return
        self.device.power_supply.set_frequency(freq, None)
        self.ui.control_freq_input.clear()
        
    def _ps_set_current_limit(self):
        try:
            curr = float(self.ui.control_curr_input.text())
        except ValueError:
            return
        self.device.power_supply.set_current_limit(curr, None)
        self.ui.control_curr_input.clear()
    
    def _ps_output_on(self):
        self.device.power_supply.set_output(1, None)
        
    def _ps_output_off(self):
        self.device.power_supply.set_output(0, None)
        

if __name__ == "__main__":
    from engine.DeviceManager import DeviceManager
    from engine.DataCollector import DataCollector
    
    
    
    device_manager = DeviceManager()
    device_manager.init_power_supply("127.0.0.1", 2268)
    data_collector = DataCollector(device_manager)
    
    app = QApplication([])
    
    ui = Ui_PowerSupplyControlPanel()
    window = PowerSupplyControlPanel(ui, device_manager)
    
    
    
    data_collector.register_power_supply_data_callback(window.update_power_supply_info)
    data_collector.start()    
    
    window.ui.show()
    
    app.exec()
    
    