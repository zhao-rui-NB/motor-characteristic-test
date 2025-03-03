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
from gui.qthread_tasks import *
from gui.DualOutput import DualOutput

import sys
import os



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('馬達測試系統')
        # full screen
        self.showMaximized()

        # redirect the print to textEdit_system_log
        dual_output = DualOutput(sys.stdout)
        # dual_output.update_log_signal.connect(self.on_update_log_signal)        
        sys.stdout = dual_output
        dual_output.log_updater.update_log_signal.connect(self.on_update_log_signal)
        
        self.task_running_mode(False)
        
        # connect all signals
        self.signal_connect()
        
        
        self.motor:Motor = Motor()
        self.device_manager = DeviceManager()
        self.data_collector = DataCollector(self.device_manager)
        self.data_sender = DataSender(self.device_manager)
        self.test_runner = TestRunner(self.device_manager)


        self.auto_test_qthread: QThread = None

        self.PlcElectrical_connect_ok = False
        self.PlcMechanical_connect_ok = False
        self.PowerMeter_connect_ok = False
        self.PowerSupply_connect_ok = False
        

        # timer for manual monitoring
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.on_update_manual_monitoring)
        
        self.saved_flag = True
        self.update_file_save_status(True)
        
        ############################## init 
        # self.on_connect()
        
        self.resize( self.width(), self.height() )
        #


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
        # self.btn_save_csv.clicked.connect(self.on_btn_save_csv)
        
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
        # other motor info
        # self.lineEdit_para_other1.editingFinished.connect(lambda: self.on_motor_parameter_edited('manufacturer', self.lineEdit_para_other1.text()))
        # self.lineEdit_para_other2.editingFinished.connect(lambda: self.on_motor_parameter_edited('model', self.lineEdit_para_other2.text()))
        # self.lineEdit_para_other3.editingFinished.connect(lambda: self.on_motor_parameter_edited('serial_number', self.lineEdit_para_other3.text()))
        # self.lineEdit_para_other4.editingFinished.connect(lambda: self.on_motor_parameter_edited('note', self.lineEdit_para_other4.text()))
        
        # 試驗日期 lineEdit_para_other_3
        self.lineEdit_para_other_3.editingFinished.connect(lambda: self.motor.update_motor_information('試驗日期', self.lineEdit_para_other_3.text()))
        # 檢驗員 lineEdit_para_other_4
        self.lineEdit_para_other_4.editingFinished.connect(lambda: self.motor.update_motor_information('檢驗員', self.lineEdit_para_other_4.text()))
        # 印表日期 lineEdit_para_other_5
        self.lineEdit_para_other_5.editingFinished.connect(lambda: self.motor.update_motor_information('印表日期', self.lineEdit_para_other_5.text()))
        # 電腦編號 lineEdit_para_other_6
        self.lineEdit_para_other_6.editingFinished.connect(lambda: self.motor.update_motor_information('電腦編號', self.lineEdit_para_other_6.text()))
        # 序號 lineEdit_para_other_7 
        self.lineEdit_para_other_7.editingFinished.connect(lambda: self.motor.update_motor_information('序號', self.lineEdit_para_other_7.text()))
        # 型式 lineEdit_para_other_8
        self.lineEdit_para_other_8.editingFinished.connect(lambda: self.motor.update_motor_information('型式', self.lineEdit_para_other_8.text()))
        # 工作單號 lineEdit_para_other_9
        self.lineEdit_para_other_9.editingFinished.connect(lambda: self.motor.update_motor_information('工作單號', self.lineEdit_para_other_9.text()))
        # 製造號碼 lineEdit_para_other_10
        self.lineEdit_para_other_10.editingFinished.connect(lambda: self.motor.update_motor_information('製造號碼', self.lineEdit_para_other_10.text()))
        # 廠牌 lineEdit_para_other_11
        self.lineEdit_para_other_11.editingFinished.connect(lambda: self.motor.update_motor_information('廠牌', self.lineEdit_para_other_11.text()))
        # 定子規格 lineEdit_para_other_12
        self.lineEdit_para_other_12.editingFinished.connect(lambda: self.motor.update_motor_information('定子規格', self.lineEdit_para_other_12.text()))
        # 轉子規格 lineEdit_para_other_13
        self.lineEdit_para_other_13.editingFinished.connect(lambda: self.motor.update_motor_information('轉子規格', self.lineEdit_para_other_13.text()))
        # 本線 lineEdit_para_other_14
        self.lineEdit_para_other_14.editingFinished.connect(lambda: self.motor.update_motor_information('本線', self.lineEdit_para_other_14.text()))
        # 啟動線 lineEdit_para_other_15
        self.lineEdit_para_other_15.editingFinished.connect(lambda: self.motor.update_motor_information('啟動線', self.lineEdit_para_other_15.text()))
        # 備註 plainTextEdit_para_other
        self.plainTextEdit_para_other.textChanged.connect(lambda: self.motor.update_motor_information('備註', self.plainTextEdit_para_other.toPlainText()))


        # auto test manual btn
        self.btn_dc_resistance_test.clicked.connect(self.on_dc_resistance_clicked)
            
        self.btn_no_load_test.clicked.connect(self.on_no_load_test_clicked)
        self.btn_lock_rotor_test.clicked.connect(self.on_lock_rotor_test_clicked)
        self.btn_load_test.clicked.connect(self.on_load_test_clicked)
        self.btn_separate_excitation_test.clicked.connect(self.on_separate_excitation_test_clicked)
        self.btn_frequency_drift_test.clicked.connect(self.on_frequency_drift_test_clicked)

        # lineEdit_cns_step_time setValidator int
        self.lineEdit_cns_step_time.setValidator(QIntValidator())

        # if line edit edit finish connect range not in 60-500 , set to 60

        def on_lineEdit_cns_step_time():
            if int(self.lineEdit_cns_step_time.text()) < 60:
                self.lineEdit_cns_step_time.setText('60')
            elif int(self.lineEdit_cns_step_time.text()) > 500:
                self.lineEdit_cns_step_time.setText('500')
                
        self.lineEdit_cns_step_time.editingFinished.connect(on_lineEdit_cns_step_time)
        # self.lineEdit_cns_step_time.setValidator
        self.btn_CNS_test.clicked.connect(self.on_btn_CNS14400_test_clicked)
        
        self.btn_three_phase_start_torque_test.clicked.connect(self.on_btn_3p_start_torque_test_clicked)
        self.btn_single_phase_start_torque_test.clicked.connect(self.on_btn_1p_start_torque_test_clicked)

        # self.btn_CNS_test.clicked.connect(lambda: print('HHHHHWWWW'))   
           
        self.btn_auto_test_stop.clicked.connect(self.on_auto_task_stop_clicked)


        
        # test connect page btn
        self.btn_Test_PlcElectrical.clicked.connect(self.on_test_PlcElectrical)
        self.btn_Test_PlcMechanical.clicked.connect(self.on_test_PlcMechanical)
        self.btn_Test_PowerMeter.clicked.connect(self.on_test_PowerMeter)
        self.btn_Test_PowerSupply.clicked.connect(self.on_test_PowerSupply)
        
        self.btn_con_connect.clicked.connect(self.on_connect)
        self.btn_con_disconnect.clicked.connect(self.on_disconnect)
        
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
    
    # log 
    def on_update_log_signal(self, message):
        vertical_scrollbar = self.textEdit_system_log.verticalScrollBar()
        # scrollbar_pos = vertical_scrollbar.value()
        # is_at_bottom = scrollbar_pos == vertical_scrollbar.maximum()
        
        self.textEdit_system_log.setText(self.textEdit_system_log.toPlainText() + message)
        
        # if is_at_bottom:
        #     vertical_scrollbar.setValue(vertical_scrollbar.maximum())
        # else:
        #     vertical_scrollbar.setValue(scrollbar_pos)

        vertical_scrollbar.setValue(vertical_scrollbar.maximum())
        

    # resize event , resize the figure
    
    ##############################################################################
    # connect page
    ##############################################################################
    def on_connect_test_clear(self):
        self.lb_PlcElectrical_test.setText('尚未測試')
        self.lb_PlcMechanical_test.setText('尚未測試')
        self.lb_PowerMeter_test.setText('尚未測試')
        self.lb_PowerSupply_test.setText('尚未測試')
        
    def on_connect(self):
        self.device_manager.load_devices_from_ini('device.ini')
        self.on_connect_test_clear()
        # test all the devices
        self.on_test_PlcElectrical()
        self.on_test_PlcMechanical()
        self.on_test_PowerMeter()
        self.on_test_PowerSupply()

        all_ok = self.PlcElectrical_connect_ok and self.PlcMechanical_connect_ok and self.PowerMeter_connect_ok and self.PowerSupply_connect_ok
        if all_ok:
            QMessageBox.information(self, 'Success', '連線成功')
        else:
            QMessageBox.critical(self, 'Error', '連線失敗')
        
        if all_ok:
            # for plc electric data display
            self.data_sender.start_plc_electric_data_sender()
            # for manual monitoring
            self.data_collector.start()
            self.monitor_timer.start(500)
            
            self.page_manual_monitoring.setEnabled(True)
            self.page_auto_test.setEnabled(True)
            self.frame_8.setEnabled(True)

    def on_disconnect(self):
        self.data_sender.stop_plc_electric_data_sender()
        self.monitor_timer.stop()
        self.data_collector.stop()
        
        self.device_manager.release_resources()
        self.on_connect_test_clear()
        
        QMessageBox.information(self, 'Success', '斷線成功')
        self.page_manual_monitoring.setEnabled(False)
        self.page_auto_test.setEnabled(False)
        self.frame_2.setEnabled(False)
        
        
    def on_test_PlcElectrical(self):
        self.lb_PlcElectrical_test.setText('測試中...')
        self.PlcElectrical_connect_ok = False
        try:
            r1 = self.device_manager.plc_electric.get_is_ps_output_single()
            r2 = self.device_manager.plc_electric.get_is_ps_output_three()
            self.lb_PlcElectrical_test.setText('測試成功')
            print(f'PlcElectrical test: {r1} {r2}')
            self.PlcElectrical_connect_ok = True
        except:
            self.lb_PlcElectrical_test.setText('測試失敗')
    def on_test_PlcMechanical(self):
        self.lb_PlcMechanical_test.setText('測試中...')
        self.PlcMechanical_connect_ok = False
        try:
            r1 = self.device_manager.plc_mechanical.get_mechanical_data()
            if None in r1.values():
                raise Exception('PlcMechanical test failed')
            self.lb_PlcMechanical_test.setText('測試成功')
            print(f'PlcMechanical test: {r1}')
            self.PlcMechanical_connect_ok = True
        except:
            self.lb_PlcMechanical_test.setText('測試失敗')
    def on_test_PowerMeter(self):
        self.lb_PowerMeter_test.setText('測試中...')
        self.PowerMeter_connect_ok = False
        try:
            r1 = self.device_manager.power_meter.get_serial_number()
        except:
            r1 = None
        if not r1 or not r1[0]:
            self.lb_PowerMeter_test.setText('測試失敗')
        else:
            self.lb_PowerMeter_test.setText('測試成功')
            self.PowerMeter_connect_ok = True
    def on_test_PowerSupply(self):
        self.lb_PowerSupply_test.setText('測試中...')
        self.PowerSupply_connect_ok = False
        try:
            r1 = self.device_manager.power_supply.get_idn()
        except:
            r1 = None
        if not r1 or not r1[0]:
            self.lb_PowerSupply_test.setText('測試失敗')
        else:
            self.lb_PowerSupply_test.setText('測試成功')
            self.PowerSupply_connect_ok = True
        
    
    
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
        
        # other 
        # self.lineEdit_para_other1.setText(self.motor.manufacturer if self.motor.manufacturer else '')
        # self.lineEdit_para_other2.setText(self.motor.model if self.motor.model else '')
        # self.lineEdit_para_other3.setText(self.motor.serial_number if self.motor.serial_number else '')
        # self.lineEdit_para_other4.setText(self.motor.note if self.motor.note else '')

        self.lineEdit_para_other_3.setText(self.motor.information_dict.get('試驗日期', ''))
        self.lineEdit_para_other_4.setText(self.motor.information_dict.get('檢驗員', ''))
        self.lineEdit_para_other_5.setText(self.motor.information_dict.get('印表日期', ''))
        self.lineEdit_para_other_6.setText(self.motor.information_dict.get('電腦編號', ''))
        self.lineEdit_para_other_7.setText(self.motor.information_dict.get('序號', ''))
        self.lineEdit_para_other_8.setText(self.motor.information_dict.get('型式', ''))
        self.lineEdit_para_other_9.setText(self.motor.information_dict.get('工作單號', ''))
        self.lineEdit_para_other_10.setText(self.motor.information_dict.get('製造號碼', ''))
        self.lineEdit_para_other_11.setText(self.motor.information_dict.get('廠牌', ''))
        self.lineEdit_para_other_12.setText(self.motor.information_dict.get('定子規格', ''))
        self.lineEdit_para_other_13.setText(self.motor.information_dict.get('轉子規格', ''))
        self.lineEdit_para_other_14.setText(self.motor.information_dict.get('本線', ''))
        self.lineEdit_para_other_15.setText(self.motor.information_dict.get('啟動線', ''))
        
        self.plainTextEdit_para_other.setPlainText(self.motor.information_dict.get('備註', ''))



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


        phase = 'three_phase' if self.motor.power_phases == 3 else 'single_phase'
        model = self.motor.information_dict.get('型式', '無型式')
        default_dir = f'D:/{phase}/{model}/{timestamp}'
        os.makedirs(default_dir, exist_ok=True)

        # a save dialog to save the file
        # get model
        model = self.motor.information_dict.get('型式', 'model')
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Project', f'{default_dir}/{model}_{timestamp}.motor.json', 'MOTOR JSON File (*.motor.json)')
        if file_name:
            with open(file_name, 'w', encoding='UTF8') as f:
                json.dump(motor_json, f, indent=4, ensure_ascii=False)
            
            # save csv 
            dir_path = os.path.dirname(file_name)
            self.motor.save_to_csv_files(dir_path)
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
            with open(file_name, 'r', encoding='UTF8') as f:
                data = json.load(f)
            self.motor.from_dict(data)
            self.update_motor_parameter()
            self.update_test_result_page()
            
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
        self.update_test_result_page()
        
        self.update_file_save_status(True)
    
    def on_btn_save_csv(self):
        timestamp = self.motor.make_time_stamp()
        
        # a save dialog to save the file
        # get model

        phase = 'three_phase' if self.motor.power_phases == 3 else 'single_phase'
        model = self.motor.information_dict.get('型式', 'model')
        default_dir = f'D:/{phase}/{model}/{timestamp}'

        os.makedirs(default_dir, exist_ok=True)  

        # ask user choose the directory
        dir_name = QFileDialog.getExistingDirectory(self, 'Save CSV', default_dir)
        if dir_name:
            os.makedirs(default_dir, exist_ok=True)
            self.motor.save_to_csv_files(dir_name)
            QMessageBox.information(self, 'Success', 'CSV檔案儲存成功')

    
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
        self.btn_CNS_test.setEnabled(not running)

        self.btn_single_phase_start_torque_test.setEnabled(not running)
        self.btn_three_phase_start_torque_test.setEnabled(not running)

        self.btn_auto_test_stop.setEnabled(running)
    
    def on_dc_resistance_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '直流電阻測試', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_dc_resistance_test(self.test_runner, self.motor)
            # self.auto_test_qthread = Qthread_test_delay(self.test_runner, self.motor, 8) # for test
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
            self.label_auto_test_state.setText('直流電阻測試中...')

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
            self.label_auto_test_state.setText('無載測試中...')
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
            self.label_auto_test_state.setText('堵轉測試中...')
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
            self.label_auto_test_state.setText('負載測試中...')
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
            self.label_auto_test_state.setText('鐵損分離測試中...')
    def on_frequency_drift_test_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '頻率變動測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_frequency_drift_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
            self.label_auto_test_state.setText('頻率變動測試中...')
    def on_btn_CNS14400_test_clicked(self):
        print('on_btn_CNS14400_test_clicked')
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', 'CNS14400測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.Ok:

            # get the step time 
            step_time = self.lineEdit_cns_step_time.text()
            step_time = int(step_time) if step_time else 60
            print(f'[on_btn_CNS14400_test_clicked] cns step time: {step_time}')

            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_CNS14400_test(self.test_runner, self.motor, step_time)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
            self.label_auto_test_state.setText('CNS14400測試中...')

    def on_btn_3p_start_torque_test_clicked(self):
        print('on_btn_3p_start_torque_test_clicked')
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '3相啟動轉矩測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_three_phase_starting_torque_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
            self.label_auto_test_state.setText('3相啟動轉矩測試中...')

    def on_btn_1p_start_torque_test_clicked(self):  
        print('on_btn_1p_start_torque_test_clicked')
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            QMessageBox.warning(self, 'Warning', '自動測試正在進行中')
            return
        # a msg box to confirm the test and mechanical connection
        reply = QMessageBox.question(self, '自動測試', '1相啟動轉矩測試\n待測馬達請<連接>扭矩測試系統', QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Ok:
            # disable all the buttons
            self.task_running_mode(True)
            self.auto_test_qthread = Qthread_run_single_phase_starting_torque_test(self.test_runner, self.motor)
            self.auto_test_qthread.signal_finish.connect(self.on_auto_test_task_done)
            self.auto_test_qthread.start()
            self.label_auto_test_state.setText('1相啟動轉矩測試中...')
        


    
    
    
    def on_auto_task_stop_clicked(self):
        if self.auto_test_qthread and self.auto_test_qthread.isRunning():
            self.auto_test_qthread.terminate()
            self.task_running_mode(False)
            self.label_auto_test_state.setText('測試已停止')

            # turn off the power supply
            self.device_manager.plc_electric.set_ps_output_off()
        
    def on_auto_test_task_done(self, succ):
        self.task_running_mode(False)
        if succ:
            QMessageBox.information(self, 'Success', '測試完成')
        else:
            QMessageBox.critical(self, 'Error', '測試失敗')
            
        self.update_test_result_page()
        self.label_auto_test_state.setText('請選擇右邊選單開始測試')
        
        
    ##############################################################################
    # Test Result page
    ##############################################################################
    def update_test_result_page(self):
        # analysis all the test data
        self.motor.analyze_dc_resistance()
        self.motor.analyze_open_circuit()
        self.motor.analyze_locked_rotor()
        self.motor.analyze_load_test()
        self.motor.analyze_separate_excitation()
        self.motor.analyze_frequency_drift()
        
        # update the test result page to ui
        
        # dc resistance
        self.lineEdit_dc_resistance_result.setText(str(self.motor.result_dc_resistance) if self.motor.result_dc_resistance else '')
        
        open_v = str(self.motor.result_open_circuit.get('voltage')) if self.motor.result_open_circuit else ''
        open_i = str(self.motor.result_open_circuit.get('current')) if self.motor.result_open_circuit else ''
        open_p = str(self.motor.result_open_circuit.get('power')) if self.motor.result_open_circuit else ''
        open_pf = str(self.motor.result_open_circuit.get('power_factor')) if self.motor.result_open_circuit else ''
        self.lineEdit_open_v.setText(open_v)
        self.lineEdit_open_i.setText(open_i)
        self.lineEdit_open_p.setText(open_p)
        self.lineEdit_open_pf.setText(open_pf)
        
        lock_v = str(self.motor.result_locked_rotor.get('voltage')) if self.motor.result_locked_rotor else ''
        lock_i = str(self.motor.result_locked_rotor.get('current')) if self.motor.result_locked_rotor else ''
        lock_p = str(self.motor.result_locked_rotor.get('power')) if self.motor.result_locked_rotor else ''
        lock_pf = str(self.motor.result_locked_rotor.get('power_factor')) if self.motor.result_locked_rotor else '' 
        self.lineEdit_lock_v.setText(lock_v)
        self.lineEdit_lock_i.setText(lock_i)
        self.lineEdit_lock_p.setText(lock_p)
        self.lineEdit_lock_pf.setText(lock_pf)
        
        
        ###### todo load, separate_excitation, frequency_drift
        ###### figure update
        # print('self.motor.result_load_test', self.motor.result_load_test)
        # if self.motor.result_load_test:
        
        
        self.mpl_load.clear_plot()
        self.mpl_load_2.clear_plot()
        self.mpl_load_3.clear_plot()
        self.mpl_load_4.clear_plot()

        if self.motor.result_load_test:
            ax0 = self.mpl_load.get_axes()
            ax1 = self.mpl_load_2.get_axes()
            ax2 = self.mpl_load_3.get_axes()
            ax3 = self.mpl_load_4.get_axes()
            
            axs = [ax0, ax1, ax2, ax3]  
            # test plot
            ax0.plot([1,2,3,4,5], [1,2,3,4,5])
            ax1.plot([1,2,3,4,5], [1,2,3,4,5])
            ax2.plot([1,2,3,4,5], [1,2,3,4,5])
            ax3.plot([1,2,3,4,5], [1,2,3,4,5])            
            self.motor.polt_load_test(axs=axs)
            
            self.motor.plot_load_test_combined_figure(self.mpl_merge_polt.get_axes())

            
        self.mpl_separate_excitation.clear_plot()
        if self.motor.result_separate_excitation:
            self.motor.plot_separate_excitation(self.mpl_separate_excitation.get_axes())
        
        self.mpl_frequency_drift.clear_plot()
        if self.motor.result_frequency_drift:
            self.motor.plot_frequency_drift(self.mpl_frequency_drift.get_axes())

            
            
        # reprint all mpl widget
        self.mpl_load.repaint()
        self.mpl_separate_excitation.repaint()
        self.mpl_frequency_drift.repaint()
        self.mpl_merge_polt.repaint()
        
        self.repaint()
        
        self.mpl_load.canvas.draw()
            
        
        
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