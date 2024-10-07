from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtCore import pyqtSlot

from threading import Thread
import time

from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.ModbusWorker import ModbusWorker
from utils.PowerSupplyASP7100 import PowerSupplyASP7100

class MotorTestSystemEngine:
    
    def __init__(self):
        
        # hardware devices
        self.power_supply: PowerSupplyASP7100 = None
        self.modbus_worker: ModbusWorker = None
        self.power_meter: PowerMeterSPM3 = None 
        
        # measurement data
        self.power_meter_data = {}
        self._power_meter_data_callback = None
        
        self.power_supply_data = {}
        self._power_supply_data_callback = None

    def set_power_supply(self, power_supply: PowerSupplyASP7100):
        self.power_supply = power_supply    
        
    def set_power_meter(self, power_meter: PowerMeterSPM3):
        self.power_meter = power_meter
        
    def set_modbus_worker(self, modbus_worker: ModbusWorker):
        self.modbus_worker = modbus_worker
        
    def register_power_meter_data_callback(self, callback: callable):
        self._power_meter_data_callback = callback
    
    def register_power_supply_data_callback(self, callback: callable):
        self._power_supply_data_callback = callback
    
    
    def _meter_vcfp_callback(self, data):
        self.power_meter_data.update(data)
        try:
            if self._power_meter_data_callback:
                self._power_meter_data_callback(data)
        except Exception as e:
            print(f'[MotorTestSystemEngine] Error in power meter data callback: {e}')
    
    def _update_power_meter_data_thread(self):
        while True:
            if self.modbus_worker.get_task_count() == 0:
                self.power_meter.read_vcfp(self._meter_vcfp_callback)
            else:
                print(f'[MotorTestSystemEngine] power meter worker too busy, task count: {self.modbus_worker.get_task_count()}, skip this round')
            
            time.sleep(0.5)
    
    
    def _make_power_supply_data_callback(self, keys:list[str], skip_callback=False):
        '''
        make a callback function for power supply data
        parameters:
            keys: list of keys to update in self.power_supply_data
            skip_callback: if True, will not call the registered callback function
        '''
        def callback(data):
            try:
                self.power_supply_data.update({k: data[i] if data else None for i, k in enumerate(keys)})
                if self._power_supply_data_callback and not skip_callback:
                    self._power_supply_data_callback(self.power_supply_data) # callback all data, not just the updated one
            except Exception as e:
                print(f'[MotorTestSystemEngine] Error in power supply data callback: {e}')
        return callback                 
    
    
    def _update_power_supply_data_thread(self):
        while True:
            if self.power_supply.worker.get_task_count() == 0:
                # only callback when all data are updated
                self.power_supply.get_voltage(self._make_power_supply_data_callback(['voltage'], skip_callback=True))
                self.power_supply.get_frequency(self._make_power_supply_data_callback(['frequency'], skip_callback=True))
                self.power_supply.get_current_limit(self._make_power_supply_data_callback(['current_limit'], skip_callback=True))
                self.power_supply.get_output(self._make_power_supply_data_callback(['output'], skip_callback=True))
                self.power_supply.measure_source(self._make_power_supply_data_callback(['voltage', 'current', 'frequency', 'power', 'VA', 'ipeak']))
            else:
                print(f'[MotorTestSystemEngine] power supply worker too busy, task count: {self.power_supply.worker.get_task_count()}, skip this round')
            
            time.sleep(0.5)
    
    def start(self):
        # start power meter data update thread
        self.power_meter_data_update_thread = Thread(target=self._update_power_meter_data_thread, daemon=True)
        self.power_meter_data_update_thread.start()
        
        # start power supply data update thread
        self.power_supply_data_update_thread = Thread(target=self._update_power_supply_data_thread, daemon=True)
        self.power_supply_data_update_thread.start()

        

    




    
            
            
if __name__=="__main__":
    engine = MotorTestSystemEngine()
    
    def print_power_meter_data(data):
        print(f'Power Meter Data: {data}')

    def print_power_supply_data(data):
        print(f'Power Supply Data: {data}')
        
    modbus_worker = ModbusWorker("COM3")
    modbus_worker.start()
    
    power_meter = PowerMeterSPM3(modbus_worker, slave_address=0x0F)
    power_supply = PowerSupplyASP7100("127.0.0.1", 2268)
    
    engine.set_power_meter(power_meter)
    engine.set_power_supply(power_supply)
    engine.set_modbus_worker(modbus_worker)
    
    
    engine.register_power_meter_data_callback(print_power_meter_data)
    engine.register_power_supply_data_callback(print_power_supply_data)
    
    engine.start()
    while True:
        pass
    
    
    
    