from .ModbusWorker import ModbusWorker
'''
   2025_0118: change to sync, not test

'''
class PowerMeterSPM3:
    def __init__(self, modbus_worker: ModbusWorker, slave_address):
        self.worker = modbus_worker
        self.slave_address = slave_address  # 0x0F

    def read_vcf(self):  # datasheet p28 #5
        keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency']

        result = self.worker.read_input_registers(0x1000, len(keys)*2, self.slave_address)
        
        if result:
            data = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
        else:
            # put all none values
            data = {k: None for k in keys}
        return data

    def read_power_result(self):  # datasheet p28 #6
        keys = ['kW_a', 'kW_b', 'kW_c', 'kW_tot', 'kvar_a', 'kvar_b', 'kvar_c', 'kvar_tot', 'kVA_a', 'kVA_b', 'kVA_c', 'kVA_tot', 'PF']

        result = self.worker.read_input_registers(0x101A, len(keys)*2, self.slave_address)
        if result:
            data = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
        else:
            data = {k: None for k in keys}
        return data

    def read_vcfp(self):  # merge read_vcf and read_power_result
        keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency', 'kW_a', 'kW_b', 'kW_c', 'kW_tot', 'kvar_a', 'kvar_b', 'kvar_c', 'kvar_tot', 'kVA_a', 'kVA_b', 'kVA_c', 'kVA_tot', 'PF']
        
        result = self.worker.read_input_registers(0x1000, len(keys)*2, self.slave_address)
        if result:
            data = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
        else:
            data = {k: None for k in keys}
        return data
    
    def read_energy(self):
        keys = ['kWh', 'kvarh', 'kVAh']

        result =  self.worker.read_input_registers(0x1034, len(keys)*2, self.slave_address)
        if result:
            data = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
        else:
            data = {k: None for k in keys}
        return data
        
if __name__ == "__main__":
    def print_callback(result):
        if result:
            print({k: f'{v:.2f}' for k, v in result.items()})
        else:
            print("Failed to read data")

    modbus_worker = ModbusWorker(port='COM3')

    powermeter = PowerMeterSPM3(modbus_worker, slave_address=0x0F)

    powermeter.read_vcf(print)
    powermeter.read_power_result(print)
    powermeter.read_energy(print)

    modbus_worker.stop()