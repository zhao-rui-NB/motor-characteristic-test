import time 
from threading import Thread
from engine.DeviceManager import DeviceManager
# from engine.DataCollector import DataCollector
from engine.DataSender import DataSender
from engine.Motor import Motor


class TestRunner:
    
    def __init__(self,device_manager: DeviceManager):
        self.device_manager = device_manager

    def system_init(self, phase_mode:int):
        '''
            this function is used to initialize the system
            - reset all devices to default
            - setting the power supply output mode
            - setting the power supply output connection
        '''
        
        is_single_phase = True if phase_mode == 1 else False
        
        # check device connection
        ps = self.device_manager.power_supply.get_idn()
        pm = self.device_manager.power_meter.get_serial_number()
        if ps is None or None in ps:
            print('[device_initialization] Power Supply Connection Error')
            return False
        if pm is None or None in pm:
            print('[device_initialization] Power Meter Connection Error')
            return False
        
        # turn off all output
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off() # a 馬達輸出關閉(off)

        ps_single = self.device_manager.plc_electric.get_is_ps_output_single()
        ps_three = self.device_manager.plc_electric.get_is_ps_output_three()
        c1 = is_single_phase and not ps_single
        c2 = not is_single_phase and not ps_three
        if c1 or c2:
            self.device_manager.plc_electric.set_ps_output_off() # b ASR6450 輸出關閉(off)
            time.sleep(1)
            # setup system 1P/2W or 3P/4W
            if is_single_phase: # c 設定外部接線開關(三相:Y03 ON, 單相低電流:Y03 ON, 單相高電流:Y01 ON,)
                self.device_manager.plc_electric.set_ps_output_single()
                time.sleep(1)
                self.device_manager.power_supply.set_output_phase_mode(1) # phase_para 0: 3P4W, 1: 1P2W, 2: 1P3W
                m = self.device_manager.power_supply.get_output_phase_mode()
                if m[0] != '1P2W':
                    raise ValueError('Power Supply Phase Mode Setting Error')
            else:
                self.device_manager.plc_electric.set_ps_output_three()
                time.sleep(1)
                self.device_manager.power_supply.set_output_phase_mode(0)
                m = self.device_manager.power_supply.get_output_phase_mode()
                if m[0] != '3P4W':
                    raise ValueError('Power Supply Phase Mode Setting Error')

        r1 = self.device_manager.plc_electric.get_is_ps_output_single()
        r3 = self.device_manager.plc_electric.get_is_ps_output_three()
        if is_single_phase and not r1 or not is_single_phase and not r3:
            raise ValueError('PLC Electric Output Setting Error') 
        
        self.device_manager.plc_mechanical.set_break(0)
        
        # self.device_manager.power_supply.reset()
        self.device_manager.power_supply.clear_status()
        
        # self.device_manager.power_meter.reset()
        # time.sleep(10)

        self.device_manager.power_meter.clear_status()
        self.device_manager.power_meter.set_input_wiring('P3W3')
        self.device_manager.power_meter.set_numeric_format('ASC')
        self.device_manager.power_meter.set_preset_read_pattern(2)
        self.device_manager.power_meter.set_list_number(40)
        
        return True
    # ok
    def test_dc_resistance(self, motor:Motor):
        self.system_init(motor.power_phases)  
        is_single_phase = True if motor.power_phases == 1 else False      

        self.device_manager.power_supply.set_instrument_edit(1) # 同時調整
        self.device_manager.power_supply.set_source_mode(2) # 0 DC-INT # e 設定ASR6450 DC+INT 三相系統
        # self.device_manager.power_supply.set_voltage(0) # g 設定ASR6450 交流電壓=0
        self.device_manager.power_supply.set_current_limit(motor.rated_current*1.2) # h 設定ASR6450 最大電流命令(滿載電流*120%)
        # self.device_manager.power_supply.set_frequency(motor.frequency)# i 設定ASR6450 頻率輸出命令
        
        self.device_manager.power_supply.set_voltage_offset(0) # set all dc offset to 0

        self.device_manager.power_supply.set_output(1) # 打開輸出


        # j 設定ASR6450 直流電壓輸出命令	(單相馬達)	直流電壓 Vtest_dc=0.1V
        # k 若為三相馬達, 則分三次測試
        # l 讀取 ASR6450 電壓(核對電壓輸出)
        # m 讀取 WT333 電壓 (核對電壓輸出)
        test_dc_voltage = 1
        for i in range(1 if is_single_phase else 3):
            self.device_manager.power_supply.set_instrument_edit(1) # 1 All
            self.device_manager.power_supply.set_voltage_offset(0) # set all dc offset to 0
            
            self.device_manager.power_supply.set_instrument_edit(0) # 0 Each
            self.device_manager.power_supply.set_instrument_select(i)
            self.device_manager.power_supply.set_voltage_offset(test_dc_voltage)
            time.sleep(1)
            # read WT333 voltage
            data:dict = self.device_manager.power_meter.read_data()
            #### todo: check voltage
            print(f"[run_dc_resistance_test] read from power meter, V1:{data.get('V1', None)}, V2:{data.get('V2', None)}, V3:{data.get('V3', None)}")

            # check voltage, chech if the voltage is correct, in +- 30% range
            # 1 : V1, 30% rated voltage
            # 2 : V1 and V3, 30% rated voltage
            # 3 : V3, 30% rated voltage

            if data.get('V1') is None or data.get('V2') is None or data.get('V3') is None:
                print('[run_dc_resistance_test] Power Meter Voltage Read Error')
                return False

            if i==0:
                if abs(data.get('V1') - test_dc_voltage)/test_dc_voltage > 0.3:
                    print('[run_dc_resistance_test] Power Meter Voltage Read Error')
                    return False
            elif i==1:
                if abs(data.get('V1') - test_dc_voltage)/test_dc_voltage > 0.3:
                    print('[run_dc_resistance_test] Power Meter Voltage Read Error')
                    return False
                if abs(data.get('V3') - test_dc_voltage)/test_dc_voltage > 0.3: 
                    print('[run_dc_resistance_test] Power Meter Voltage Read Error')
                    return False
            elif i==2:
                if abs(data.get('V3') - test_dc_voltage)/test_dc_voltage > 0.3:
                    print('[run_dc_resistance_test] Power Meter Voltage Read Error')
                    return False
            # input(f'read finish {i}, press Enter to continue')
        
        print(f"[run_dc_resistance_test] system check done")
            
        # set all dc offset to 0
        # self.device_manager.power_supply.set_instrument_edit(1) # 1 All
        # self.device_manager.power_supply.set_voltage_offset(0) # set all dc offset to 0
        # print('[run_dc_resistance_test] System check done')
        
        # n 提示 ”待測馬達請脫離扭矩測試系統”
        # o 等待啟動確認按鍵(提示輸出確認?)
        print('[run_dc_resistance_test] ”待測馬達請脫離扭矩測試系統”')
        input('Press Enter to continue:')
        
        # p 設定外部輸出開關 (啟動測試電壓輸出Y24 OR Y25)
        if is_single_phase:
            self.device_manager.plc_electric.set_motor_output_single()
        else:
            self.device_manager.plc_electric.set_motor_output_three()
            
    
        # q 連續  讀取 WT333  [電壓Vdc, 電流Idc, 功率Pdc ]
        # r 逐漸增加直流輸出電壓 , 直到電流 = [滿載電流 ]
        raw_data = []
        for i in range(1 if is_single_phase else 3):
            self.device_manager.power_supply.set_instrument_edit(1) # 1 All
            self.device_manager.power_supply.set_voltage_offset(0) # set all dc offset to 0
            self.device_manager.power_supply.set_instrument_edit(0) # 0 Each
            self.device_manager.power_supply.set_instrument_select(i)
            time.sleep(2)
            v_test_dc = 1                        
            while True:
                self.device_manager.power_supply.set_voltage_offset(v_test_dc)
                time.sleep(0.1)
                data:dict = self.device_manager.power_meter.read_data()
                v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
                i_str = f"I1:{data.get('I1')}, I2:{data.get('I2')}, I3:{data.get('I3')}"
                print(f"[run_dc_resistance_test] read from power meter, {v_str}, {i_str}")
                
                if i==0:
                    now_current = data.get('I1')
                elif i==1:
                    now_current = data.get('I1') + data.get('I3')
                elif i==2:
                    now_current = data.get('I3')
                
                if now_current >= motor.rated_current/2:
                    for _ in range(5):
                        time.sleep(1)
                        data:dict = self.device_manager.power_meter.read_data()
                        raw_data.append({'power_meter': data})
                    break

                v_test_dc += 0.1
            input(f'read finish {i}, press Enter to continue')
        # return
        
        # s 計算直流電阻 = (2/3)*( Vdc/Idc)
        # t 轉動轉子以讀取不同角度的電阻值
        print(f'[run_dc_resistance_test] Test Done')

        # u 關閉測試電壓輸出Y27
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off()
        
        # v 存入資料 
        motor.add_result_dc_resistance(raw_data)
        
        # w 結束測試 
        return True
    # ok
    def run_open_circuit_test(self, motor:Motor):
        self.system_init(motor.power_phases)
        # 
        if motor.rated_voltage < 130:
            self.device_manager.power_meter.set_voltage_range(150)
        elif motor.rated_voltage < 250:
            self.device_manager.power_meter.set_voltage_range(300)
        else:
            self.device_manager.power_meter.set_voltage_range(600)


        is_single_phase = True if motor.power_phases == 1 else False
        
        # e 三相模式 設定ASR6450 為平衡三相系統
        self.device_manager.power_supply.set_phase_mode(1) # 0:UNBalance, 1:Balance  
        # f 三相模式 設定ASR6450 為三相電壓同步調整系統
        self.device_manager.power_supply.set_instrument_edit(1)
        self.device_manager.power_supply.set_source_mode(1) # 1 AC-INT 
        # g 設定ASR6450 電壓命令
        self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732)
        # h 設定ASR6450 最大電流命令(無載電流*120%)
        # self.device_manager.power_supply.set_current_limit(motor.rated_current)
        self.device_manager.power_supply.set_current_limit(15)

        # i 設定ASR6450 頻率輸出命令
        self.device_manager.power_supply.set_frequency(motor.frequency)
        # j 設定ASR6450 電壓輸出命令
        self.device_manager.power_supply.set_output(1)
        time.sleep(1)

        
        # k 讀取 ASR6450 電壓與頻率 (核對電壓輸出)
        # l 讀取 WT333 電壓與頻率 (核對電壓輸出)
        data:dict = self.device_manager.power_meter.read_data()
        v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
        f_str = f"F1:{data.get('FU1')}"
        print(f'[run_open_circuit_test] read from power meter, {v_str}, {f_str}')
        #### todo: check voltage

        # check voltage, and frequency in 30% range
        if data.get('V1') is None or data.get('V2') is None or data.get('V3') is None:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V1') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V2') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V3') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('FU1') - motor.frequency)/motor.frequency > 0.03:
            print('[run_open_circuit_test] Power Meter Frequency Read Error')
            return False
        
        print(f"[run_open_circuit_test] system check done")



        # return
        
        
        # m 提示 ”待測馬達請脫離扭矩測試系統”
        # n 等待啟動確認按鍵(提示輸出確認?)
        print('[run_open_circuit_test] ”待測馬達請脫離扭矩測試系統”')
        input('Press Enter to continue:')   


        # self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732)
        self.device_manager.power_supply.set_voltage(0)

        # o 設定外部輸出開關 (啟動測試電壓輸出Y24 OR Y25)
        if is_single_phase:
            self.device_manager.plc_electric.set_motor_output_single()
        else:
            self.device_manager.plc_electric.set_motor_output_three()

        # set voltage 30% - 100%
        for i in range(30, 100+1, 5):
            self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732*i/100)
            time.sleep(0.2)

        print('[run_open_circuit_test] 啟動完成')

        
            
        raw_data = []
                
        # p 連續  讀取 WT333  [電壓Vnl, 電流Inl, 功率Pnl, 功率因數PFnl ]
        for i in range(10):
            time.sleep(1)
            data:dict = self.device_manager.power_meter.read_data()
            # 'V_SIGMA', 'I_SIGMA', 'P_SIGMA', 'S_SIGMA', 'Q_SIGMA', 'LAMBDA_SIGMA'
            v_str = f"V1:{data.get('V1')}, V3:{data.get('V3')}"
            i_str = f"I1:{data.get('I1')}, I3:{data.get('I3')}"
            p_str = f"P1:{data.get('P1')}, P3:{data.get('P3')}"
            sig_str = f"V_SIGMA:{data.get('V_SIGMA')}, I_SIGMA:{data.get('I_SIGMA')}, P_SIGMA:{data.get('P_SIGMA')}, LAMBDA_SIGMA:{data.get('LAMBDA_SIGMA')}"
            print(f"[run_open_circuit_test] read from power meter, {v_str}, {i_str}, {p_str}, {sig_str}")
            raw_data.append({'power_meter': data})
        
        # q 關閉測試電壓輸出Y27
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off()
        
        # r 存入資料 
        motor.add_result_open_circuit(raw_data)
        # s 結束測試 
        
        print('[run_open_circuit_test] Test Done')
        
        return True
    # 堵轉試驗 ok
    def run_lock_rotor_test(self, motor:Motor):
        self.system_init(motor.power_phases)
        self.device_manager.power_meter.set_voltage_range(60)
        is_single_phase = True if motor.power_phases == 1 else False
        
        check_system_voltage = 3

        # e 三相模式 設定ASR6450 為平衡三相系統
        self.device_manager.power_supply.set_phase_mode(1) # 0:UNBalance, 1:Balance  
        # f 三相模式 設定ASR6450 為三相電壓同步調整系統
        self.device_manager.power_supply.set_instrument_edit(1)
        self.device_manager.power_supply.set_source_mode(1) # 1 AC-INT 
        # g 設定ASR6450 電壓命令
        self.device_manager.power_supply.set_voltage(check_system_voltage/1.732)
        # h 設定ASR6450 最大電流命令(無載電流*120%)
        # self.device_manager.power_supply.set_current_limit(motor.rated_current)
        self.device_manager.power_supply.set_current_limit(15)

        # i 設定ASR6450 頻率輸出命令
        self.device_manager.power_supply.set_frequency(motor.frequency)
        # j 設定ASR6450 電壓輸出命令
        self.device_manager.power_supply.set_output(1)
        time.sleep(1)

        
        # k 讀取 ASR6450 電壓與頻率 (核對電壓輸出)
        # l 讀取 WT333 電壓與頻率 (核對電壓輸出)
        data:dict = self.device_manager.power_meter.read_data()
        v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
        f_str = f"F1:{data.get('FU1')}"
        print(f'[run_open_circuit_test] read from power meter, {v_str}, {f_str}')
        #### todo: check voltage

        # check_system_voltage
        # check voltage, and frequency in 30% range
        if data.get('V1') is None or data.get('V2') is None or data.get('V3') is None:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V1') - check_system_voltage)/check_system_voltage > 0.1:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V2') - check_system_voltage)/check_system_voltage > 0.1:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V3') - check_system_voltage)/check_system_voltage > 0.1:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('FU1') - motor.frequency)/motor.frequency > 0.03:
            print('[run_open_circuit_test] Power Meter Frequency Read Error')
            return False
        
        print(f"[run_open_circuit_test] system check done")
        # m. 提示 ”待測馬達請安裝至扭矩測試系統”
        # n. 制動輸出(DA OUTPUT)輸出50% (2000 Count)
        self.device_manager.plc_mechanical.set_break(2000)
        
        # o. 等待啟動確認按鍵(提示輸出確認?)
        print('[run_lock_rotor_test] ”待測馬達請安裝至扭矩測試系統”')
        input('Press Enter to continue:')
        
        # p. 設定外部輸出開關 (啟動測試電壓輸出Y24 OR Y25)
        if is_single_phase:
            self.device_manager.plc_electric.set_motor_output_single()
        else:
            self.device_manager.plc_electric.set_motor_output_three()
            
        # q. 連續  讀取 WT333  [電壓Vbk, 電流Ibk, 功率Pbk, 功率因數PFbk ]
        # r. 逐漸增加輸出電壓 , 直到電流 = [滿載電流 ]
        v_test = 3
        raw_data = []
        while True:
            self.device_manager.power_supply.set_voltage(v_test/1.732)
            time.sleep(0.5)
            data:dict = self.device_manager.power_meter.read_data()
            v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
            i_str = f"I1:{data.get('I1')}, I2:{data.get('I2')}, I3:{data.get('I3')}"
            print(f"[run_dc_resistance_test] read from power meter, {v_str}, {i_str}")
            
            now_current = data.get('I1')
            if now_current >= motor.rated_current or data.get('V1') > motor.rated_voltage*0.3:
                print(f"[run_dc_resistance_test] start read data")
                for _ in range(5):
                    data:dict = self.device_manager.power_meter.read_data()
                    raw_data.append({'power_meter': data})
                    time.sleep(1)
                break
            v_test += 1
                
        # s. 轉動轉子以讀取不同角度的測試值
        # t. 關閉測試電壓輸出Y27
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off()
        self.device_manager.plc_mechanical.set_break(0)
        # u. 存入資料 

        motor.add_result_locked_rotor(raw_data)
        # v. 結束測試 
        print('[run_lock_rotor_test] Test Done')
        return True
    # 負載試驗 ok
    def run_load_test(self, motor:Motor):
        self.system_init(motor.power_phases)
        # 
        if motor.rated_voltage < 130:
            self.device_manager.power_meter.set_voltage_range(150)
        elif motor.rated_voltage < 250:
            self.device_manager.power_meter.set_voltage_range(300)
        else:
            self.device_manager.power_meter.set_voltage_range(600)


        is_single_phase = True if motor.power_phases == 1 else False
        
        # e 三相模式 設定ASR6450 為平衡三相系統
        self.device_manager.power_supply.set_phase_mode(1) # 0:UNBalance, 1:Balance  
        # f 三相模式 設定ASR6450 為三相電壓同步調整系統
        self.device_manager.power_supply.set_instrument_edit(1)
        self.device_manager.power_supply.set_source_mode(1) # 1 AC-INT 
        # g 設定ASR6450 電壓命令
        self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732)
        # h 設定ASR6450 最大電流命令(無載電流*120%)
        # self.device_manager.power_supply.set_current_limit(motor.rated_current)
        self.device_manager.power_supply.set_current_limit(15)

        # i 設定ASR6450 頻率輸出命令
        self.device_manager.power_supply.set_frequency(motor.frequency)
        # j 設定ASR6450 電壓輸出命令
        self.device_manager.power_supply.set_output(1)
        time.sleep(1)

        
        # k 讀取 ASR6450 電壓與頻率 (核對電壓輸出)
        # l 讀取 WT333 電壓與頻率 (核對電壓輸出)
        data:dict = self.device_manager.power_meter.read_data()
        v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
        f_str = f"F1:{data.get('FU1')}"
        print(f'[run_open_circuit_test] read from power meter, {v_str}, {f_str}')
        #### todo: check voltage

        # check voltage, and frequency in 30% range
        if data.get('V1') is None or data.get('V2') is None or data.get('V3') is None:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V1') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V2') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('V3') - motor.rated_voltage)/motor.rated_voltage > 0.03:
            print('[run_open_circuit_test] Power Meter Voltage Read Error')
            return False
        if abs(data.get('FU1') - motor.frequency)/motor.frequency > 0.03:
            print('[run_open_circuit_test] Power Meter Frequency Read Error')
            return False
        
        print(f"[run_open_circuit_test] system check done")
        
        # m 提示 ”待測馬達請脫離扭矩測試系統”
        # n 等待啟動確認按鍵(提示輸出確認?)
        print('[run_open_circuit_test] ”待測馬達請連結至負載測試系統”')
        input('Press Enter to continue:')   


        # self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732)
        self.device_manager.power_supply.set_voltage(0)

        # o 設定外部輸出開關 (啟動測試電壓輸出Y24 OR Y25)
        if is_single_phase:
            self.device_manager.plc_electric.set_motor_output_single()
        else:
            self.device_manager.plc_electric.set_motor_output_three()

        # set voltage 30% - 100%
        # for i in range(30, 100+1, 5):
        for i in range(30, 50+1, 5):
            self.device_manager.power_supply.set_voltage(motor.rated_voltage/1.732*i/100)
            time.sleep(0.2)

        print('[run_open_circuit_test] 啟動完成')
        
        # q. 逐漸增加制動控制的輸出電流(DA output, 加載)
        # r. 連續  讀取 WT333  [電壓V 電流I, 功率P, 功率因數PF ]
        # s. 重複(q.)直到馬達鎖住 ( 轉速=0)
        raw_data = []
        for da in range(0, 4000, 5):
            self.device_manager.plc_mechanical.set_break(da)
            time.sleep(0.5)
            
            power_meter = self.device_manager.power_meter.read_data()
            mechanical = self.device_manager.plc_mechanical.get_mechanical_data()
            raw_data.append({'power_meter': power_meter, 'mechanical': mechanical})
            # print .3f
            print(f"[run_load_test] speed:{mechanical['speed']}, torque:{mechanical['torque']:.2f}, DA:{da}, V1:{power_meter.get('V1')}, I1:{power_meter.get('I1')}")

            # if mechanical['speed'] <= motor.speed*0.5:
            if mechanical['speed'] <= 1:
                break

        # t. 關閉測試電壓輸出Y27
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off()
        self.device_manager.plc_mechanical.set_break(0)
        # u. 存入資料 
        motor.add_result_load_test(raw_data)
        # v. 結束測試 
    # 鐵損分離試驗
    def run_separate_excitation_test(self, motor:Motor):
        self.system_init(motor.power_phases)
        is_single_phase = True if motor.power_phases == 1 else False
        
        # e. 三相模式 設定ASR6450 為平衡三相系統
        self.device_manager.power_supply.set_phase_mode(1) # 0:UNBalance, 1:Balance
        # f. 三相模式 設定ASR6450 為三相電壓同步調整系統
        self.device_manager.power_supply.set_instrument_edit(1)
        # g. 設定ASR6450 電壓命令
        self.device_manager.power_supply.set_voltage(5)
        # h. 設定ASR6450 最大電流命令(無載電流*120%)
        self.device_manager.power_supply.set_source_mode(1) # 1 AC-INT 
        self.device_manager.power_supply.set_current_limit(motor.rated_current*1.2)
        # i. 設定ASR6450 頻率輸出命令
        self.device_manager.power_supply.set_frequency(motor.frequency)
        # j. 設定ASR6450 電壓輸出命令
        self.device_manager.power_supply.set_output(1)
        # k. 讀取 ASR6450 電壓與頻率 (核對電壓輸出)
        # l. 讀取 WT333 電壓與頻率 (核對電壓輸出)
        data:dict = self.device_manager.power_meter.read_data()
        v_str = f"V1:{data.get('V1')}, V2:{data.get('V2')}, V3:{data.get('V3')}"
        f_str = f"F1:{data.get('F1')}, F2:{data.get('F2')}, F3:{data.get('F3')}"
        print(f'[run_lock_rotor_test] read from power meter, {v_str}, {f_str}')
        

        # m. 提示 ”待測馬達請脫離扭矩測試系統”
        # n. 等待啟動確認按鍵(提示輸出確認?)
        print('[run_separate_excitation_test] ”待測馬達請脫離扭矩測試系統”')
        input('Press Enter to continue:')
        
        # o. 設定ASR6450 輸出電壓=20%額定電壓(減少啟動電流衝擊) 設定外部輸出開關 (啟動測試電壓輸出Y24 OR Y25) , 逐漸調整輸出電壓到額定電壓的80%(每0.5 Sec增加 5%)等待3 Sec 讓系統穩定後, 開是測試:
        if is_single_phase:
            self.device_manager.plc_electric.set_motor_output_single()
        else:
            self.device_manager.plc_electric.set_motor_output_three()
            
        for i in range(0.2, 1, 0.05): # 20% to 100%
            self.device_manager.power_supply.set_voltage(i*motor.rated_voltage)
            time.sleep(0.5)
        self.device_manager.power_supply.set_voltage(motor.rated_voltage)
        time.sleep(3)
        
        
        # p. 連續  讀取 WT333  [電壓Vt5, 電流It5, 功率Pt5, 功率因數PFt5]
        # q. 逐漸調整輸出電壓到額定電壓的120%  [80%-120%]
        raw_data = []
        for p in range(80, 120+1, 5):
            self.device_manager.power_supply.set_voltage(motor.rated_voltage*p/100)
            time.sleep(0.5)
            data:dict = self.device_manager.power_meter.read_data()
            raw_data.append({'power_meter': data})
            

        # r. 關閉測試電壓輸出Y27
        self.device_manager.power_supply.set_output(0)
        self.device_manager.plc_electric.set_motor_output_off()
        self.device_manager.plc_electric.set_ps_output_off()
        
        # s. 存入資料 
        motor.add_result_separate_excitation(raw_data)
        # t. 結束測試 
        print('[run_separate_excitation_test] Test Done')
        return True
    

        


        
if __name__ == '__main__':
    
    device_manager = DeviceManager()
    device_manager.load_devices_from_ini('device.ini')
    
    # exit()
    # data_sender = DataSender(device_manager)
    # data_sender.start_plc_electric_data_sender(interval=1)
    
    motor = Motor()
    motor.rated_voltage = 220
    motor.power_phases = 3
    motor.speed = 3600
    motor.rated_current = 3
    motor.frequency = 60
    motor.horsepower = 1
    motor.poles = 2
    motor.no_load_current = 0.8
    
    test_runner = TestRunner(device_manager)
    print(test_runner.device_manager.power_meter.get_serial_number())
    print(test_runner.device_manager.power_supply.get_idn())


    # test_runner.system_init(1)
    # test_runner.test_dc_resistance(motor)
    # test_runner.run_open_circuit_test(motor)
    # test_runner.run_lock_rotor_test(motor)

    test_runner.run_load_test(motor)

    
    
    # test_runner.run_separate_excitation_test(motor)

    import json
    timestamp = motor.make_time_stamp()
    with open(f'test_file/motor_{timestamp}_load_test.json', 'w') as f:
        json.dump(motor.to_dict(), f, indent=4)
    
    
    

    
            