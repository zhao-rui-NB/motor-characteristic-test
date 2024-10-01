from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


from widget.ui.ui_PowerSupplyControlPanel import Ui_PowerSupplyControlPanel
from utils.PowerSupplyASP7100 import PowerSupplyASP7100




class PowerSupplyControlPanel():
    def __init__(self, ui:Ui_PowerSupplyControlPanel, power_supply: PowerSupplyASP7100):
        super().__init__()
        self.ui = ui
        self.power = power_supply
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)
        
        self.ui.closeEvent = self.closeEvent
        
        self.ui.control_volt_set_button.clicked.connect(self._ps_set_voltage)
        self.ui.control_freq_set_button.clicked.connect(self._ps_set_frequency)
        self.ui.control_curr_set_button.clicked.connect(self._ps_set_current_limit)
        # self.ui.output_button.clicked.connect(self._ps_toggle_output)
        self.ui.output_on_button.clicked.connect(self._ps_output_on)
        self.ui.output_off_button.clicked.connect(self._ps_output_off)
        
        self._ps_state = {
            'voltage': None,
            'frequency': None,
            'current_limit': None,
            'output': None,
            'measure_volt': None,
            'measure_curr': None,
            'measure_power': None,
            'measure_app_power': None
            
        }        
        
    #close enent
    def closeEvent(self, event: QCloseEvent):
        self.power.stop()
    
    def _ps_voltage_callback(self, result):
        if not result: return
        self._ps_state['voltage'] = result
        text = f'{result[0]:.3f} V' if result else "N/A"
        self.ui.control_volt_read_label.setText(text)
        
    def _ps_frequency_callback(self, result):
        if not result: return
        self._ps_state['frequency'] = result
        text = f'{result[0]:.3f} Hz' if result else "N/A"
        self.ui.control_freq_read_label.setText(text)
        
    def _ps_current_limit_callback(self, result):
        if not result: return
        self._ps_state['current_limit'] = result
        text = f'{result[0]:.3f} A' if result else "N/A"
        self.ui.control_curr_read_label.setText(text)
        
    def _ps_measure_callback(self, result):
        if not result: return
        self._ps_state['measure_volt'] = result[0]
        self._ps_state['measure_curr'] = result[1]
        self._ps_state['measure_power'] = result[3]
        self._ps_state['measure_app_power'] = result[4]

        if result:
            self.ui.meas_volt_label.setText(f'{result[0]:.3f} V') 
            self.ui.meas_curr_label.setText(f'{result[1]:.3f} A')
            self.ui.meas_power_label.setText(f'{result[3]:.3f} W')
            self.ui.meas_app_power_label.setText(f'{result[4]:.3f} VA')
        else:
            self.ui.meas_volt_label.setText("N/A")
            self.ui.meas_curr_label.setText("N/A")
            self.ui.meas_power_label.setText("N/A")
            self.ui.meas_app_power_label.setText("N/A")
    
    def _ps_output_callback(self, result):
        if not result: return
        self._ps_state['output'] = result
        if result:
            of_state = result[0]

            if of_state:
                self.ui.output_state_label.setText("Output is ON")
                self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style + self.ui.output_state_label_add_style_on)                
                
            else:
                self.ui.output_state_label.setText("Output is OFF")
                self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style + self.ui.output_state_label_add_style_off)
        else:
            self.ui.output_state_label.setText("Output is unknown")
            self.ui.output_state_label.setStyleSheet(self.ui.output_state_label_default_style)
        
    def update_info(self):
        self.power.get_voltage(self._ps_voltage_callback)
        self.power.get_frequency(self._ps_frequency_callback)
        self.power.get_current_limit(self._ps_current_limit_callback)
        self.power.get_output(self._ps_output_callback)
        
        self.power.measure_source(self._ps_measure_callback)
        
    def _ps_set_voltage(self):
        try:
            voltage = float(self.ui.control_volt_input.text())
        except ValueError:
            return            
        self.power.set_voltage(voltage, None)
        self.ui.control_volt_input.clear()
        
    def _ps_set_frequency(self):
        try:
            freq = float(self.ui.control_freq_input.text())
        except ValueError:
            return
        self.power.set_frequency(freq, None)
        self.ui.control_freq_input.clear()
        
    def _ps_set_current_limit(self):
        try:
            curr = float(self.ui.control_curr_input.text())
        except ValueError:
            return
        self.power.set_current_limit(curr, None)
        self.ui.control_curr_input.clear()
        
    def _ps_toggle_output(self):
        current_state = self._ps_state['output'][0]
        # print(current_state)
        new_state = 1 if current_state == 0 else 0
        self.power.set_output(new_state, None)
        # self.ui.output_button.setText("Output ON" if new_state else "Output OFF")    
    
    def _ps_output_on(self):
        self.power.set_output(1, None)
        
    def _ps_output_off(self):
        self.power.set_output(0, None)
        
    


if __name__ == "__main__":
    app = QApplication([])
    
    
    # window = Ui_PowerSupplyControlPanel()
    # window.show()
    
    power = PowerSupplyASP7100('127.0.0.1', 2268)
    
    
    ui = Ui_PowerSupplyControlPanel()
    window = PowerSupplyControlPanel(ui, power)
    
    
    window.ui.show()
    
    app.exec()
    
    