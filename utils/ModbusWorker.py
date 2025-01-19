from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

import struct
import threading

'''
   2025_0118: change to sync, not test

'''
class ModbusWorker:

    def __init__(self, port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        self.client: ModbusSerialClient = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )
        self.lock = threading.Lock()
        
        self.start() # connect to modbus device

    def start(self):
        res = self.client.connect()
        if res:
            print(f"[ModbusWorker] connected to {self.client.comm_params.host}")
        else:
            print(f"[ModbusWorker] failed to connect to {self.client.comm_params.host}")

    def stop(self):
        self.client.close()
        print(f"[ModbusWorker] disconnected from {self.client.comm_params.host}")

    def read_input_registers(self,  address, count, slave):
        with self.lock:
            try:
                result = self.client.read_input_registers(address=address, count=count, slave=slave)
                if not result.isError():
                    return result.registers
                else:
                    print(f"[ModbusWorker] read input registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusWorker] Modbus exception: {e}")

    def read_holding_registers(self, address, count, slave):
        with self.lock:
            try:
                result = self.client.read_holding_registers(address=address, count=count, slave=slave)
                if not result.isError():
                    return result.registers
                else:
                    print(f"[ModbusWorker] read holding registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusWorker] Modbus exception: {e}")

    def write_register(self, address, value, slave):
        with self.lock:
            try:
                result = self.client.write_register(address=address, value=value, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusWorker] write register error: {result}")
            except ModbusException as e:
                print(f"[ModbusWorker] Modbus exception: {e}")
    
    def write_registers(self, address, values, slave):
        with self.lock:
            try:
                result = self.client.write_registers(address=address, values=values, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusWorker] write registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusWorker] Modbus exception: {e}")  


    @staticmethod
    def registers_to_float(registers):
        if len(registers) == 2:
            return struct.unpack('f', struct.pack('HH', registers[0], registers[1]))[0]

    @staticmethod
    def registers_to_long(registers):
        if len(registers) == 2:
            return struct.unpack('i', struct.pack('HH', registers[0], registers[1]))[0]

    @staticmethod
    def float_to_registers(value):
        data = struct.pack('f', value)
        return struct.unpack('HH', data)
    
    @staticmethod
    def long_to_registers(value):
        data = struct.pack('i', value)
        return struct.unpack('HH', data)



if __name__ == "__main__":
    import time
    
    counter = 0 
    def read_vcf(worker:ModbusWorker): # datasheet p28 #5 
        global counter
        counter += 1
        print(f'\n\ncounter: {counter}')

        result = worker.read_input_registers(0x1000, 26, 0x0F)
        if result:
            keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency']
            res_dict = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
            print({k: f'{v:.2f}' for k, v in res_dict.items()})

    
    modbus = ModbusWorker(port='COM3')
    
    for i in range(100):
        read_vcf(modbus)
        # time.sleep(1)

    modbus.stop()
    print('done')
