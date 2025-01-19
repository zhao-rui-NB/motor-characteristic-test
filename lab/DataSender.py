import time 
from threading import Thread

from engine.DeviceManager import DeviceManager
from engine.DataCollector import DataCollector


'''
each 1 second read data collector data then send to modbus display 

'''

class DataSender:
    
    def __init__(self,device_manager: DeviceManager, data_collector: DataCollector):
        self.device_manager = device_manager
        self.data_collector = data_collector

        self.display_sender_running = False
        self.display_sender_thread = None
        self.display_sender_interval = 1
        self.display_address_config: dict[str,dict[str,dict]] = {} # data name to address map
        
    
    def start_display_sender(self, display_address:dict[str,dict[str,dict]], interval=1):
        self.display_sender_running = True
        self.display_sender_interval = interval
        self.display_address_config = display_address
        self.display_sender_thread = Thread(target=self._display_sender_thread, daemon=True)
        self.display_sender_thread.start()
        
    def stop_display_sender(self):
        self.display_sender_running = False
        self.display_sender_thread.join()
        self.display_sender_thread = None
        
    def _display_sender_thread(self):
        '''
        display sender address format: {'power_meter': {'Vln_a': 0, 'Vln_b': 105, 'Vll_bc': 105, 'I_c': 84}, 'power_supply': {'voltage': 17}}
        '''
        while self.display_sender_running:
            time.sleep(self.display_sender_interval)
            
            # get data from data collector {name: data}
            power_meter_data = self.data_collector.power_meter_data
            power_supply_data = self.data_collector.power_supply_data
            
            # the config of display need to be updated, {name: address}
            power_meter_address = self.display_address_config.get('power_meter', {})
            power_supply_address = self.display_address_config.get('power_supply', {})
            
            # send data to display
            for name, address in power_meter_address.items():
                if name in power_meter_data:
                    data = power_meter_data[name]
                    display = self.device_manager.segment_display_dict[address]
                    if data is not None:
                        display.set_number(data)
                    else:
                        display.set_number(6969)
                        
            for name, address in power_supply_address.items():
                if name in power_supply_data:
                    data = power_supply_data[name]
                    display = self.device_manager.segment_display_dict[address]
                    if data is not None:
                        display.set_number(data)
                    else:
                        display.set_number(6969)
                    
                    