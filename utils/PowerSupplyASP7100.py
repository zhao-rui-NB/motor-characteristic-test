import threading

from .ScpiSocketWorker import ScpiSocketWorker

'''
   2025_0118: change to sync, not test

'''

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

class PowerSupplyASP7100:
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

        success, response = self.worker.send_command(cmd)
        
        if not success:
            print(f"[PowerSupplyASP7100] Command failed: {cmd}")
        
        items = self._split_response(response) # if none, return None

        # if no need to convert type, return directly
        if type_list is None:
            return items
        
        # convert type, is failed, return None for each item
        items = self._cvt_response_type(items, type_list)
        if items is None:
            return [None for _ in type_list]
        return items

    def get_idn(self):
        return self._generic_command("*IDN?", type_list=[str, str, str, str])

    def clear_status(self):
        return self._generic_command("*CLS")

    def set_voltage(self, voltage):
        return self._generic_command(f"SOUR:VOLT {voltage}")

    def set_frequency(self, frequency):
        return self._generic_command(f"SOUR:FREQ {frequency}")

    def set_current_limit(self, current):
        return self._generic_command(f"SOUR:CURR:LIM:RMS {current}")

    def set_output(self, output):
        return self._generic_command(f"OUTPut {output}")

    def get_voltage(self):
        return self._generic_command("SOUR:VOLT?", type_list=[float])

    def get_frequency(self):
        return self._generic_command("SOUR:FREQ?", type_list=[float])

    def get_current_limit(self):
        return self._generic_command("SOUR:CURR:LIM:RMS?", type_list=[float])

    def get_output(self):
        return self._generic_command("OUTPut?", type_list=[int])

    def measure_current(self):
        return self._generic_command("MEAS:CURR?", type_list=[float])

    def measure_voltage(self):
        return self._generic_command("MEAS:VOLT?", type_list=[float])

    def measure_apparent_power(self):
        return self._generic_command("MEAS:POW:APP?", type_list=[float])

    def measure_power(self):
        return self._generic_command("MEAS:POW?", type_list=[float])

    def measure_source(self):
        '''
        return [voltage, current, frequency, real_power, apparent_power, peak_current]
                <voltage>,<current>,<frequency>,<power>,<VA>,<ipeak>
        '''
        self._generic_command("SOUR:READ?", type_list=[float, float, float, float, float, float])




if __name__ == "__main__":
    import time

    ps = PowerSupplyASP7100("127.0.0.1", 2268)

    print(ps.get_idn())
    
    ps.set_voltage(50)
    print(ps.get_voltage())

    ps.set_voltage(3.3)
    print(ps.get_voltage())

    ps.worker.stop()