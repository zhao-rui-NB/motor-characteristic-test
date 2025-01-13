# %%
import threading

from .ScpiSocketWorker import ScpiSocketWorker


'''

*IDN	識別設備
*CLS	清除狀態
MEAS:CURR	測量電流
MEAS:VOLT	測量電壓
MEAS:POW:APP	測量視在功率
MEAS:POW	測量實際功率

SOUR:READ	讀取源設置
SOUR:VOLT	設置/查詢輸出電壓
SOUR:FREQ	設置/查詢輸出頻率
SOUR:CURR:LIM:RMS	設置/查詢 RMS 電流限制
SOUR:VOLT:RANG	設置/查詢電壓範圍
OUTPut	控制/查詢輸出開關狀態
SYSTem:REBoot	重啟系統

'''

class PowerSupplyASR6450:
    def __init__(self, host, port):
        self.worker = ScpiSocketWorker(host, port)
        self.worker.start()
        # self.lock = threading.Lock()

    def _split_response(self, response, to_1d=True):
        if response is None:
            return None
        
        if isinstance(response, bytes):
            response = response.decode()
        response = response.strip() 
        
        response = response.split(";")
        response = [x.split(",") for x in response]

        response_1d = []
        for x in response:
            response_1d.extend(x)
        
        return response_1d if to_1d else response
    
    def _cvt_response_type(self, response_list, type_list):
        if response_list is None or type_list is None:
            return None
        if len(response_list) != len(type_list):
            return None
        
        for i in range(len(response_list)):
            try:
                response_list[i] = type_list[i](response_list[i])
            except ValueError:
                return None
        return response_list

    def _generic_command(self, cmd, callback, type_list=None):
        def internal_callback(result):
            if not callback:
                return
            
            success, response = result
            
            items = self._split_response(response) # if none, return None
            items = self._cvt_response_type(items, type_list)
            
            if items is None and type_list:
                callback([None for _ in type_list])
            else:
                callback(items)

        self.worker.send_command_threaded(cmd, callback=internal_callback)


    def reset(self, callback):
        self._generic_command("*RST", callback)

    def get_idn(self, callback):
        self._generic_command("*IDN?", callback, type_list=[str, str, str, str])

    def clear_status(self, callback):
        self._generic_command("*CLS", callback)


    '''
        Source Commands
        programming Manual p52
    ''' 
    # voltage    
    def set_voltage(self, voltage, callback):
        self._generic_command(f"SOUR:VOLT {voltage}", callback)
        
    def get_voltage(self, callback):
        self._generic_command("SOUR:VOLT?", callback, type_list=[float])
        
    # frequency
    def set_frequency(self, frequency, callback):
        self._generic_command(f"SOUR:FREQ {frequency}", callback)

    def get_frequency(self, callback):
        self._generic_command("SOUR:FREQ?", callback, type_list=[float])
    
    # current limit
    def set_current_limit_state(self, state, callback):
        # [:SOURce]:CURRent:LIMit:RMS:MODE
        '''IRMS limit state: 0=off, 1=on '''
        self._generic_command(f"SOUR:CURR:LIM:RMS:MODE {state}", callback)
    
    def get_current_limit_state(self, callback):
        self._generic_command("SOUR:CURR:LIM:RMS:MODE?", callback, type_list=[int])
        
    def set_current_limit(self, current, callback):
        self._generic_command(f"SOUR:CURR:LIM:RMS {current}", callback)

    def get_current_limit(self, callback):
        self._generic_command("SOUR:CURR:LIM:RMS?", callback, type_list=[float])


    '''
        Output Commands
        programming Manual p50
    '''
    def set_output(self, output, callback):
        self._generic_command(f"OUTPut {output}", callback)

    def get_output(self, callback):
        self._generic_command("OUTPut?", callback, type_list=[int])

    '''
        Measure Commands
        programming Manual p48
    '''

    def measure_current(self, callback):
        self._generic_command("MEAS:CURR?", callback, type_list=[float])

    def measure_voltage(self, callback):
        self._generic_command("MEAS:VOLT?", callback, type_list=[float])

    def measure_apparent_power(self, callback):
        self._generic_command("MEAS:POW:APP?", callback, type_list=[float])

    def measure_power(self, callback):
        self._generic_command("MEAS:POW?", callback, type_list=[float])

    def set_output_phase(self, phase_para, callback):
        # :SYSTem:CONFigure:PHASe 
        '''
        phase_para
        0 3P4W 
        1 1P2W 
        2 1P3W 
        '''

        self._generic_command(f"SYSTem:CONFigure:PHASe {phase_para}", callback)

    # VOLTage:RANGe 
    def set_voltage_range(self, range_para, callback):
        '''
        range_para
        100 | 0 100V 
        200 | 1 200V 
        AUTO | 2 
        '''
        self._generic_command(f"VOLTage:RANGe {range_para}", callback)

    # [:SOURce]:MODE? 
    def set_source_mode(self, mode_para, callback):
        #  ac int : 1
        #  dc int : 2
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
        self._generic_command(f"MODE {mode_para}", callback)

    # [:SOURce]:VOLTage[:LEVel][:IMMediate]:OFFSet 
    def set_voltage_offset(self, offset, callback):
        self._generic_command(f"VOLTage:OFFSet {offset}", callback)


    # :INSTrument:EDIT 
    # 個別調參數
    def set_instrument_edit(self, para, callback):
        '''
            EACH 0 Each phase 
            ALL 1 All phase 
        '''
        self._generic_command(f"INSTrument:EDIT {para}", callback)

    # :INSTrument:SELect 
    def set_instrument_select(self, para, callback):
        '''
            L1 | 0 L1 phase 
            L2 | 1 L2 phase 
            L3 | 2 L3 phase 
        '''
        self._generic_command(f"INSTrument:SELect {para}", callback)


    # [:SOURce]:PHASe:PHASe
    def set_phase_phase(self, target, angle, callback):
                        
        '''
            <target> <NR1> 
                L12 | 0 Phase angle between L1-L2 
                L13 | 1 Phase angle between L1-L3 
            <phase angle> <NR2> 
                MINimum 0 
                MAXimum 359.9 
        '''
        self._generic_command(f"PHASe:PHASe {target},{angle}", callback)

    # [:SOURce]:PHASe:MODE
    def set_phase_mode(self, mode_para, callback):
        '''
            mode_para
                UNBalance|0 UNBalance 
                BALance|1 Balance 
        '''
        self._generic_command(f"PHASe:MODE {mode_para}", callback)
    
            

if __name__ == "__main__":
    import time

    ps = PowerSupplyASR6450("192.168.0.103", 5025)

    def print_callback(result):
        print(f"Received: {result}")

    # # %%
    # ps.set_voltage(50, None)
    
    ps.clear_status(print_callback)

    # %%
    print("get_idn")
    ps.get_idn(print_callback)
    time.sleep(0.1)

    # ps.set_output_phase(0, print_callback)
    # time.sleep(0.1)

    # set voltage range
    # print("set_voltage_range")
    # ps.set_voltage_range(2, print_callback)
    # time.sleep(0.1)

    # %%
    # print("set_voltage")
    # ps.set_voltage(127, print_callback)
    # ps.set_voltage(10, print_callback)
    # time.sleep(0.1)

    # print("get_voltage")
    # ps.get_voltage(print_callback)
    # time.sleep(0.1)


    # set frequency
    # print("set_frequency")
    # ps.set_frequency(55, print_callback)
    # time.sleep(0.1)


    # 電壓
    # set source mode
    # print("set_source_mode")
    # ps.set_source_mode(1, print_callback)




    ############################
    # set instrument edit
    # print("set_instrument_edit")
    # ps.set_instrument_edit(0, print_callback)

    # # set instrument select
    # print("set_instrument_select")
    # ps.set_instrument_select(0, print_callback)

    # # set voltage offset
    # print("set_voltage_offset")
    # ps.set_voltage_offset(0, print_callback)

    # ps.set_instrument_select(1, print_callback)
    # ps.set_voltage_offset(0, print_callback)
    # ps.set_instrument_select(2, print_callback)
    # ps.set_voltage_offset(0, print_callback)
    ############################

    # set instrument edit
    # print("set_instrument_edit")
    # ps.set_instrument_edit(0, print_callback)

    # ps.set_instrument_select(0, print_callback)
    # ps.set_voltage(127, print_callback)
    # ps.set_instrument_select(1, print_callback)
    # ps.set_voltage(127, print_callback)
    # ps.set_instrument_select(2, print_callback)
    # ps.set_voltage(127, print_callback)

    ############################


    # set phase phase
    # print("set_phase_phase")
    ps.set_phase_phase(0, 90, print_callback)
    ps.set_phase_phase(1, 180, print_callback)



    # print("get_output")
    # ps.get_output(print_callback)
    # time.sleep(0.1)

    # print("set_output")
    # ps.set_output(True, print_callback)
    # time.sleep(0.1)

    # print("get_output")
    # ps.get_output(print_callback)
    # time.sleep(0.1)

    print("set_output")
    ps.set_output(1, print_callback)
    # time.sleep(0.1)

    # print("get_output")
    # ps.get_output(print_callback)
    # time.sleep(0.1)

    time.sleep(1)
