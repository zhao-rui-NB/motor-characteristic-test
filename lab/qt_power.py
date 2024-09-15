from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from utils.PowerSupplyASP7100 import PowerSupplyASP7100

'''

class PowerSupplyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Supply Control")
        self.setGeometry(100, 100, 400, 400)

        self.power_supply = PowerSupplyASP7100("127.0.0.1", 2268)
        self.power_supply.client.wait_connect()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_control_group()
        self.create_measurement_group()

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_measurements)
        self.update_timer.start(1000)  # Update every 1 second

    def create_control_group(self):
        control_group = QGroupBox("Control")
        control_layout = QVBoxLayout()

        # Voltage control
        voltage_layout = QHBoxLayout()
        voltage_layout.addWidget(QLabel("Voltage (V):"))
        self.voltage_input = QLineEdit()
        voltage_layout.addWidget(self.voltage_input)
        self.set_voltage_button = QPushButton("Set")
        self.set_voltage_button.clicked.connect(self.set_voltage)
        voltage_layout.addWidget(self.set_voltage_button)
        control_layout.addLayout(voltage_layout)

        # Frequency control
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency (Hz):"))
        self.freq_input = QLineEdit()
        freq_layout.addWidget(self.freq_input)
        self.set_freq_button = QPushButton("Set")
        self.set_freq_button.clicked.connect(self.set_frequency)
        freq_layout.addWidget(self.set_freq_button)
        control_layout.addLayout(freq_layout)

        # Current limit control
        current_layout = QHBoxLayout()
        current_layout.addWidget(QLabel("Current Limit (A):"))
        self.current_input = QLineEdit()
        current_layout.addWidget(self.current_input)
        self.set_current_button = QPushButton("Set")
        self.set_current_button.clicked.connect(self.set_current_limit)
        current_layout.addWidget(self.set_current_button)
        control_layout.addLayout(current_layout)

        # Output control
        self.output_button = QPushButton("Output OFF")
        self.output_button.clicked.connect(self.toggle_output)
        control_layout.addWidget(self.output_button)

        control_group.setLayout(control_layout)
        self.layout.addWidget(control_group)

    def create_measurement_group(self):
        measurement_group = QGroupBox("Measurements")
        measurement_layout = QVBoxLayout()

        self.voltage_label = QLabel("Voltage: N/A")
        self.current_label = QLabel("Current: N/A")
        self.power_label = QLabel("Power: N/A")
        self.apparent_power_label = QLabel("Apparent Power: N/A")

        measurement_layout.addWidget(self.voltage_label)
        measurement_layout.addWidget(self.current_label)
        measurement_layout.addWidget(self.power_label)
        measurement_layout.addWidget(self.apparent_power_label)

        measurement_group.setLayout(measurement_layout)
        self.layout.addWidget(measurement_group)

    def set_voltage(self):
        voltage = float(self.voltage_input.text())
        self.power_supply.set_voltage(voltage)

    def set_frequency(self):
        frequency = float(self.freq_input.text())
        self.power_supply.set_frequency(frequency)

    def set_current_limit(self):
        current = float(self.current_input.text())
        self.power_supply.set_current_limit(current)

    def toggle_output(self):
        current_state = self.power_supply.get_output()[0]
        new_state = not current_state
        self.power_supply.set_output(new_state)
        self.output_button.setText("Output ON" if new_state else "Output OFF")

    def update_measurements(self):
        voltage = self.power_supply.measure_voltage()[0]
        current = self.power_supply.measure_current()[0]
        power = self.power_supply.measure_power()[0]
        apparent_power = self.power_supply.measure_apparent_power()[0]

        self.voltage_label.setText(f"Voltage: {voltage:.2f} V")
        self.current_label.setText(f"Current: {current:.2f} A")
        self.power_label.setText(f"Power: {power:.2f} W")
        self.apparent_power_label.setText(f"Apparent Power: {apparent_power:.2f} VA")


'''



class Ui_PowerSupplyControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Supply Control")
        self.setGeometry(100, 100, 800, 600)

        # Set the default font for the entire application
        default_font = QFont("Arial", 20)
        self.setFont(default_font)

        self.setupUi()


    def setupUi(self):
        
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())
        
        self.create_control_group()
        self.create_measurement_group()      

    def create_control_row(self, label_text):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        read_label = QLabel("N/A")
        read_label.setFont(QFont("Arial", 20))
        read_label.setStyleSheet("background-color: #94ADDB; padding: 5px; border: 1px solid #CCCCCC; border-radius: 5px;")
        read_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        read_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        
        input_field = QLineEdit()
        input_field.setFont(QFont("Arial", 20))
        input_field.setStyleSheet("padding: 5px;")
        input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        input_field.setValidator(QDoubleValidator())
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        set_button = QPushButton("Set")
        set_button.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        set_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px;")
        set_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        return label, read_label, input_field, set_button 
        
    def create_control_group(self):
        control_group = QGroupBox("Control")
        control_group.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        control_layout = QGridLayout(control_group)
        control_layout.setColumnStretch(0, 4)
        control_layout.setColumnStretch(1, 2)
        control_layout.setColumnStretch(2, 2)# empty column
        control_layout.setColumnStretch(3, 2)
        control_layout.setColumnStretch(4, 1)

        # Voltage control
        volt = self.create_control_row("Voltage (V):")
        self.control_volt_read_label = volt[1]
        self.control_volt_input = volt[2]
        self.control_volt_set_button = volt[3]
        control_layout.addWidget(volt[0], 0, 0)
        control_layout.addWidget(volt[1], 0, 1)
        control_layout.addWidget(volt[2], 0, 3)
        control_layout.addWidget(volt[3], 0, 4)
                
        # Frequency control
        freq = self.create_control_row("Frequency (Hz):")
        self.control_freq_read_label = freq[1]
        self.control_freq_input = freq[2]
        self.control_freq_set_button = freq[3]
        control_layout.addWidget(freq[0], 1, 0)
        control_layout.addWidget(freq[1], 1, 1)
        control_layout.addWidget(freq[2], 1, 3)
        control_layout.addWidget(freq[3], 1, 4)
        
        # Current limit control
        curr = self.create_control_row("Current Limit (A):")
        self.control_curr_read_label = curr[1]
        self.control_curr_input = curr[2]
        self.control_curr_set_button = curr[3]
        control_layout.addWidget(curr[0], 2, 0)
        control_layout.addWidget(curr[1], 2, 1)
        control_layout.addWidget(curr[2], 2, 3)
        control_layout.addWidget(curr[3], 2, 4)

        # Output control
        self.output_button = QPushButton("Output OFF")
        self.output_button.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.output_button.setStyleSheet("background-color: #FF6B6B; color: white; padding: 10px;")
        control_layout.addWidget(self.output_button, 3, 0, 1, 5)

        self.main_layout.addWidget(control_group)


    def create_measurement_row(self, text):
        layout = QHBoxLayout()
        
        label = QLabel(text)
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(label,1)

        value_label = QLabel("N/A")
        value_label.setFont(QFont("Arial", 20))
        value_label.setStyleSheet("background-color: #94ADDB; padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label, 1)
        
        return layout, value_label


    def create_measurement_group(self):
        measurement_group = QGroupBox("Measurements")
        measurement_group.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        measurement_layout = QVBoxLayout()
        measurement_group.setLayout(measurement_layout)
        
        
        volt = self.create_measurement_row("Voltage:")
        curr = self.create_measurement_row("Current:")
        power = self.create_measurement_row("Power:")
        app_power = self.create_measurement_row("Apparent Power:")
        
        measurement_layout.addLayout(volt[0])
        measurement_layout.addLayout(curr[0])
        measurement_layout.addLayout(power[0])
        measurement_layout.addLayout(app_power[0])
        
        self.meas_volt_label = volt[1]
        self.meas_curr_label = curr[1]
        self.meas_power_label = power[1]
        self.meas_app_power_label = app_power[1]

        self.main_layout.addWidget(measurement_group)



class PowerSupplyControlPanel(Ui_PowerSupplyControlPanel):
    def __init__(self):
        super().__init__()
        
        self.power = PowerSupplyASP7100("127.0.0.1", 2268)
        # self.ui = Ui_PowerSupplyControlPanel()
        # self.show()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)
        
        self.num = 10
        
        self.control_volt_set_button.clicked.connect(self.set_voltage)
        self.control_freq_set_button.clicked.connect(self.set_frequency)
        self.control_curr_set_button.clicked.connect(self.set_current_limit)
        self.output_button.clicked.connect(self.toggle_output)
        
    
    
    #close enent
    def closeEvent(self, event: QCloseEvent):
        self.timer.stop()
        self.power.client.stop()
        event.accept()
    
    def update_info(self):
        # self.control_volt_read_label.setText(f'{self.num}')
        
        resp = self.power.get_voltage()
        if resp: self.control_volt_read_label.setText(f'{resp[0]:.3f} V')
        else: self.control_volt_read_label.setText("N/A")
        
            
        resp = self.power.get_frequency()
        if resp: self.control_freq_read_label.setText(f'{resp[0]:.3f} Hz')
        else: self.control_freq_read_label.setText("N/A")
        
        resp = self.power.get_current_limit()
        if resp: self.control_curr_read_label.setText(f'{resp[0]:.3f} A')
        else: self.control_curr_read_label.setText("N/A")
        

        
        resp = self.power.measure_source()
        if resp:
            self.meas_volt_label.setText(f'{resp[0]:.3f} V')
            self.meas_curr_label.setText(f'{resp[1]:.3f} A')
            self.meas_power_label.setText(f'{resp[3]:.3f} W')
            self.meas_app_power_label.setText(f'{resp[4]:.3f} VA')
        else:
            self.meas_volt_label.setText("N/A")
            self.meas_curr_label.setText("N/A")
            self.meas_power_label.setText("N/A")
            self.meas_app_power_label.setText("N/A")
        
        
        resp = self.power.get_output()
        if resp: 
            of_state = resp[0]
            if of_state:
                
                self.output_button.setStyleSheet("background-color: #06937A; color: white; padding: 10px;")
            else:
                self.output_button.setStyleSheet("background-color: #FFE497; color: black; padding: 10px;")
                
                
            self.output_button.setText("Output ON" if of_state else "Output OFF")
        else: 
            self.output_button.setText("Output unknown")
            self.output_button.setStyleSheet("background-color: #B1AFAF; color: white; padding: 10px;")
                
            
            

        

    def set_voltage(self):
        try:
            voltage = float(self.control_volt_input.text())
        except ValueError:
            return            
        self.power.set_voltage(voltage)
        self.control_volt_input.clear()
    
    def set_frequency(self):
        try:
            freq = float(self.control_freq_input.text())
        except ValueError:
            return
        self.power.set_frequency(freq)
        self.control_freq_input.clear()
    
    def set_current_limit(self):
        try:
            curr = float(self.control_curr_input.text())
        except ValueError:
            return
        self.power.set_current_limit(curr)
        self.control_curr_input.clear()
    
    def toggle_output(self):
        
        current_state = self.power.get_output()[0]
        new_state = not current_state
        self.power.set_output(new_state)
        self.output_button.setText("Output ON" if new_state else "Output OFF")
        
    
    

if __name__ == "__main__":
    app = QApplication([])
    
    
    # window = Ui_PowerSupplyControlPanel()
    # window.show()
    
    window = PowerSupplyControlPanel()
    window.show()
    
    
    
    app.exec()
    
    