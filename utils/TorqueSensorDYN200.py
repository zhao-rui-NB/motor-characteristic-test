from .ModbusWorker import ModbusWorker

class TorqueSensor:
    def __init__(self, modbus_worker: ModbusWorker, slave_address):
        self.worker: ModbusWorker = modbus_worker
        self.slave_address = slave_address

    def read_torque(self, callback):
        def process_result(result):
            if result:
                data = {'torque': ModbusWorker.registers_to_long(result)}
            else:
                data = {'torque': None}
            callback(data)

        self.worker.read_holding_registers_threaded(0x0000, 2, self.slave_address, process_result)

    def read_speed(self, callback):
        def process_result(result):
            if result:
                data = {'speed': ModbusWorker.registers_to_long(result)}
            else:
                data = {'speed': None}
            callback(data)

        self.worker.read_holding_registers_threaded(0x0002, 2, self.slave_address, process_result)

    def read_power(self, callback):
        def process_result(result):
            if result:
                data = {'power': ModbusWorker.registers_to_long(result)}
            else:
                data = {'power': None}
            callback(data)

        self.worker.read_holding_registers_threaded(0x0004, 2, self.slave_address, process_result)

    def read_all(self, callback):
        def process_result(result):
            if result:
                torque = ModbusWorker.registers_to_long(result[0:2])
                speed = ModbusWorker.registers_to_long(result[2:4])
                power = ModbusWorker.registers_to_long(result[4:6])
                data = {'torque': torque, 'speed': speed, 'power': power}
            else:
                data = {'torque': None, 'speed': None, 'power': None}
            callback(data)

        self.worker.read_holding_registers_threaded(0x0000, 6, self.slave_address, process_result)

if __name__ == "__main__":
    def print_callback(result):
        if result:
            print({k: f'{v:.2f}' if v is not None else 'N/A' for k, v in result.items()})
        else:
            print("Failed to read data")

    modbus_worker = ModbusWorker(port='COM3', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5)
    modbus_worker.start()

    torque_sensor = TorqueSensor(modbus_worker, slave_address=0x01)

    torque_sensor.read_torque(print_callback)
    torque_sensor.read_speed(print_callback)
    torque_sensor.read_power(print_callback)
    torque_sensor.read_all(print_callback)

    # Wait for all tasks to complete
    while not modbus_worker.task_queue.empty():
        pass

    modbus_worker.stop()