import time 
import json
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from threading import Thread
from engine.DeviceManager import DeviceManager
# from engine.DataCollector import DataCollector
from engine.DataSender import DataSender
from engine.Motor import Motor


from gui.ui.main_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # set title
        self.setWindowTitle('馬達測試系統')
        
        self.motor:Motor = Motor()
        
        self.saved_flag = True
        self.update_file_save_status(True)
        

        ### side bar buttons signal
        # page btn
        self.btn_connect.clicked.connect(lambda: self.switch_page(0))
        self.btn_motor_parameter.clicked.connect(lambda : self.switch_page(1))
        self.btn_auto_test.clicked.connect(lambda : self.switch_page(2))
        self.btn_test_result.clicked.connect(lambda : self.switch_page(3))
        self.btn_manual_monitoring.clicked.connect(lambda : self.switch_page(4))
        self.switch_page(1)
        
        # file btn
        self.btn_save.clicked.connect(self.on_save_project)
        self.btn_open.clicked.connect(self.on_open_project)
        self.btn_new.clicked.connect(self.on_new_project)
        
        # motor parameter
        # set all line edit input check 
        self.lineEdit_para_rated_voltage.setValidator(QDoubleValidator())
        self.lineEdit_para_rated_current.setValidator(QDoubleValidator())
        self.lineEdit_para_horsepower.setValidator(QDoubleValidator())
        self.lineEdit_para_no_load_current.setValidator(QDoubleValidator())
        self.lineEdit_para_poles.setValidator(QIntValidator())
        self.lineEdit_para_frequency.setValidator(QDoubleValidator())
        self.lineEdit_para_power_phases.setValidator(QIntValidator())
        self.lineEdit_para_speed.setValidator(QDoubleValidator())
        
        self.lineEdit_para_rated_voltage.editingFinished.connect(lambda: self.on_motor_parameter_edited('rated_voltage', self.lineEdit_para_rated_voltage.text()))
        self.lineEdit_para_rated_current.editingFinished.connect(lambda: self.on_motor_parameter_edited('rated_current', self.lineEdit_para_rated_current.text()))
        self.lineEdit_para_horsepower.editingFinished.connect(lambda: self.on_motor_parameter_edited('horsepower', self.lineEdit_para_horsepower.text()))
        self.lineEdit_para_no_load_current.editingFinished.connect(lambda: self.on_motor_parameter_edited('no_load_current', self.lineEdit_para_no_load_current.text()))
        self.lineEdit_para_poles.editingFinished.connect(lambda: self.on_motor_parameter_edited('poles', self.lineEdit_para_poles.text()))
        self.lineEdit_para_frequency.editingFinished.connect(lambda: self.on_motor_parameter_edited('frequency', self.lineEdit_para_frequency.text()))
        self.lineEdit_para_power_phases.editingFinished.connect(lambda: self.on_motor_parameter_edited('power_phases', self.lineEdit_para_power_phases.text()))
        self.lineEdit_para_speed.editingFinished.connect(lambda: self.on_motor_parameter_edited('speed', self.lineEdit_para_speed.text()))
    
        
    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        button_list = [self.btn_connect, self.btn_motor_parameter, self.btn_auto_test, self.btn_test_result, self.btn_manual_monitoring]
        for i, button in enumerate(button_list):
            button.setChecked(i == index)
            
    ##############################################################################
    # Motor Parameter page
    ##############################################################################            
    def on_motor_parameter_edited(self, parameter_name, value):
        self.update_file_save_status(False)
        succ = self.motor.update_motor_parameter(parameter_name, value)
        # read back the value to make sure it is updated
        self.update_motor_parameter()
        
        if not succ and value!='':
            QMessageBox.critical(self, 'Error', '請輸入正確的數值')
        
    def update_motor_parameter(self):
        # update the ui motor parameter from the motor class
        self.lineEdit_para_rated_voltage.setText(str(self.motor.rated_voltage) if self.motor.rated_voltage else '')
        self.lineEdit_para_rated_current.setText(str(self.motor.rated_current) if self.motor.rated_current else '')
        self.lineEdit_para_horsepower.setText(str(self.motor.horsepower) if self.motor.horsepower else '')
        self.lineEdit_para_no_load_current.setText(str(self.motor.no_load_current) if self.motor.no_load_current else '')
        self.lineEdit_para_poles.setText(str(self.motor.poles) if self.motor.poles else '')
        self.lineEdit_para_frequency.setText(str(self.motor.frequency) if self.motor.frequency else '')
        self.lineEdit_para_power_phases.setText(str(self.motor.power_phases) if self.motor.power_phases else '')
        self.lineEdit_para_speed.setText(str(self.motor.speed) if self.motor.speed else '')
        

    
    
    ##############################################################################
    # File operation
    ##############################################################################
    def update_file_save_status(self, saved):
        self.saved_flag = saved
        # footer status bar
        self.statusbar.showMessage('專案未儲存' if not saved else '')
    # save or load the project
    def on_save_project(self):
        motor_json = self.motor.to_dict()
        timestamp = self.motor.make_time_stamp()
        # a save dialog to save the file
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Project', f'{timestamp}.motor.json', 'MOTOR JSON File (*.motor.json)')
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(motor_json, f, indent=4)
            self.update_file_save_status(True)
    
    def on_open_project(self):
        if not self.saved_flag:
            reply = QMessageBox.question(self, 'Save Project', 'Do you want to save the current project?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.on_save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
            # else no need to save the current project
            
        # a open dialog to open the file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Project', '', 'MOTOR JSON File (*.motor.json)')
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)
                self.motor.from_dict(data)
                self.update_motor_parameter()
            self.update_file_save_status(True)
                
    def on_new_project(self):
        if not self.saved_flag:
            reply = QMessageBox.question(self, 'Save Project', 'Do you want to save the current project?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Yes:
                self.on_save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
            # else no need to save the current project
        
        # create a new motor object
        self.motor = Motor()
        self.update_motor_parameter()
        self.update_file_save_status(True)
        
                
    

        


    
        



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    # app.setStyle('Windows')
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())