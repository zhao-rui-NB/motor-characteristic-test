import struct
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

class Modbus:
    def __init__(self, port, slave_address, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1):
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )
        self.slave_address = slave_address

    def connect(self):
        return self.client.connect()

    def close(self):
        self.client.close()

    def read_input_registers(self, address, count):
        try:
            result = self.client.read_input_registers(address=address, count=count, slave=self.slave_address)
            if not result.isError():
                return result.registers
            else:
                print(f"讀取錯誤: {result}")
                return None
        except ModbusException as e:
            print(f"Modbus異常: {e}")
            return None

    def read_holding_registers(self, address, count):
        try:
            result = self.client.read_holding_registers(address=address, count=count, slave=self.slave_address)
            if not result.isError():
                return result.registers
            else:
                print(f"讀取錯誤: {result}")
                return None
        except ModbusException as e:
            print(f"Modbus異常: {e}")
            return None

    @staticmethod
    def registers_to_float(registers):
        if len(registers) != 2:
            raise ValueError("需要兩個寄存器來轉換為浮點數")
        return struct.unpack('f', struct.pack('HH', registers[0], registers[1]))[0]

    @staticmethod
    def registers_to_long(registers):
        if len(registers) != 2:
            raise ValueError("需要兩個寄存器來轉換為長整型")
        return struct.unpack('i', struct.pack('HH', registers[0], registers[1]))[0]

    def read_float(self, address):
        registers = self.read_input_registers(address, 2)
        if registers:
            return self.registers_to_float(registers)
        return None

    def read_long(self, address):
        registers = self.read_input_registers(address, 2)
        if registers:
            return self.registers_to_long(registers)
        return None

    def write_register(self, address, value):
        try:
            result = self.client.write_register(address=address, value=value, slave=self.slave_address)
            if not result.isError():
                return True
            else:
                print(f"寫入錯誤: {result}")
                return False
        except ModbusException as e:
            print(f"Modbus異常: {e}")
            return False

    def write_float(self, address, value):
        # 將浮點數轉換為兩個16位整數
        data = struct.pack('f', value)
        register1, register2 = struct.unpack('HH', data)
        
        # 寫入兩個寄存器
        if self.write_register(address, register1) and self.write_register(address + 1, register2):
            return True
        return False
    
if __name__ == "__main__":
    mb = Modbus(port='COM3', baudrate=9600, slave_address=0x0F)

    mb.connect()
    
    
    # read Vln_a
    register_address = 0x1000    # 起始寄存器地址
    res = mb.read_float(register_address)
    print('res', res)
    
    # read x1018
    register_address = 0x1018    # 起始寄存器地址
    res = mb.read_float(register_address)
    print('res', res)
    
    