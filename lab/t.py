# file: motor_test_system/__init__.py
from .engine import MotorTestSystemEngine
from .data_manager import DataManager
from .device_manager import DeviceManager
from .test_runner import TestRunner

# file: motor_test_system/engine.py
from .data_manager import DataManager
from .device_manager import DeviceManager
from .test_runner import TestRunner

class MotorTestSystemEngine:
    def __init__(self):
        self.data_manager = DataManager()
        self.device_manager = DeviceManager()
        self.test_runner = TestRunner(self.device_manager, self.data_manager)

    def start(self):
        self.data_manager.start()
        self.device_manager.start()
        self.test_runner.start()

# file: motor_test_system/data_manager.py
from threading import Thread
import time

class DataManager:
    def __init__(self):
        self.power_meter_data = {}
        self.power_supply_data = {}
        self._power_meter_data_callback = None
        self._power_supply_data_callback = None

    def register_power_meter_data_callback(self, callback):
        self._power_meter_data_callback = callback

    def register_power_supply_data_callback(self, callback):
        self._power_supply_data_callback = callback

    def update_power_meter_data(self, data):
        self.power_meter_data.update(data)
        if self._power_meter_data_callback:
            self._power_meter_data_callback(data)

    def update_power_supply_data(self, data):
        self.power_supply_data.update(data)
        if self._power_supply_data_callback:
            self._power_supply_data_callback(self.power_supply_data)

    def start(self):
        # Start any necessary threads for data management

# file: motor_test_system/device_manager.py
from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.ModbusWorker import ModbusWorker
from utils.PowerSupplyASP7100 import PowerSupplyASP7100

class DeviceManager:
    def __init__(self):
        self.power_supply = None
        self.modbus_worker = None
        self.power_meter = None

    def set_power_supply(self, power_supply):
        self.power_supply = power_supply

    def set_power_meter(self, power_meter):
        self.power_meter = power_meter

    def set_modbus_worker(self, modbus_worker):
        self.modbus_worker = modbus_worker

    def start(self):
        # Initialize and start devices if necessary

# file: motor_test_system/test_runner.py
import time
from threading import Thread

class TestRunner:
    def __init__(self, device_manager, data_manager):
        self.device_manager = device_manager
        self.data_manager = data_manager

    def start(self):
        self._start_power_meter_update_thread()
        self._start_power_supply_update_thread()

    def _start_power_meter_update_thread(self):
        Thread(target=self._update_power_meter_data_thread, daemon=True).start()

    def _start_power_supply_update_thread(self):
        Thread(target=self._update_power_supply_data_thread, daemon=True).start()

    def _update_power_meter_data_thread(self):
        while True:
            if self.device_manager.modbus_worker.get_task_count() == 0:
                self.device_manager.power_meter.read_vcfp(self.data_manager.update_power_meter_data)
            time.sleep(0.5)

    def _update_power_supply_data_thread(self):
        while True:
            if self.device_manager.power_supply.worker.get_task_count() == 0:
                self._update_power_supply_data()
            time.sleep(0.5)

    def _update_power_supply_data(self):
        self.device_manager.power_supply.get_voltage(lambda data: self.data_manager.update_power_supply_data({'voltage': data[0] if data else None}))
        self.device_manager.power_supply.get_frequency(lambda data: self.data_manager.update_power_supply_data({'frequency': data[0] if data else None}))
        self.device_manager.power_supply.get_current_limit(lambda data: self.data_manager.update_power_supply_data({'current_limit': data[0] if data else None}))
        self.device_manager.power_supply.get_output(lambda data: self.data_manager.update_power_supply_data({'output': data[0] if data else None}))
        self.device_manager.power_supply.measure_source(lambda data: self.data_manager.update_power_supply_data({
            'voltage': data[0], 'current': data[1], 'frequency': data[2],
            'power': data[3], 'VA': data[4], 'ipeak': data[5]
        }))

    def run_voltage_test(self, start_voltage, end_voltage, step, duration):
        for voltage in range(start_voltage, end_voltage + 1, step):
            self.device_manager.power_supply.set_voltage(voltage)
            time.sleep(duration)
            # Record power meter data
            power_meter_data = self.data_manager.power_meter_data.copy()
            power_supply_data = self.data_manager.power_supply_data.copy()
            # Here you would typically save this data to a file or database
            print(f"Voltage: {voltage}, Power Meter: {power_meter_data}, Power Supply: {power_supply_data}")

# file: main.py
from motor_test_system import MotorTestSystemEngine
from utils.ModbusWorker import ModbusWorker
from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.PowerSupplyASP7100 import PowerSupplyASP7100

def main():
    engine = MotorTestSystemEngine()

    modbus_worker = ModbusWorker("COM3")
    power_meter = PowerMeterSPM3(modbus_worker, slave_address=0x0F)
    power_supply = PowerSupplyASP7100("127.0.0.1", 2268)

    engine.device_manager.set_modbus_worker(modbus_worker)
    engine.device_manager.set_power_meter(power_meter)
    engine.device_manager.set_power_supply(power_supply)

    engine.data_manager.register_power_meter_data_callback(lambda data: print(f"Power Meter Data: {data}"))
    engine.data_manager.register_power_supply_data_callback(lambda data: print(f"Power Supply Data: {data}"))

    engine.start()

    # Run a test
    engine.test_runner.run_voltage_test(start_voltage=100, end_voltage=200, step=10, duration=5)

if __name__ == "__main__":
    main()