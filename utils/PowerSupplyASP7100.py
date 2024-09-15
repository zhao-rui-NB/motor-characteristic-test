
from .ScpiSocketClient import SocketClient


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
        self.client = SocketClient(host, port)
        self.client.start()
    
    # scpi return value to number 
    
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
    
    
    def get_idn(self):
        cmd = "*IDN?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [str, str, str, str])
    
    def clear_status(self):
        cmd = "*CLS"
        succ, _ = self.client.send_command(cmd, False)
        return succ
    
    def set_voltage(self, voltage):
        cmd = f"SOUR:VOLT {voltage}"
        succ, _ = self.client.send_command(cmd, False)
        return succ

    def set_frequency(self, frequency):
        cmd = f"SOUR:FREQ {frequency}"
        succ, _ = self.client.send_command(cmd, False)
        return succ
    
    def set_current_limit(self, current):
        cmd = f"SOUR:CURR:LIM:RMS {current}"
        succ, _ = self.client.send_command(cmd, False)
        return succ
        
    def set_output(self, output):
        cmd = f"OUTPut {'1' if output else '0'}"
        succ, _ = self.client.send_command(cmd, False)
        return succ
        
    def get_voltage(self):
        cmd = "SOUR:VOLT?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def get_frequency(self):
        cmd = "SOUR:FREQ?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def get_current_limit(self):
        cmd = "SOUR:CURR:LIM:RMS?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def get_output(self):
        cmd = "OUTPut?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [int])
    
    def measure_current(self):
        cmd = "MEAS:CURR?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def measure_voltage(self):
        cmd = "MEAS:VOLT?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])

    def measure_apparent_power(self):
        cmd = "MEAS:POW:APP?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def measure_power(self):
        cmd = "MEAS:POW?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        return self._cvt_response_type(items, [float])
    
    def measure_source(self):
        cmd = "SOUR:READ?"
        succ, response = self.client.send_command(cmd)
        items = self._split_response(response)
        # measure v c p va ipeak
        # <voltage>, <current>, <frequency>, <power>, <VA>, <ipeak>
        return self._cvt_response_type(items, [float, float, float, float, float, float])
    

    
if __name__ == "__main__":
        import time
        
        ps = PowerSupplyASP7100("127.0.0.1", 2268)
        ps.client.wait_connect()
        
        
        # print(ps.get_voltage())
        # time.sleep(0.01)
        
        # ps.set_voltage(3.3)
        # time.sleep(0.01)
        
        # print(ps.get_voltage())
        # time.sleep(0.01)
        
        
        
        # print(ps.get_idn())
        # time.sleep(0.01)
        
        
        # print(ps.measure_source())
        # time.sleep(0.01)
        
        
        # for i in range(50):
        #     print(ps.measure_current())
        #     time.sleep(0.1)
        
    
        print(ps.get_output())
        time.sleep(0.01)
        ps.set_output(True)
        time.sleep(0.01)
        print(ps.get_output())
        
        time.sleep(0.01)
        
        
        print(ps.get_output())
        time.sleep(0.01)
        ps.set_output(False)
        time.sleep(0.01)
        print(ps.get_output())
    
        ps.client.stop()
    