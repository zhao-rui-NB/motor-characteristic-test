import time 
from threading import Thread

from engine.DeviceManager import DeviceManager

class DataCollector:
    
    def __init__(self,device_manager: DeviceManager):
        self.device_manager = device_manager
        
        self.running = False
        
        # measurement data

        self.power_meter_data = {}
        self.power_meter_data_update_thread = None
        self.power_meter_data_timestamp = 0
        self.power_meter_data_callback = None
        
        # self.power_supply_data_keys = ['voltage', 'frequency', 'current_limit', 'output', 'measure_voltage', 'measure_current', 'measure_frequency', 'measure_power', 'measure_VA', 'measure_ipeak']
        self.power_supply_data = {}
        self.power_supply_data_update_thread = None
        self.power_supply_data_timestamp = 0
        self.power_supply_data_callback = None

    def register_power_meter_data_callback(self, callback: callable):
        self.power_meter_data_callback = callback
    
    def register_power_supply_data_callback(self, callback: callable):
        self.power_supply_data_callback = callback
    
    def start(self):
        if self.running:
            print('[DataCollector] already running, please stop first')
            return
        self.running = True
        
        if self.device_manager.power_meter:
            # start power meter data update thread
            self.power_meter_data_update_thread = Thread(target=self._update_power_meter_data_thread, daemon=True)
            self.power_meter_data_update_thread.start()
        else:
            print('[DataCollector] power meter not initialized, skip power meter data collection')
        
        if self.device_manager.power_supply:
            # start power supply data update thread
            self.power_supply_data_update_thread = Thread(target=self._update_power_supply_data_thread, daemon=True)
            self.power_supply_data_update_thread.start()
        else:
            print('[DataCollector] power supply not initialized, skip power supply data collection')
            
    def stop(self):
        self.running = False
        if self.power_meter_data_update_thread:
            self.power_meter_data_update_thread.join()
        if self.power_supply_data_update_thread:
            self.power_supply_data_update_thread.join()
    
    
    #### Power Meter Data ####
    def _meter_vcfp_callback(self, data: dict[str, float]):
        # add convert kW to W
        without_k = {}
        for key, value in data.items():
            if key.startswith('k'):
                without_k[key.replace('k', '')] = value * 1000 if value is not None else None
        data.update(without_k)
        
        self.power_meter_data.update(data)
        try:
            if self.power_meter_data_callback:
                self.power_meter_data_callback(data)
        except Exception as e:
            print(f'[DataCollector] Error in power meter data callback: {e}')
    
    def _update_power_meter_data_thread(self):
        while self.running and self.device_manager.power_meter:
            if self.device_manager.power_meter.worker.get_task_count() == 0:
                self.device_manager.power_meter.read_vcfp(self._meter_vcfp_callback)
            else:
                print(f'[DataCollector] power meter worker too busy, task count: {self.device_manager.power_meter.worker.get_task_count()}, skip this round')
            
            time.sleep(0.5)
    
    #### Power Supply Data ####
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
                if self.power_supply_data_callback and not skip_callback:
                    self.power_supply_data_callback(self.power_supply_data) # callback all data, not just the updated one
            except Exception as e:
                print(f'[DataCollector] Error in power supply data callback: {e}')
        return callback                 
    
    def _update_power_supply_data_thread(self):
        while self.running and self.device_manager.power_supply:
            if self.device_manager.power_supply.worker.get_task_count() == 0:
                # only callback when all data are updated
                self.device_manager.power_supply.get_voltage(self._make_power_supply_data_callback(['voltage'], skip_callback=True))
                self.device_manager.power_supply.get_frequency(self._make_power_supply_data_callback(['frequency'], skip_callback=True))
                self.device_manager.power_supply.get_current_limit(self._make_power_supply_data_callback(['current_limit'], skip_callback=True))
                self.device_manager.power_supply.get_output(self._make_power_supply_data_callback(['output'], skip_callback=True))
                self.device_manager.power_supply.measure_source(self._make_power_supply_data_callback(['measure_voltage', 'measure_current', 'measure_frequency', 'measure_power', 'measure_VA', 'measure_ipeak']))
            else:
                print(f'[DataCollector] power supply worker too busy, task count: {self.device_manager.power_supply.worker.get_task_count()}, skip this round')
            
            time.sleep(0.5)
            



if __name__=="__main__":
    from engine.DeviceManager import DeviceManager

    
    
    device_manager = DeviceManager()
    device_manager.init_power_supply("127.0.0.1", 2268)
    device_manager.init_power_meter("COM3", 0x0F)
    
    data_collector = DataCollector(device_manager)
    
    
    def print_power_meter_data(data):
        # if data is dict and value is not none print each value 2 decimal places
        if type(data) == dict:
            print(f'Power Meter Data: { {k: f"{v:.1f}" if v is not None else None for k, v in data.items()} }')
        else:
            print(f'Power Meter Data: {data}')
        
    def print_power_supply_data(data):
        print(f'Power Supply Data: {data}')
        
    data_collector.register_power_meter_data_callback(print_power_meter_data)
    data_collector.register_power_supply_data_callback(print_power_supply_data) 
    
    
    
    try:
        data_collector.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    data_collector.stop()
    print('done')
    # time.sleep(3)