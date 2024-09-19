from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


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


if __name__ == "__main__":
    app = QApplication([])
    window = Ui_PowerSupplyControlPanel()
    window.show()
    app.exec()
