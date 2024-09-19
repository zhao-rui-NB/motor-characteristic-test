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
        
        self.ui.control_volt_set_button.clicked.connect(self.set_voltage)
        self.ui.control_freq_set_button.clicked.connect(self.set_frequency)
        self.ui.control_curr_set_button.clicked.connect(self.set_current_limit)
        self.ui.output_button.clicked.connect(self.toggle_output)
        
    
    
    #close enent
    def closeEvent(self, event: QCloseEvent):
        self.timer.stop()
        self.power.client.stop()
        event.accept()
    
    def update_info(self):
        
        resp = self.power.get_voltage()
        if resp: self.ui.control_volt_read_label.setText(f'{resp[0]:.3f} V')
        else: self.ui.control_volt_read_label.setText("N/A")
        
            
        resp = self.power.get_frequency()
        if resp: self.ui.control_freq_read_label.setText(f'{resp[0]:.3f} Hz')
        else: self.ui.control_freq_read_label.setText("N/A")
        
        resp = self.power.get_current_limit()
        if resp: self.ui.control_curr_read_label.setText(f'{resp[0]:.3f} A')
        else: self.ui.control_curr_read_label.setText("N/A")
        

        
        resp = self.power.measure_source()
        if resp:
            self.ui.meas_volt_label.setText(f'{resp[0]:.3f} V')
            self.ui.meas_curr_label.setText(f'{resp[1]:.3f} A')
            self.ui.meas_power_label.setText(f'{resp[3]:.3f} W')
            self.ui.meas_app_power_label.setText(f'{resp[4]:.3f} VA')
        else:
            self.ui.meas_volt_label.setText("N/A")
            self.ui.meas_curr_label.setText("N/A")
            self.ui.meas_power_label.setText("N/A")
            self.ui.meas_app_power_label.setText("N/A")
        
        
        resp = self.power.get_output()
        if resp: 
            of_state = resp[0]
            if of_state:
                
                self.ui.output_button.setStyleSheet("background-color: #06937A; color: white; padding: 10px;")
            else:
                self.ui.output_button.setStyleSheet("background-color: #FFE497; color: black; padding: 10px;")
                
                
            self.ui.output_button.setText("Output ON" if of_state else "Output OFF")
        else: 
            self.ui.output_button.setText("Output unknown")
            self.ui.output_button.setStyleSheet("background-color: #B1AFAF; color: white; padding: 10px;")
                
        

    def set_voltage(self):
        try:
            voltage = float(self.ui.control_volt_input.text())
        except ValueError:
            return            
        self.power.set_voltage(voltage)
        self.ui.control_volt_input.clear()
    
    def set_frequency(self):
        try:
            freq = float(self.ui.control_freq_input.text())
        except ValueError:
            return
        self.power.set_frequency(freq)
        self.ui.control_freq_input.clear()
    
    def set_current_limit(self):
        try:
            curr = float(self.ui.control_curr_input.text())
        except ValueError:
            return
        self.power.set_current_limit(curr)
        self.ui.control_curr_input.clear()
    
    def toggle_output(self):
        
        current_state = self.power.get_output()[0]
        new_state = not current_state
        self.power.set_output(new_state)
        self.ui.output_button.setText("Output ON" if new_state else "Output OFF")
        
    


if __name__ == "__main__":
    app = QApplication([])
    
    
    # window = Ui_PowerSupplyControlPanel()
    # window.show()
    
    power = PowerSupplyASP7100('127.0.0.1', 2268)
    
    
    ui = Ui_PowerSupplyControlPanel()
    window = PowerSupplyControlPanel(ui, power)
    
    
    window.ui.show()
    
    app.exec()
    
    