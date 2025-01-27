from .ModbusTcpWorker import ModbusTcpWorker


class PlcElectric:
    
    def __init__(self, ip, port):
        self.worker = ModbusTcpWorker(ip, port)
    
    
    def send_power_meter_data(self, data_dict):
        '''Send wt330 power meter data to PLC, data only for display'''
        key1 = ['V1', 'I1', 'P1', 'S1', 'Q1', 'LAMBDA1', 'PHI1', 'FU1', 'FI1']
        key2 = ['V2', 'I2', 'P2', 'S2', 'Q2', 'LAMBDA2', 'PHI2', 'FU2', 'FI2']
        key3 = ['V3', 'I3', 'P3', 'S3', 'Q3', 'LAMBDA3', 'PHI3', 'FU3', 'FI3']
        key_sigma = ['V_SIGMA', 'I_SIGMA', 'P_SIGMA', 'S_SIGMA', 'Q_SIGMA', 'LAMBDA_SIGMA', 'PHI_SIGMA', 'FU_SIGMA', 'FI_SIGMA']
        
        # check data_dict key is valid
        if not all([k in data_dict for k in key1 + key2 + key3 + key_sigma]):
            print(f"[PlcElectric] send_power_meter_data error: data_dict key not valid")
            return False
        
        # reg start from 100
        reg_data = []
        
        # cvt all data by key order than prepare for send
        # each float need 2 register
        for k in key1:
            if data_dict[k] is None:
                data_dict[k] = 0
            reg_data.extend(self.worker.float_to_registers(data_dict[k]))
        reg_data.extend([69,69]) # one empty register
        for k in key2:
            if data_dict[k] is None:
                data_dict[k] = 0
            reg_data.extend(self.worker.float_to_registers(data_dict[k]))
        reg_data.extend([69,69]) # one empty register
        for k in key3:
            if data_dict[k] is None:
                data_dict[k] = 0
            reg_data.extend(self.worker.float_to_registers(data_dict[k]))
        reg_data.extend([69,69]) # one empty register
        for k in key_sigma:
            if data_dict[k] is None:
                data_dict[k] = 0
            reg_data.extend(self.worker.float_to_registers(data_dict[k]))
            
        # send data to plc
        return self.worker.write_registers(100, reg_data)
        
    
    '''
    輸出控制
    192.168.0.102
    coil
    17: ASR 單相選擇
    18: ASR OFF
    19: ASR 三相選擇
    20: 單相馬達輸出
    21: 三相馬達輸出
    22: 保留
    23: 馬達輸出 OFF

    1: ASR 單相接線完成
    3: ASR 三相接線完成
    '''
    
    
    def set_ps_output_off(self):
        '''Set power supply output off'''
        r1 = self.worker.write_coil(18, True)
        r2 = self.worker.write_coil(18, False)
        return r1 and r2
    
    def set_ps_output_single(self):
        '''Set power supply output connection to single phase'''
        r1 = self.worker.write_coil(17, True)
        r2 = self.worker.write_coil(17, False)
        return r1 and r2

    def set_ps_output_three(self):
        '''Set power supply output connection to three phase'''
        r1 = self.worker.write_coil(19, True)
        r2 = self.worker.write_coil(19, False)
        return r1 and r2
    
    def set_motor_output_off(self):
        '''Set motor output off'''
        r1 = self.worker.write_coil(23, True)
        r2 = self.worker.write_coil(23, False)
        return r1 and r2
    
    def set_motor_output_single(self):
        '''Set motor output to single phase'''
        r1 = self.worker.write_coil(20, True)
        r2 = self.worker.write_coil(20, False)
        return r1 and r2
    
    def set_motor_output_three(self):
        '''Set motor output to three phase'''
        r1 = self.worker.write_coil(21, True)
        r2 = self.worker.write_coil(21, False)
        return r1 and r2
    
    def get_is_ps_output_single(self):
        '''Get power supply output connection is single phase'''
        return self.worker.read_coils(1, 1)[0]
    
    def get_is_ps_output_three(self):
        '''Get power supply output connection is three phase'''
        return self.worker.read_coils(3, 1)[0]
    
    
if __name__ == '__main__':
    import time

    plc = PlcElectric('192.168.0.102', 502)
    
    print(plc.set_motor_output_off())
    print(plc.set_ps_output_off())


    # plc.set_ps_output_single()
    # time.sleep(1)
    # plc.set_motor_output_single()


    # plc.set_ps_output_three()
    # time.sleep(1)
    # plc.set_motor_output_three()


    print('get_is_ps_output_single', plc.get_is_ps_output_single())
    print('get_is_ps_output_three', plc.get_is_ps_output_three())



    
    
    
    
    