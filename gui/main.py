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
from engine.DataCollector import DataCollector
from engine.Motor import Motor
from engine.TestRunner import TestRunner


from gui.ui.main_ui import Ui_MainWindow
from gui.qthread_tasks import Qthread_test_delay, Qthread_run_dc_resistance_test, Qthread_run_open_circuit_test, Qthread_run_lock_rotor_test, Qthread_run_load_test, Qthread_run_separate_excitation_test, Qthread_run_frequency_drift_test

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('馬達測試系統')
        
        self.task_running_mode(False)
        
        # connect all signals
        self.signal_connect()
        
        
        self.motor:Motor = Motor()
        self.device_manager = DeviceManager()
        self.data_collector = DataCollector(self.device_manager)
        self.data_sender = DataSender(self.device_manager)
        self.test_runner = TestRunner(self.device_manager)


        self.auto_test_qthread: QThread = None


        
        self.device_manager.load_devices_from_ini('device.ini')
        self.data_collector.start() # start the data collector
        self.data_sender.start_plc_electric_data_sender()
        # timer for manual monitoring
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.on_update_manual_monitoring)
        self.monitor_timer.start(500)
        
        self.saved_flag = True
        self.update_file_save_status(True)
        


    def signal_connect(self):
        
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
        
        # auto test manual btn
        self.btn_dc_resistance_test.clicked.connect(self.on_dc_resistance_clicked)
        self.btn_no_load_test.clicked.connect(self.on_no_load_test_clicked)
        self.btn_lock_rotor_test.clicked.connect(self.on_lock_rotor_test_clicked)
        self.btn_load_test.clicked.connect(self.on_load_test_clicked)
        self.btn_separate_excitation_test.clicked.connect(self.on_separate_excitation_test_clicked)
        self.btn_frequency_drift_test.clicked.connect(self.on_frequency_drift_test_clicked)
        self.btn_auto_test_stop.clicked.connect(self.on_auto_task_stop_clicked)
        
        # test connect page btn
        self.btn_Test_PlcElectrical.clicked.connect(self.on_test_PlcElectrical)
        self.btn_Test_PlcMechanical.clicked.connect(self.on_test_PlcMechanical)
        self.btn_Test_PowerMeter.clicked.connect(self.on_test_PowerMeter)
        self.btn_Test_PowerSupply.clicked.connect(self.on_test_PowerSupply)
        
        self.btn_con_reconnect.clicked.connect(self.on_reconnect)
        self.btn_con_test_clear.clicked.connect(self.on_connect_test_clear)
        self.btn_con_test_all.clicked.connect(self.on_connect_test_all)     
        
        # manual monitoring page
        # setValidator
        self.lineEdit_manual_plc_mechanical_break.setValidator(QIntValidator())
        
        self.lineEdit_manual_power_supply_ac.setValidator(QDoubleValidator())
        self.lineEdit_manual_power_supply_dc_offect.setValidator(QDoubleValidator())
        self.lineEdit_manual_power_supply_current.setValidator(QDoubleValidator())
        self.lineEdit_manual_power_supply_frequency.setValidator(QDoubleValidator())
        
        self.lineEdit_manual_power_supply_phase_angle.setValidator(QDoubleValidator())
                
        
        # panel connect signal
        # plc mechanical
        self.btn_manual_plc_mechanical_break.clicked.connect(self.on_btn_manual_plc_mechanical_break)
        # plc electric
        self.btn_manual_plc_electric_ps_single.clicked.connect(self.on_btn_manual_plc_electric_ps_single)
        self.btn_manual_plc_electric_ps_three.clicked.connect(self.on_btn_manual_plc_electric_ps_three)
        self.btn_manual_plc_electric_ps_off.clicked.connect(self.on_btn_manual_plc_electric_ps_off)
        self.btn_manual_plc_electric_output_single.clicked.connect(self.on_btn_manual_plc_electric_output_single)
        self.btn_manual_plc_electric_output_three.clicked.connect(self.on_btn_manual_plc_electric_output_three)
        self.btn_manual_plc_electric_output_off.clicked.connect(self.on_btn_manual_plc_electric_output_off)
        # power meter
        self.btn_manual_power_meter_clear.clicked.connect(self.on_btn_manual_power_meter_clear)
        self.btn_manual_power_meter_reset.clicked.connect(self.on_btn_manual_power_meter_reset)
        # power supply
        self.btn_manual_power_supply_clear.clicked.connect(self.on_btn_manual_power_supply_clear)
        self.btn_manual_power_supply_reset.clicked.connect(self.on_btn_manual_power_supply_reset)
        self.btn_manual_power_supply_output_on.clicked.connect(self.on_btn_manual_power_supply_output_on)
        self.btn_manual_power_supply_output_off.clicked.connect(self.on_btn_manual_power_supply_output_off)
        
        self.btn_manual_power_supply_ac.clicked.connect(self.on_btn_manual_power_supply_ac)
        self.btn_manual_power_supply_dc_offect.clicked.connect(self.on_lineEdit_manual_power_supply_dc_offect)
        self.btn_manual_power_supply_current.clicked.connect(self.on_lineEdit_manual_power_supply_current)
        self.btn_manual_power_supply_frequency.clicked.connect(self.on_lineEdit_manual_power_supply_frequency)
        
        self.btn_manual_power_supply_phase_wire_3P4W.clicked.connect(self.on_btn_manual_power_supply_phase_wire_3P4W)
        self.btn_manual_power_supply_phase_wire_1P2W.clicked.connect(self.on_btn_manual_power_supply_phase_wire_1P2W)
        self.btn_manual_power_supply_phase_wire_1P3W.clicked.connect(self.on_btn_manual_power_supply_phase_wire_1P3W)        
        
        self.btn_manual_power_supply_mode_acdc.clicked.connect(self.on_btn_manual_power_supply_mode_acdc)
        self.btn_manual_power_supply_mode_ac.clicked.connect(self.on_btn_manual_power_supply_mode_ac)
        self.btn_manual_power_supply_mode_dc.clicked.connect(self.on_btn_manual_power_supply_mode_dc)
        
        self.btn_manual_power_supply_edit_each.clicked.connect(self.on_btn_manual_power_supply_edit_each)
        self.btn_manual_power_supply_edit_all.clicked.connect(self.on_btn_manual_power_supply_edit_all)
        
        self.btn_manual_power_supply_edit_L1.clicked.connect(self.on_btn_manual_power_supply_edit_L1)
        self.btn_manual_power_supply_edit_L2.clicked.connect(self.on_btn_manual_power_supply_edit_L2)
        self.btn_manual_power_supply_edit_L3.clicked.connect(self.on_btn_manual_power_supply_edit_L3)
        
        self.btn_manual_power_supply_unbalance.clicked.connect(self.on_btn_manual_power_supply_unbalance)
        self.btn_manual_power_supply_balance.clicked.connect(self.on_btn_manual_power_supply_balance)
        
        self.btn_manual_power_supply_phase_angle_L12.clicked.connect(self.on_btn_manual_power_supply_phase_angle_L12)
        self.btn_manual_power_supply_phase_angle_L13.clicked.connect(self.on_btn_manual_power_supply_phase_angle_L13)
        
        
        
        
        
    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        button_list = [self.btn_connect, self.btn_motor_parameter, self.btn_auto_test, self.btn_test_result, self.btn_manual_monitoring]
        for i, button in enumerate(button_list):
            button.setChecked(i == index)
    
    ##############################################################################
    # connect page
    ##############################################################################
    def on_connect_test_clear(self):
        self.lb_PlcElectrical_test.setText('尚未測試')
        self.lb_PlcMechanical_test.setText('尚未測試')
        self.lb_PowerMeter_test.setText('尚未測試')
        self.lb_PowerSupply_test.setText('尚未測試')
        
    def on_reconnect(self):
        self.device_manager.load_devices_from_ini('device.ini')
        self.data_sender.start_plc_electric_data_sender()
        self.on_connect_test_clear()
        
    def on_connect_test_all(self):
        self.on_test_PlcElectrical()
        self.on_test_PlcMechanical()
        self.on_test_PowerMeter()
        self.on_test_PowerSupply()
        
    def on_test_PlcElectrical(self):
        self.lb_PlcElectrical_test.setText('測試中...')
        try:
            r1 = self.device_manager.plc_electric.get_is_ps_output_single()
            r2 = self.device_manager.plc_electric.get_is_ps_output_three()
            self.lb_PlcElectrical_test.setText('測試成功')
            print(f'PlcElectrical test: {r1} {r2}')
        except:
            self.lb_PlcElectrical_test.setText('測試失敗')
        
    def on_test_PlcMechanical(self):
        self.lb_PlcMechanical_test.setText('測試中...')
        try:
            r1 = self.device_manager.plc_mechanical.get_mechanical_data()
            self.lb_PlcMechanical_test.setText('測試成功')
            print(f'PlcMechanical test: {r1}')
        except:
            self.lb_PlcMechanical_test.setText('測試失敗')
        
    def on_test_PowerMeter(self):
        self.lb_PowerMeter_test.setText('測試中...')
        r1 = self.device_manager.power_meter.get_serial_number()
        if not r1 or not r1[0]:
            self.lb_PowerMeter_test.setText('測試失敗')
        else:
            self.lb_PowerMeter_test.setText('測試成功')
        
    def on_test_PowerSupply(self):
        self.lb_PowerSupply_test.setText('測試中...')
        r1 = self.device_manager.power_supply.get_idn()
        if not r1 or not r1[0]:
            self.lb_PowerSupply_test.setText('測試失敗')
        else:
            self.lb_PowerSupply_test.setText('測試成功')
        
    
    
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
        
    
    ##############################################################################
    # Auto Test page
    ##############################################################################
    def task_running_mode(self, running):
        # disable all the buttons
        self.btn_dc_resistance_test.setEnabled(not running)
        self.btn_no_load_test.setEnabled(not running)
        self.btn_lock_rotor_test.setEnabled(not running)
        self.btn_separate_excitation_test.setEnabled(not running)
        self.btn_frequency_drift_test.setEnabled(not running)
        self.btn_load_test.setEnabled(not running)

        self.btn_auto_test_stop.setEnabled(running)
    
    def on_dc_resistance_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '直流阻抗測試\n待測馬達請<脫離>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_dc_resistance_test(self.test_runner, self.motor)
            # self.auto_test_qthread = Qthread_test_delay(self.test_runner, self.motor, 8) # for test
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
    def on_no_load_test_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '無載測試\n待測馬達請<脫離>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_open_circuit_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
    def on_lock_rotor_test_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '堵轉測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_lock_rotor_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
    def on_load_test_clicked(self): 
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '負載測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_load_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
    def on_separate_excitation_test_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '鐵損分離測試\n待測馬達請<脫離>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_separate_excitation_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
    def on_frequency_drift_test_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '頻率漂移測試\n待測馬達請<脫離>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_frequency_drift_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
        
    def on_auto_task_stop_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            self.auto_test_qthread.terminate()
            self.task_running_mode(False)
        
    def on_auto_test_task_done(self, succ):
        self.task_running_mode(False)
        if succ:
            QMessageBox.information(self, 'Success', '測試完成')
        else:
            QMessageBox.critical(self, 'Error', '測試失敗')
            
        self.update_test_result_page()
        
        
    ##############################################################################
    # Test Result page
    ##############################################################################
    def update_test_result_page(self):
        # update the test result page to ui
        
        # dc resistance
        self.lineEdit_dc_resistance_result.setText(str(self.motor.result_dc_resistance))
        
        open_v = str(self.motor.result_open_circuit.get('voltage')) if self.motor.result_open_circuit else ''
        open_i = str(self.motor.result_open_circuit.get('current')) if self.motor.result_open_circuit else ''
        open_p = str(self.motor.result_open_circuit.get('power')) if self.motor.result_open_circuit else ''
        self.lineEdit_open_v.setText(open_v)
        self.lineEdit_open_i.setText(open_i)
        self.lineEdit_open_p.setText(open_p)
        
        lock_v = str(self.motor.result_locked_rotor.get('voltage')) if self.motor.result_locked_rotor else ''
        lock_i = str(self.motor.result_locked_rotor.get('current')) if self.motor.result_locked_rotor else ''
        lock_p = str(self.motor.result_locked_rotor.get('power')) if self.motor.result_locked_rotor else ''
        self.lineEdit_lock_v.setText(lock_v)
        self.lineEdit_lock_i.setText(lock_i)
        self.lineEdit_lock_p.setText(lock_p)
        
        
        ###### todo load, separate_excitation, frequency_drift
        ###### figure update
        
        
    ##############################################################################
    # Manual Monitoring page
    ##############################################################################
    def on_update_manual_monitoring(self):
        # update the manual monitoring page to ui
        power_meter_data = self.data_collector.get_power_meter_data()
        plc_mechanical_data = self.data_collector.get_plc_mechanical_data()
        
        if power_meter_data:
            self.lcdNumber_V1.display(power_meter_data.get('V1') if power_meter_data.get('V1') else 0)
            self.lcdNumber_V2.display(power_meter_data.get('V2') if power_meter_data.get('V2') else 0)
            self.lcdNumber_V3.display(power_meter_data.get('V3') if power_meter_data.get('V3') else 0)
            self.lcdNumber_VS.display(power_meter_data.get('V_SIGMA') if power_meter_data.get('V_SIGMA') else 0)
            
            self.lcdNumber_I1.display(power_meter_data.get('I1') if power_meter_data.get('I1') else 0)
            self.lcdNumber_I2.display(power_meter_data.get('I2') if power_meter_data.get('I2') else 0)
            self.lcdNumber_I3.display(power_meter_data.get('I3') if power_meter_data.get('I3') else 0)
            self.lcdNumber_IS.display(power_meter_data.get('I_SIGMA') if power_meter_data.get('I_SIGMA') else 0)
            
            self.lcdNumber_P1.display(power_meter_data.get('P1') if power_meter_data.get('P1') else 0)
            self.lcdNumber_P2.display(power_meter_data.get('P2') if power_meter_data.get('P2') else 0)
            self.lcdNumber_P3.display(power_meter_data.get('P3') if power_meter_data.get('P3') else 0)
            self.lcdNumber_PS.display(power_meter_data.get('P_SIGMA') if power_meter_data.get('P_SIGMA') else 0)
            
            self.lcdNumber_S1.display(power_meter_data.get('S1') if power_meter_data.get('S1') else 0)
            self.lcdNumber_S2.display(power_meter_data.get('S2') if power_meter_data.get('S2') else 0)
            self.lcdNumber_S3.display(power_meter_data.get('S3') if power_meter_data.get('S3') else 0)
            self.lcdNumber_SS.display(power_meter_data.get('S_SIGMA') if power_meter_data.get('S_SIGMA') else 0)
            
            self.lcdNumber_Q1.display(power_meter_data.get('Q1') if power_meter_data.get('Q1') else 0)
            self.lcdNumber_Q2.display(power_meter_data.get('Q2') if power_meter_data.get('Q2') else 0)
            self.lcdNumber_Q3.display(power_meter_data.get('Q3') if power_meter_data.get('Q3') else 0)
            self.lcdNumber_QS.display(power_meter_data.get('Q_SIGMA') if power_meter_data.get('Q_SIGMA') else 0)
            
            self.lcdNumber_VF.display(power_meter_data.get('FU1') if power_meter_data.get('FU1') else 0)
            
        if plc_mechanical_data:
            self.lcdNumber_SPEED.display(plc_mechanical_data.get('speed') if plc_mechanical_data.get('speed') else 0)
            self.lcdNumber_TORQUE.display(plc_mechanical_data.get('torque') if plc_mechanical_data.get('torque') else 0)
            
    ## manual control panel
    
    # plc mechanical
    def on_btn_manual_plc_mechanical_break(self):
        if not self.lineEdit_manual_plc_mechanical_break.text():
            return
        self.device_manager.plc_mechanical.set_break(int(self.lineEdit_manual_plc_mechanical_break.text()))
        self.lineEdit_manual_plc_mechanical_break.setText('')
    # plc electric
    def on_btn_manual_plc_electric_ps_single(self):
        self.device_manager.plc_electric.set_ps_output_single()
    def on_btn_manual_plc_electric_ps_three(self):
        self.device_manager.plc_electric.set_ps_output_three()
    def on_btn_manual_plc_electric_ps_off(self):
        self.device_manager.plc_electric.set_ps_output_off()
    
    def on_btn_manual_plc_electric_output_single(self):
        self.device_manager.plc_electric.set_motor_output_single()
    def on_btn_manual_plc_electric_output_three(self):
        self.device_manager.plc_electric.set_motor_output_three()
    def on_btn_manual_plc_electric_output_off(self):
        self.device_manager.plc_electric.set_motor_output_off()
    # power meter
    def on_btn_manual_power_meter_clear(self):
        self.device_manager.power_meter.clear_status()
    def on_btn_manual_power_meter_reset(self):
        self.device_manager.power_meter.reset()
    # power supply
    def on_btn_manual_power_supply_clear(self):
        self.device_manager.power_supply.clear_status()
    def on_btn_manual_power_supply_reset(self):
        self.device_manager.power_supply.reset()
        
    def on_btn_manual_power_supply_output_on(self):
        self.device_manager.power_supply.set_output(1)
    def on_btn_manual_power_supply_output_off(self):
        self.device_manager.power_supply.set_output(0)
    
    def on_btn_manual_power_supply_ac(self):
        if not self.lineEdit_manual_power_supply_ac.text():
            return
        self.device_manager.power_supply.set_voltage(float(self.lineEdit_manual_power_supply_ac.text()))
        self.lineEdit_manual_power_supply_ac.setText('')
        
    def on_lineEdit_manual_power_supply_dc_offect(self):
        if not self.lineEdit_manual_power_supply_dc_offect.text():
            return
        self.device_manager.power_supply.set_voltage_offset(float(self.lineEdit_manual_power_supply_dc_offect.text()))
        self.lineEdit_manual_power_supply_dc_offect.setText('')
        
    def on_lineEdit_manual_power_supply_current(self):
        if not self.lineEdit_manual_power_supply_current.text():
            return
        self.device_manager.power_supply.set_current_limit(float(self.lineEdit_manual_power_supply_current.text()))
        self.lineEdit_manual_power_supply_current.setText('')
        
    def on_lineEdit_manual_power_supply_frequency(self):
        if not self.lineEdit_manual_power_supply_frequency.text():
            return
        self.device_manager.power_supply.set_frequency(float(self.lineEdit_manual_power_supply_frequency.text()))
        self.lineEdit_manual_power_supply_frequency.setText('')
    
    def on_btn_manual_power_supply_phase_wire_3P4W(self):
        '''
            phase_para
            0 3P4W 
            1 1P2W 
            2 1P3W 
        '''
        self.device_manager.power_supply.set_output_phase_mode(0)
    def on_btn_manual_power_supply_phase_wire_1P2W(self):
        self.device_manager.power_supply.set_output_phase_mode(1)
    def on_btn_manual_power_supply_phase_wire_1P3W(self):
        self.device_manager.power_supply.set_output_phase_mode(2)
        
    def on_btn_manual_power_supply_mode_acdc(self):
        '''
            mode_para
                ACDC-INT    | 0 AC+DC-INT 
                AC-INT      | 1 AC-INT 
                DC-INT      | 2 DC-INT 
                ACDC-EXT    | 3 AC+DC-EXT 
                AC-EXT      | 4 AC-EXT 
                ACDC-ADD    | 5 AC+DC-ADD 
                AC-ADD      | 6 AC-ADD 
                ACDC-SYNC   | 7 AC+DC-SYNC 
                AC-SYNC     | 8 AC-SYNC  
                AC-VCA      | 9 AC-VCA 
        '''
        self.device_manager.power_supply.set_source_mode(0)
    def on_btn_manual_power_supply_mode_ac(self):
        self.device_manager.power_supply.set_source_mode(1)
    def on_btn_manual_power_supply_mode_dc(self):
        self.device_manager.power_supply.set_source_mode(2)
        
    def on_btn_manual_power_supply_edit_each(self):
        '''
            EACH 0 Each phase 
            ALL 1 All phase 
        '''
        self.device_manager.power_supply.set_instrument_edit(0)
        
    def on_btn_manual_power_supply_edit_all(self):
        self.device_manager.power_supply.set_instrument_edit(1)
        
    def on_btn_manual_power_supply_edit_L1(self):
        self.device_manager.power_supply.set_instrument_select(0)
    def on_btn_manual_power_supply_edit_L2(self):
        self.device_manager.power_supply.set_instrument_select(1)
    def on_btn_manual_power_supply_edit_L3(self):
        self.device_manager.power_supply.set_instrument_select(2)
        
    def on_btn_manual_power_supply_unbalance(self):
        self.device_manager.power_supply.set_phase_mode(0)
    def on_btn_manual_power_supply_balance(self):
        self.device_manager.power_supply.set_phase_mode(1)
        
    def on_btn_manual_power_supply_phase_angle_L12(self):
        if not self.lineEdit_manual_power_supply_phase_angle.text():
            return
        self.device_manager.power_supply.set_phase_phase(0, float(self.lineEdit_manual_power_supply_phase_angle.text()))
        self.lineEdit_manual_power_supply_phase_angle.setText('')
    def on_btn_manual_power_supply_phase_angle_L13(self):
        if not self.lineEdit_manual_power_supply_phase_angle.text():
            return
        self.device_manager.power_supply.set_phase_phase(1, float(self.lineEdit_manual_power_supply_phase_angle.text()))
        self.lineEdit_manual_power_supply_phase_angle.setText('')
    
    
    
    
    
                
    


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    # app.setStyle('Windows')
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())