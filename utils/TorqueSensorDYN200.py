from .ModbusWorker import ModbusWorker

'''
   2025_0118: change to sync, not test

'''

class TorqueSensorDYN200:
    def __init__(self, modbus_worker: ModbusWorker, slave_address):
        self.worker: ModbusWorker = modbus_worker
        self.slave_address = slave_address

    def read_torque(self):
        result = self.worker.read_holding_registers(0x0000, 2, self.slave_address)
        if result:
            data = {'torque': ModbusWorker.registers_to_long(result)}
        else:
            data = {'torque': None}
        return data

    def read_speed(self):
        result = self.worker.read_holding_registers(0x0002, 2, self.slave_address)
        if result:
            data = {'speed': ModbusWorker.registers_to_long(result)}
        else:
            data = {'speed': None}
        return data
    
    def read_power(self):
        result = self.worker.read_holding_registers(0x0004, 2, self.slave_address)
        if result:
            data = {'power': ModbusWorker.registers_to_long(result)}
        else:
            data = {'power': None}
        return data
    
    def read_all(self):
        result = self.worker.read_holding_registers(0x0000, 6, self.slave_address)
        if result:
            torque = ModbusWorker.registers_to_long(result[0:2])
            speed = ModbusWorker.registers_to_long(result[2:4])
            power = ModbusWorker.registers_to_long(result[4:6])
            data = {'torque': torque, 'speed': speed, 'power': power}
        else:
            data = {'torque': None, 'speed': None, 'power': None}
        return data

if __name__ == "__main__":

    def print_resaut(result):
        if result:
            print({k: f'{v:.2f}' if v is not None else 'N/A' for k, v in result.items()})
        else:
            print("Failed to read data")

    modbus_worker = ModbusWorker(port='COM3', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5)

    torque_sensor = TorqueSensorDYN200(modbus_worker, slave_address=0x01)
    
    print_resaut(torque_sensor.read_torque())
    print_resaut(torque_sensor.read_speed())
    print_resaut(torque_sensor.read_power())
    print_resaut(torque_sensor.read_all())


    modbus_worker.stop()