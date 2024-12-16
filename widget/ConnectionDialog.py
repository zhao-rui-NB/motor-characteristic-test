from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import json

from .SegmentDisplayAddressDialog import SegmentDisplayAddressDialog

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # self.setModal(True)
        self.setFont(QFont("Arial", 20))
        
        self.setWindowTitle('Device Settings')
        self.setMinimumSize(400, 500)
        
        self.initUI()
        self.segment_display_dialog: SegmentDisplayAddressDialog = SegmentDisplayAddressDialog()
        
        self.pm_com_port.returnPressed.connect(self.accept)
        self.pm_slave_address.returnPressed.connect(self.accept)
        self.ps_ip.returnPressed.connect(self.accept)
        self.ps_port.returnPressed.connect(self.accept)
        
        self.set_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.config_display_address_button.clicked.connect(self.config_display_address)
        
        self.apply_style()
        
    def initUI(self):
        
        self.out_widget = QWidget(self)
        # self.out_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        
        self.main_layout = QVBoxLayout(self)
        # self.out_widget.setLayout(self.main_layout)


        ## Power Meter Group
        self.pm_group = QGroupBox("Power Meter")
        self.pm_layout = QFormLayout(self.pm_group)
        # self.pm_layout.setSpacing(40)
        self.main_layout.addWidget(self.pm_group)        
        
        self.pm_com_port = QLineEdit()
        self.pm_com_port.setPlaceholderText("COMx")
        self.pm_layout.addRow(QLabel("COM Port:"), self.pm_com_port)
        
        
        self.pm_slave_address = QLineEdit()
        self.pm_slave_address.setPlaceholderText("0x")
        hex_validator = QRegularExpressionValidator(QRegularExpression("^0x[0-9A-Fa-f]{1,2}$"))
        self.pm_slave_address.setValidator(hex_validator)
        self.pm_layout.addRow(QLabel("Slave Address:"), self.pm_slave_address)
    
        ## Power Supply Group
        self.ps_group = QGroupBox("Power Supply")
        self.ps_layout = QFormLayout(self.ps_group)
        # self.ps_layout.setSpacing(40)
        self.main_layout.addWidget(self.ps_group)
        
        self.ps_ip = QLineEdit()
        self.ps_ip.setPlaceholderText("xxx.xxx.xxx.xxx")
        ip_validator = QRegularExpressionValidator(QRegularExpression("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"))
        self.ps_ip.setValidator(ip_validator)
        self.ps_layout.addRow(QLabel("IP Address:"), self.ps_ip)
        
        self.ps_port = QLineEdit()
        self.ps_port.setPlaceholderText("xxxx")
        self.ps_port.setValidator(QIntValidator())
        self.ps_layout.addRow(QLabel("Port:"), self.ps_port)
        
        ## SegmentDisplay Group
        self.sd_group = QGroupBox("Segment Display")
        self.sd_layout = QFormLayout(self.sd_group)
        # self.sd_layout.setSpacing(40)
        self.main_layout.addWidget(self.sd_group)
        
        self.sd_com_port = QLineEdit()
        self.sd_com_port.setPlaceholderText("COMx")
        self.sd_layout.addRow(QLabel("COM Port:"), self.sd_com_port)
        self.config_display_address_button = QPushButton("Configure Display Addresses")
        self.sd_layout.addRow(self.config_display_address_button)
        
        ## TorqueSensor Group
        self.ts_group = QGroupBox("Torque Sensor")
        self.ts_layout = QFormLayout(self.ts_group)
        # self.ts_layout.setSpacing(40)
        self.main_layout.addWidget(self.ts_group)
        
        self.ts_com_port = QLineEdit()
        self.ts_com_port.setPlaceholderText("COMx")
        self.ts_layout.addRow(QLabel("COM Port:"), self.ts_com_port)
        
        self.ts_slave_address = QLineEdit()
        self.ts_slave_address.setPlaceholderText("0x")
        hex_validator = QRegularExpressionValidator(QRegularExpression("^0x[0-9A-Fa-f]{1,2}$"))
        self.ts_slave_address.setValidator(hex_validator)
        self.ts_layout.addRow(QLabel("Slave Address:"), self.ts_slave_address)
        
        
        
        ## Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")

        self.set_button = QPushButton("SET")
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.set_button)
        self.main_layout.addLayout(button_layout)

    def apply_style(self):
        # self.setStyleSheet("""

        #     QLineEdit {
        #         border: 3px solid #57756e;
        #         padding: 0px 10px;
        #         border-radius: 15px;
        #         background-color: #1a1a1a;
        #         color: #ffffff;
        #     }
            
        #     QLineEdit:focus { border-color: #5a49ff; background-color: #711b79; }
        #     QLineEdit:hover { border-color: #5a49ff; border-width: 5px; }
            
            
            
        #     QPushButton#set_button, QPushButton#cancel_button {
        #         color: white;
        #         padding: 10px 20px;
        #         border-radius: 15px;
        #         font-weight: bold;
        #     }

        #     QPushButton#set_button { background-color: #12e232; }
        #     QPushButton#set_button:hover { background-color: #07b221; border: 6px solid #ffeeff;}
        #     QPushButton#set_button:focus {  border: 6px solid #ffeeff; outline: none;}
        #     QPushButton#set_button:pressed { background-color: #0a8b1e; }
            
        #     QPushButton#cancel_button { background-color: #f73c3c; }
        #     QPushButton#cancel_button:hover { background-color: #db1a1a; border: 6px solid #ffeeff;}
        #     QPushButton#cancel_button:focus {  border: 6px solid #ffeeff; outline: none;}
        #     QPushButton#cancel_button:pressed { background-color: #c01515; }
        # """)
    

        self.cancel_button.setObjectName("cancel_button")
        self.set_button.setObjectName("set_button")
        
    def config_display_address(self):
        self.segment_display_dialog.exec()

    # def resizeEvent(self, event: QResizeEvent):

    #     font_size = max(10, int(event.size().height() * 0.03))
    #     self.base_font.setPointSize(font_size)
    #     self.setFont(self.base_font)
        
    #     self.out_widget.setGeometry(
    #         0,
    #         0,
    #         event.size().width(),
    #         event.size().height()
    #     )

    #     # all children set font 
    #     for child in self.findChildren(QWidget):
    #         child.setFont(self.font())
    
    def save_settings(self):
        settings = self.get_settings(cvt_to_int=False)
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
    
    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings: dict = json.load(f)
            self.pm_com_port.setText(settings["PowerMeter"]["COMPort"])
            self.pm_slave_address.setText(settings["PowerMeter"]["SlaveAddress"])          
            
            self.ps_ip.setText(settings["PowerSupply"]["IPAddress"])
            self.ps_port.setText(settings["PowerSupply"]["Port"])
            
            display_settings: dict = settings.get("SegmentDisplay", {})
            self.sd_com_port.setText(display_settings.get("COMPort", ""))
            self.segment_display_dialog.load_settings(display_settings.get("Addresses", {}))

        except FileNotFoundError as e:
            self.set_to_default()
            print(e)
                        
    def set_to_default(self):
        self.pm_com_port.setText("COM3")
        self.pm_slave_address.setText("0x0F")
        self.ps_ip.setText("127.0.0.1")
        self.ps_port.setText("2268")
        
    def get_settings(self, cvt_to_int=True):
        '''
        when save and load to json config file, will store raw string from QLineEdit
        when get dialog return value, will convert to int, cvt_to_int=True
        '''
        js = {
            "PowerMeter": {
                "COMPort": self.pm_com_port.text(),
                "SlaveAddress": self.pm_slave_address.text()
            },
            "PowerSupply": {
                "IPAddress": self.ps_ip.text(),
                "Port": self.ps_port.text()
            },
            "SegmentDisplay": {
                "COMPort": self.sd_com_port.text(),
                "Addresses": self.segment_display_dialog.get_settings(cvt_to_int=cvt_to_int)
            }
            
        }
        
        if cvt_to_int:
            js["PowerMeter"]["SlaveAddress"] = int(js["PowerMeter"]["SlaveAddress"], 16)
            js["PowerSupply"]["Port"] = int(js["PowerSupply"]["Port"])
        
        return js
            
    def accept(self):
        self.save_settings()
        super().accept()
        
        
if __name__ == '__main__':
    app = QApplication([])
    dialog = ConnectionDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("Accepted")
        print('no int:', dialog.get_settings(cvt_to_int=False))
        print('int:', dialog.get_settings(cvt_to_int=True))
    else:
        print("Rejected")