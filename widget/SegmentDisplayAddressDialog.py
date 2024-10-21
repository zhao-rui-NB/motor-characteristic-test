from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QWidget
from PyQt6.QtCore import Qt

class SegmentDisplayAddressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.power_meter_data_keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency', 'kW_a', 'kW_b', 'kW_c', 'kW_tot', 'kvar_a', 'kvar_b', 'kvar_c', 'kvar_tot', 'kVA_a', 'kVA_b', 'kVA_c', 'kVA_tot', 'PF']
        self.power_supply_data_keys = ['voltage', 'frequency', 'current_limit', 'output', 'measure_voltage', 'measure_current', 'measure_frequency', 'measure_power', 'measure_VA', 'measure_ipeak']
        
        self.power_meter_line_edits: dict[str, QLineEdit] = {}
        self.power_supply_line_edits: dict[str, QLineEdit] = {}
        
        self.address_inputs = {}
        self.modbus_addresses = {}
        self.initUI()
        
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)

    def initUI(self):
        self.setWindowTitle('Modbus Address Configuration')
        # self.setGeometry(100, 100, 400, 600)

        self.main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.main_layout.addWidget(self.scroll_area)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        
        


        # group box for power meter
        self.pm_group = QGroupBox('Power Meter')
        self.pm_group_form = QFormLayout(self.pm_group)
        for key in self.power_meter_data_keys:
            input_field = QLineEdit()
            input_field.setPlaceholderText("0x")
            input_field.setValidator(QRegularExpressionValidator(QRegularExpression("^0x[0-9A-Fa-f]{1,2}$")))
            self.pm_group_form.addRow(key, input_field)
            self.power_meter_line_edits[key] = input_field
        self.scroll_layout.addWidget(self.pm_group)
        
        # group box for power supply
        self.ps_group = QGroupBox('Power Supply')
        self.ps_group_form = QFormLayout(self.ps_group)
        for key in self.power_supply_data_keys:
            input_field = QLineEdit()
            input_field.setPlaceholderText("0x")
            input_field.setValidator(QRegularExpressionValidator(QRegularExpression("^0x[0-9A-Fa-f]{1,2}$")))
            self.ps_group_form.addRow(key, input_field)
            self.power_supply_line_edits[key] = input_field
        self.scroll_layout.addWidget(self.ps_group)

        confirm_button = QPushButton('Confirm')
        confirm_button.clicked.connect(self.on_confirm)
        self.main_layout.addWidget(confirm_button)

    def load_settings(self,setting: dict): 
        '''
        load setting from a dictionary
        value of dictionary should be in string format
        '''
        try:
            power_meter_addresses = setting.get('power_meter', {})
            power_supply_addresses = setting.get('power_supply', {})
            
            for key, value in power_meter_addresses.items():
                self.power_meter_line_edits[key].setText(value)
                
            for key, value in power_supply_addresses.items():
                self.power_supply_line_edits[key].setText(value)
        except TypeError:
            print('[SegmentDisplayAddressDialog] load_settings: Invalid setting format, dict value should be in string format')
            
    def get_settings(self, cvt_to_int=True):
        '''
        return a dictionary of power meter and power supply addresses.
        cvt_to_int = true for converting the address from string to int
        '''
        power_meter_addresses = {key: input_field.text()  for key, input_field in self.power_meter_line_edits.items() if input_field.text()}
        power_supply_addresses = {key: input_field.text() for key, input_field in self.power_supply_line_edits.items() if input_field.text()}

        if cvt_to_int:
            power_meter_addresses = {key: int(value, 16) for key, value in power_meter_addresses.items()}
            power_supply_addresses = {key: int(value, 16) for key, value in power_supply_addresses.items()}
            
        return {'power_meter': power_meter_addresses, 'power_supply': power_supply_addresses}

    def on_confirm(self):
        self.accept()
        


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = SegmentDisplayAddressDialog()

    # load setting
    import json
    try:
        with open('[TEST]display_address_setting.json', 'r') as f:
            setting = json.load(f)
            dialog.load_settings(setting)
    except FileNotFoundError:
        print("Setting file not found")
        

    dialog.show()
    app.exec()
    
    # save setting
    setting = dialog.get_settings(cvt_to_int=False)
    print("Setting:", setting)
    if setting:
        with open('[TEST]display_address_setting.json', 'w') as f:
            json.dump(setting, f)
        
    sys.exit()
    
    