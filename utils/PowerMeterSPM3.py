
from .Modbus import Modbus

class PowerMeterSPM3:
    def __init__(self, port, slave_address):
        self.modbus = Modbus(port=port, slave_address=slave_address)

        self.modbus.connect()
        
    def read_vcf(self): # datasheet p28 #5 
        # start address 0x1000 4byte float
        keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency']
        data = self.modbus.read_input_registers(0x1000,len(keys)*2)
        # cvt to float store data into dict
        return {k: self.modbus.registers_to_float(data[i*2:i*2+2]) for i, k in enumerate(keys)} 

    def read_power_resault(self): # datasheet p28 #6
        # start address 0x101A 4byte float
        key = ['kW_a', 'kW_b', 'kW_c', 'kW_tot', 'kvar_a', 'kvar_b', 'kvar_c', 'kvar_tot', 'kVA_a', 'kVA_b', 'kVA_c', 'kVA_tot', 'PF']
        data = self.modbus.read_input_registers(0x101A,len(key)*2)
        # cvt to float store data into dict
        return {k: self.modbus.registers_to_float(data[i*2:i*2+2]) for i, k in enumerate(key)}

    def read_energy(self):
        # start address 0x1034 4byte float
        key = ['kWh', 'kvarh', 'kVAh']
        data = self.modbus.read_input_registers(0x1034,len(key)*2)
        # cvt to float store data into dict
        return {k: self.modbus.registers_to_float(data[i*2:i*2+2]) for i, k in enumerate(key)}
            
    
    
if __name__ == "__main__":
    powermeter = PowerMeterSPM3(port='COM3', slave_address=0x0F)
    
    print(powermeter.read_vcf())
    
    print(powermeter.read_power_resault())
    
    print(powermeter.read_energy()) 