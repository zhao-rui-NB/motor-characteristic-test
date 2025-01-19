# %%
import threading

from .ScpiSocketWorker import ScpiSocketWorker

'''
   2025_0118: change to sync, not test

'''


class PowerSupplyASR6450:
    def __init__(self, host, port):
        self.worker = ScpiSocketWorker(host, port)
        self.worker.start()

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

    def _generic_command(self, cmd, type_list=None):
        
        success, reponse = self.worker.send_command(cmd)
        
        if not success:
            print(f"[PowerSupplyASR6450] Command failed: {cmd}")
            
        items = self._split_response(reponse) # if none, return None
        
        # if no need to convert type, return directly
        if type_list is None:
            return items
        
        # convert type, is failed, return None for each item
        items = self._cvt_response_type(items, type_list)
        if items is None:
            return [None for _ in type_list]
        return items
    
    # 回復已知設定參數
    def reset(self):
        return self._generic_command("*RST")

    def get_idn(self):
        return self._generic_command("*IDN?", type_list=[str, str, str, str])

    def clear_status(self):
        return self._generic_command("*CLS")

    # voltage    
    def set_voltage(self, voltage):
        return self._generic_command(f"SOUR:VOLT {voltage}")
        
    def get_voltage(self):
        return self._generic_command("SOUR:VOLT?", type_list=[float])
        
    # frequency
    def set_frequency(self, frequency):
        return self._generic_command(f"SOUR:FREQ {frequency}")

    def get_frequency(self):
        return self._generic_command("SOUR:FREQ?", type_list=[float])
    
    # current limit
    def set_current_limit_state(self, state):
        # [:SOURce]:CURRent:LIMit:RMS:MODE
        '''IRMS limit state: 0=off, 1=on '''
        return self._generic_command(f"SOUR:CURR:LIM:RMS:MODE {state}")
    
    def get_current_limit_state(self):
        return self._generic_command("SOUR:CURR:LIM:RMS:MODE?", type_list=[int])
        
    def set_current_limit(self, current):
        return self._generic_command(f"SOUR:CURR:LIM:RMS {current}")

    def get_current_limit(self):
        return self._generic_command("SOUR:CURR:LIM:RMS?", type_list=[float])

    def set_output(self, output):
        return self._generic_command(f"OUTPut {output}")

    def get_output(self):
        return self._generic_command("OUTPut?", type_list=[int])

    def measure_current(self): 
        return self._generic_command("MEAS:CURR?", type_list=[float])

    def measure_voltage(self):
        return self._generic_command("MEAS:VOLT?", type_list=[float])

    def measure_apparent_power(self):
        return self._generic_command("MEAS:POW:APP?", type_list=[float])

    def measure_power(self):
        self._generic_command("MEAS:POW?", type_list=[float])

    # 設定輸出相和線數
    def set_output_phase_mode(self, phase_para):
        # :SYSTem:CONFigure:PHASe 
        '''
        phase_para
        0 3P4W 
        1 1P2W 
        2 1P3W 
        '''

        return self._generic_command(f"SYSTem:CONFigure:PHASe {phase_para}")

    def get_output_phase_mode(self):
        return self._generic_command("SYSTem:CONFigure:PHASe?", type_list=[str])
    
    # 設定輸出電壓範圍
    def set_voltage_range(self, range_para):
        # VOLTage:RANGe 
        '''
        range_para
        100 | 0 100V 
        200 | 1 200V 
        AUTO | 2 
        '''
        return self._generic_command(f"VOLTage:RANGe {range_para}")

    # 設定輸出交直流模式
    def set_source_mode(self, mode_para):
        # [:SOURce]:MODE? 
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
        return self._generic_command(f"MODE {mode_para}")

    # 設定輸出直流篇移準位
    def set_voltage_offset(self, offset):
        # [:SOURce]:VOLTage[:LEVel][:IMMediate]:OFFSet 
        return self._generic_command(f"VOLTage:OFFSet {offset}")

    # 設定參數是否三相一起調整
    def set_instrument_edit(self, para):
        # :INSTrument:EDIT 
        '''
            EACH 0 Each phase 
            ALL 1 All phase 
        '''
        return self._generic_command(f"INSTrument:EDIT {para}")

    # 設定要調整的相
    def set_instrument_select(self, para):
        # :INSTrument:SELect 
        '''
            L1 | 0 L1 phase 
            L2 | 1 L2 phase 
            L3 | 2 L3 phase 
        '''
        return self._generic_command(f"INSTrument:SELect {para}")

    # 設定某兩項之間的相位角
    def set_phase_phase(self, target, angle):
        # [:SOURce]:PHASe:PHASe
        '''
            <target> <NR1> 
                L12 | 0 Phase angle between L1-L2 
                L13 | 1 Phase angle between L1-L3 
            <phase angle> <NR2> 
                MINimum 0 
                MAXimum 359.9 
        '''
        return self._generic_command(f"PHASe:PHASe {target},{angle}")

    # 設定是否為平衡系統模式
    def set_phase_mode(self, mode_para):
        # [:SOURce]:PHASe:MODE
        '''
            mode_para
                UNBalance|0     UNBalance 
                BALance|1       Balance 
        '''
        return self._generic_command(f"PHASe:MODE {mode_para}")
    
            

if __name__ == "__main__":
    import time

    # ps = PowerSupplyASR6450("192.168.0.103", 5025)
    ps = PowerSupplyASR6450("127.0.0.1", 2268)

    # # %%
    # ps.set_voltage(50, None)
    
    ps.clear_status()

    # %%
    print("get_idn")
    print(ps.get_idn())

    # 0: 3P4W, 1: 1P2W, 2: 1P3W 
    # ps.set_output_phase_mode(0)

    # print("set_voltage_range")
    # ps.set_voltage_range(2)

    # %%
    print("set_voltage", ps.set_voltage(127))
    # 

    print("get_voltage")
    print(ps.get_voltage())

    # print("set_frequency")
    # ps.set_frequency(55)

    # print("set_source_mode")
    # ps.set_source_mode(1)

    ############################
    # 每相個別調整
    # print("set_instrument_edit")
    # ps.set_instrument_edit(0)

    # 設定要調整的相
    # print("set_instrument_select")

    # # L1 phase
    # ps.set_instrument_select(0)
    # ps.set_voltage_offset(0)

    # # L2 phase
    # ps.set_instrument_select(1)
    # ps.set_voltage_offset(0)

    # # L3 phase
    # ps.set_instrument_select(2)
    # ps.set_voltage_offset(0)
    ############################

    # 設定相位角
    # print("set_phase_phase")
    # ps.set_phase_phase(0, 90)
    # ps.set_phase_phase(1, 180)

    ############################

    # OUTPUT
    # print("set_output")
    # ps.set_output(1)


