from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

import struct
import threading

'''
   2025_0118: cp form ModbusWorker then change to TCP

'''
class ModbusTcpWorker:

    def __init__(self, host, port=502, timeout=0.5):
        self.client: ModbusTcpClient = ModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout
        )
        self.lock = threading.Lock()
        
        self.start() # connect to modbus device

    def start(self):
        res = self.client.connect()
        if res:
            print(f"[ModbusTcpWorker] connected to {self.client.comm_params.host}")
        else:
            print(f"[ModbusTcpWorker] failed to connect to {self.client.comm_params.host}")

    def stop(self):
        self.client.close()
        print(f"[ModbusTcpWorker] disconnected from {self.client.comm_params.host}")

    def read_input_registers(self,  address, count, slave=1):
        with self.lock:
            try:
                result = self.client.read_input_registers(address=address, count=count, slave=slave)
                if not result.isError():
                    return result.registers
                else:
                    print(f"[ModbusTcpWorker] read input registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")

    def read_holding_registers(self, address, count, slave=1):
        with self.lock:
            try:
                result = self.client.read_holding_registers(address=address, count=count, slave=slave)
                if not result.isError():
                    return result.registers
                else:
                    print(f"[ModbusTcpWorker] read holding registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")

    def write_register(self, address, value, slave=1):
        with self.lock:
            try:
                result = self.client.write_register(address=address, value=value, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusTcpWorker] write register error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")
    
    def write_registers(self, address, values, slave=1):
        with self.lock:
            try:
                result = self.client.write_registers(address=address, values=values, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusTcpWorker] write registers error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")  

    def write_coil(self, address, value, slave=1):
        with self.lock:
            try:
                result = self.client.write_coil(address=address, value=value, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusTcpWorker] write coil error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")
                
    def write_coils(self, address, values, slave=1):
        with self.lock:
            try:
                result = self.client.write_coils(address=address, values=values, slave=slave)
                if not result.isError():
                    return True
                else:
                    print(f"[ModbusTcpWorker] write coils error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")
    
    
    def read_coils(self, address, count, slave=1):
        with self.lock:
            try:
                result = self.client.read_coils(address=address, count=count, slave=slave)
                if not result.isError():
                    return result.bits
                else:
                    print(f"[ModbusTcpWorker] read coils error: {result}")
            except ModbusException as e:
                print(f"[ModbusTcpWorker] Modbus exception: {e}")
                

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
    
    modbus = ModbusTcpWorker('127.0.0.1', port=502)


    modbus.stop()
    print('done')
