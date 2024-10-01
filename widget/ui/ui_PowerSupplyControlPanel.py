from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Ui_PowerSupplyControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power Supply Control")
        self.setGeometry(100, 100, 800, 600)
        
        self.setFont(QFont("Arial", 20))
        
        self.setupUi()
    # def resizeEvent(self, event):
    #     self.default_font.setPointSize(max(10, int(self.height() * 0.05)))
    #     self.setFont(self.default_font)
    #     super().resizeEvent(event)
        

    def setupUi(self):
        self.center_widget = QWidget(self)
        self.center_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        self.main_layout = QVBoxLayout(self.center_widget)
        
        self.create_control_group()
        self.create_measurement_group()      
    

    def resizeEvent(self, event: QResizeEvent):
        
        ratio_limit = 1.1
        
        new_width = self.width() # fix the width
        new_height = self.height()
        new_height = min(new_height, int(new_width * ratio_limit))
        
        self.center_widget.setGeometry(
            int(event.size().width() - new_width) // 2,
            int(event.size().height() - new_height) // 2,
            new_width,
            new_height
        )
        

        ns = max(10, int(new_height * 0.04))
        self.setFont(QFont("Arial", ns, QFont.Weight.Light))
        
        for child in self.findChildren(QWidget):
            child.setFont(self.font())
    
    def create_control_row(self, label_text):
        label = QLabel(label_text, self)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        read_label = QLabel("N/A")
        read_label.setStyleSheet("background-color: #94ADDB; padding: 5px; border: 1px solid #CCCCCC; border-radius: 5px;")
        read_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        read_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        
        input_field = QLineEdit()
        input_field.setStyleSheet("*{padding: 5px;} QLineEdit:hover , QLineEdit:focus  {border: 6px solid #FF00FF;border-radius: 10px;}")
        input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        input_field.setValidator(QDoubleValidator())
        input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        set_button = QPushButton("Set")
        set_button.setStyleSheet("*{background-color: #4CAF50; color: white;} QPushButton:hover , QPushButton:focus {border: 6px solid #FF00FF;border-radius: 10px;}")
        set_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # when line edit press enter, click set button
        input_field.returnPressed.connect(set_button.click)
        
        return label, read_label, input_field, set_button 
        
    def create_control_group(self):
        control_group = QGroupBox("Control")
        control_layout = QGridLayout(control_group)
        control_layout.setColumnStretch(0, 4)
        control_layout.setColumnStretch(1, 2)
        control_layout.setColumnStretch(2, 2)# empty column
        control_layout.setColumnStretch(3, 2)
        control_layout.setColumnStretch(4, 1)
        # no padding
        control_layout.setHorizontalSpacing(5)
        

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
        self.output_state_label = QLabel("Output is known")
        self.output_state_label_default_style = 'border-radius: 5px; padding: 5px;'
        self.output_state_label_add_style_on = 'background-color: #FFD700; color: #000000;'
        self.output_state_label_add_style_off = 'background-color: #E0E0E0; color: #757575;'
        self.output_state_label.setStyleSheet(self.output_state_label_default_style)
        self.output_state_label.setAutoFillBackground(True)
        self.output_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(self.output_state_label, 3, 0, 1, 2)
        
        
        self.output_on_button = QPushButton("ON")
        self.output_on_button.setStyleSheet("*{background-color: #4CAF50; color: white;} QPushButton:hover, QPushButton:focus {border: 6px solid #FF00FF;border-radius: 10px;}")                                    
        self.output_on_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        self.output_off_button = QPushButton("OFF")
        self.output_off_button.setStyleSheet("*{background-color: #FF6B6B; color: white;} QPushButton:hover, QPushButton:focus {border: 6px solid #FF00FF;border-radius: 10px;}")
        self.output_off_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        onoff_layout = QHBoxLayout()
        
        # onoff_layout.setSpacing(5)
        onoff_layout.addWidget(self.output_on_button)
        onoff_layout.addWidget(self.output_off_button)
        
        control_layout.addLayout(onoff_layout, 3, 3, 1, 2)  
        
        self.main_layout.addWidget(control_group)


    def create_measurement_row(self, text):
        layout = QHBoxLayout()
        
        label = QLabel(text)
        layout.addWidget(label,1)

        value_label = QLabel("N/A")
        value_label.setStyleSheet("background-color: #94ADDB; padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label, 1)
        
        return layout, value_label

    def create_measurement_group(self):
        measurement_group = QGroupBox("Measurements")
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
