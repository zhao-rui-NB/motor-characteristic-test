import time 
from threading import Thread

from engine.DeviceManager import DeviceManager

class DataSender:
    
    def __init__(self,device_manager: DeviceManager):
        self.device_manager = device_manager
        
        self.plc_electric_data_sender_running = False
        self.plc_electric_data_sender_interval = 1
        self.plc_electric_data_sender_thread = None
        
    def _plc_electric_data_sender_thread(self):
        while self.plc_electric_data_sender_running:
            time.sleep(self.plc_electric_data_sender_interval)
            data = self.device_manager.power_meter.read_data()
            self.device_manager.plc_electric.send_power_meter_data(data)
        
    def start_plc_electric_data_sender(self, interval=1):
        if self.plc_electric_data_sender_thread is not None:
            print('[DataSender] plc electric data sender already running')
            return
        self.plc_electric_data_sender_running = True
        self.plc_electric_data_sender_interval = interval
        self.plc_electric_data_sender_thread = Thread(target=self._plc_electric_data_sender_thread, daemon=True)
        self.plc_electric_data_sender_thread.start()
        
    def stop_plc_electric_data_sender(self):
        self.plc_electric_data_sender_running = False
        self.plc_electric_data_sender_thread.join()
        self.plc_electric_data_sender_thread = None
        
                    